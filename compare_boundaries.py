import geopandas as gpd
import pandas as pd
import requests
import json
import os
from datetime import datetime, UTC
from pathlib import Path
from shapely.geometry import mapping, MultiLineString, LineString, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import polygonize, unary_union
import plotly.graph_objects as go

OVERPASS_CACHE_PATH = Path("output/overpass_cache.json")
OVERPASS_CACHE_TTL_SECONDS = 4 * 60 * 60


def _load_overpass_cache(
    cache_path=OVERPASS_CACHE_PATH, ttl_seconds=OVERPASS_CACHE_TTL_SECONDS
):
    if not cache_path.exists():
        return None

    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        fetched_at = payload.get("fetched_at")
        osm_data = payload.get("osm_data")
        if not fetched_at or not isinstance(osm_data, dict):
            return None

        fetched_time = datetime.fromisoformat(fetched_at)
        if fetched_time.tzinfo is None:
            fetched_time = fetched_time.replace(tzinfo=UTC)
        age_seconds = (datetime.now(UTC) - fetched_time).total_seconds()
        if age_seconds <= ttl_seconds:
            return osm_data
    except Exception:
        return None

    return None


def _save_overpass_cache(osm_data, cache_path=OVERPASS_CACHE_PATH):
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "fetched_at": datetime.now(UTC).isoformat(),
            "osm_data": osm_data,
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
    except Exception as e:
        print(f"Warning: Could not save Overpass cache: {e}")


def load_osm_boundaries(target_crs="EPSG:2056"):
    """
    Query Overpass API for Swiss boundaries with swisstopo:BFS_NUMMER.

    Args:
        target_crs: Target coordinate reference system (default: WGS84)

    Returns:
        GeoDataFrame with OSM boundaries
    """

    print("Loading OSM boundaries...")

    # Overpass QL query
    overpass_query = """
    [out:json][timeout:120];
    area["ISO3166-1"="CH"][admin_level=2]->.switzerland;
    (
      relation["boundary"="administrative"]["admin_level"="8"]["swisstopo:BFS_NUMMER"](area.switzerland);
    );
    out geom;
    """

    try:
        osm_data = _load_overpass_cache()
        if osm_data is not None:
            print("  - Using cached Overpass response (<= 4 hours old)")
        else:
            print("  - Querying Overpass API...")
            response = requests.post(
                "http://overpass.osm.ch/api/interpreter",
                data=overpass_query,
                timeout=120,
            )
            response.raise_for_status()
            osm_data = response.json()
            _save_overpass_cache(osm_data)
            print("  - Cached Overpass response")

        if not osm_data.get("elements"):
            print("  - No boundaries found with swisstopo:BFS_NUMMER tag")
            return None

        print(f"  - Found {len(osm_data['elements'])} OSM elements")

        # Convert to GeoJSON
        geojson = osm_to_geojson(osm_data)

        if not geojson["features"]:
            print("  - Error: No valid features created from OSM data")
            return None

        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geojson["features"], crs="EPSG:4326")

        # 2D ENFORCEMENT: Strip Z-coords if any (OSM sometimes has them in specific tags)
        gdf.geometry = gdf.geometry.apply(force_2d)

        # Reproject if needed
        if target_crs != "EPSG:4326":
            gdf = gdf.to_crs(target_crs)
            print(f"  - Reprojected to: {target_crs}")

        print(f"  - Created GeoDataFrame with {len(gdf)} features")
        print(f"  - Columns: {', '.join(gdf.columns)}")

        return gdf

    except Exception as e:
        print(f"Error loading OSM data: {e}")
        return None


def osm_to_geojson(osm_data):
    """Convert OSM JSON format to GeoJSON."""

    geojson = {"type": "FeatureCollection", "features": []}

    for element in osm_data.get("elements", []):
        feature = create_feature(element)
        if feature:
            geojson["features"].append(feature)

    return geojson


def create_feature(element):
    """Convert OSM element to Polygon/MultiPolygon for Area Metrics."""
    e_type = element.get("type")
    tags = element.get("tags", {})
    bfs_num = tags.get("swisstopo:BFS_NUMMER")

    if e_type == "relation":
        outer_lines = []
        inner_lines = []
        all_lines = []

        for member in element.get("members", []):
            if member.get("type") == "way" and "geometry" in member:
                coords = [(pt["lon"], pt["lat"]) for pt in member["geometry"]]
                if len(coords) < 2:
                    continue

                line = LineString(coords)
                if line.is_empty:
                    continue

                all_lines.append(line)

                role = (member.get("role") or "").lower()
                if role == "inner":
                    inner_lines.append(line)
                else:
                    # Role "outer" and blank/unexpected roles are treated as outers.
                    outer_lines.append(line)

        if not all_lines:
            return None

        def _polygonize_lines(lines):
            if not lines:
                return []
            return [poly for poly in polygonize(lines) if not poly.is_empty]

        outer_polygons = _polygonize_lines(outer_lines)
        inner_polygons = _polygonize_lines(inner_lines)

        if outer_polygons:
            assembled = []
            for outer_poly in outer_polygons:
                hole_rings = []
                for inner_poly in inner_polygons:
                    if outer_poly.covers(inner_poly.representative_point()):
                        hole_rings.append(list(inner_poly.exterior.coords))

                polygon_with_holes = Polygon(
                    list(outer_poly.exterior.coords),
                    hole_rings,
                )
                if not polygon_with_holes.is_empty:
                    assembled.append(orient(polygon_with_holes, sign=1.0))

            polygons = assembled
        else:
            polygons = [orient(poly, sign=1.0) for poly in _polygonize_lines(all_lines)]

        if polygons:
            final_geom = unary_union(polygons)
        else:
            # If it won't polygonize, we can't do area metrics effectively
            return None

        return {
            "type": "Feature",
            "id": f"relation/{element['id']}",
            "properties": {
                "osm_id": element["id"],
                "swisstopo:BFS_NUMMER": bfs_num,
                **tags,
            },
            "geometry": mapping(final_geom),
        }
    return None


def load_swisstopo_municipalities(gpkg_path, target_crs="EPSG:2056"):
    """Load municipalities as Polygons to preserve Area Metrics."""
    if not Path(gpkg_path).exists():
        return None

    try:
        gdf = gpd.read_file(gpkg_path, layer="tlm_hoheitsgebiet")
        gdf = gdf[(gdf["objektart"] == "Gemeindegebiet") & (gdf["icc"] == "CH")].copy()

        # Reproject and Force 2D immediately
        gdf = gdf.to_crs(target_crs)
        gdf.geometry = gdf.geometry.apply(force_2d)

        # Ensure geometries are valid for area calculations
        gdf.geometry = gdf.geometry.make_valid()

        return gdf
    except Exception as e:
        print(f"Error loading SwissTopo data: {e}")
        return None


def group_connected_ways(ways):
    """Group ways that connect to each other."""
    if not ways:
        return []

    groups = []
    remaining = list(ways)

    while remaining:
        current_group = [remaining.pop(0)]
        changed = True

        while changed:
            changed = False
            for i in range(len(remaining) - 1, -1, -1):
                way = remaining[i]
                for group_way in current_group:
                    if (
                        way[0] == group_way[0]
                        or way[0] == group_way[-1]
                        or way[-1] == group_way[0]
                        or way[-1] == group_way[-1]
                    ):
                        current_group.append(remaining.pop(i))
                        changed = True
                        break

        groups.append(current_group)

    return groups


def save_boundaries_as_geojson(gdf, output_folder, source_date=None):
    """Saves Polygons as a FeatureCollection of individual LineString segments."""
    os.makedirs(output_folder, exist_ok=True)

    # Ensure we are in WGS84 for GeoJSON standard
    gdf_wgs84 = gdf.to_crs("EPSG:4326")

    for bfs_num, group in gdf_wgs84.groupby("bfs_nummer"):
        features = []

        for _, row in group.iterrows():
            # 1. Get the boundary (this turns Polygon -> LineString/MultiLineString)
            boundary = row.geometry.boundary

            # 2. EXPLOSION LOGIC: Break into individual parts
            # Handles MultiLineStrings (multiple rings/exclaves)
            if hasattr(boundary, "geoms"):
                parts = list(boundary.geoms)
            else:
                parts = [boundary]

            for part in parts:
                # 3. Create a unique feature for every single segment
                # This ensures the GeoJSON is a collection of lines, not one big one
                props = {"source": "swisstopo SWISSBOUNDARIES3D"}
                if source_date:
                    props["source:date"] = source_date
                features.append(
                    {
                        "type": "Feature",
                        "properties": props,
                        "geometry": mapping(part),
                    }
                )

        # 4. Wrap everything in a FeatureCollection
        geojson_output = {"type": "FeatureCollection", "features": features}

        file_path = os.path.join(output_folder, f"{int(bfs_num)}.geojson")
        with open(file_path, "w") as f:
            json.dump(geojson_output, f, indent=2)

    print(
        f"  - Successfully saved {len(gdf_wgs84['bfs_nummer'].unique())} exploded GeoJSON files."
    )


def force_2d(geom):
    """Force geometry to 2D using shapely.ops.transform."""
    from shapely.ops import transform

    if geom is None:
        return None
    return transform(lambda x, y, z=None: (x, y), geom)


def calculate_metrics(geom1, geom2):
    """Calculate comparison metrics in projected coordinates (EPSG:2056)"""
    try:
        # Force to 2D before comparing
        geom1 = force_2d(geom1)
        geom2 = force_2d(geom2)

        # Standardize/Fix Geometries
        if not geom1.is_valid:
            geom1 = geom1.buffer(0)
        if not geom2.is_valid:
            geom2 = geom2.buffer(0)

        if geom1.is_empty or geom2.is_empty:
            return None

        # Area metrics, only relevant for Polygons/MultiPolygons
        if "Polygon" in geom1.geom_type and "Polygon" in geom2.geom_type:
            intersection = geom1.intersection(geom2)
            union = geom1.union(geom2)

            iou = intersection.area / union.area if union.area > 0 else 0
            area_diff = (
                abs(geom1.area - geom2.area) / geom1.area * 100 if geom1.area > 0 else 0
            )
            sym_diff_area = geom1.symmetric_difference(geom2).area
            sym_diff_pct = sym_diff_area / geom1.area * 100 if geom1.area > 0 else 0
        else:  # For Lines, Area metrics are meaningless
            iou = area_diff = sym_diff_pct = float("nan")

        # Distance metrics, helpful for conflation
        try:
            # Round hausdorff to 3 decimals, which is millimeter precision in EPSG:2056 and sufficient for this context
            hausdorff = round(geom1.hausdorff_distance(geom2), 3)
        except:
            hausdorff = float("nan")

        return {
            "iou": iou,
            "area_diff_pct": area_diff,
            "hausdorff_distance": hausdorff,
            "symmetric_diff_pct": sym_diff_pct,
            "swisstopo_area": geom1.area,
            "osm_area": geom2.area,
            "geom_type": geom1.geom_type,
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None


def compare_boundaries(swisstopo_gdf, osm_gdf):
    """Compare matching boundaries"""
    print("Comparing boundaries...")

    results = []
    osm_lookup = {}
    osm_id_lookup = {}
    osm_name_lookup = {}

    for idx, row in osm_gdf.iterrows():
        bfs_num = row.get("swisstopo:BFS_NUMMER")
        if bfs_num:
            osm_lookup[str(bfs_num)] = row.geometry
            osm_id_lookup[str(bfs_num)] = str(row.get("osm_id", ""))
            osm_name_lookup[str(bfs_num)] = row.get("name", "")

    print(f"OSM lookup contains {len(osm_lookup)} municipalities")

    swisstopo_bfs_set = set()
    for idx, row in swisstopo_gdf.iterrows():
        name = row.get("name", row.get("NAME", "Unknown"))
        bfs_num = int(row["bfs_nummer"])
        swisstopo_bfs_set.add(str(bfs_num))
        kantonsnummer = (
            int(row.get("kantonsnummer"))
            if pd.notna(row.get("kantonsnummer"))
            else None
        )
        bezirksnummer = (
            int(row.get("bezirksnummer"))
            if pd.notna(row.get("bezirksnummer"))
            else None
        )

        if str(bfs_num) in osm_lookup:
            metrics = calculate_metrics(row.geometry, osm_lookup[str(bfs_num)])
            if metrics:
                results.append(
                    {
                        "name": name,
                        "bfs_nummer": bfs_num,
                        "kantonsnummer": kantonsnummer,
                        "bezirksnummer": bezirksnummer,
                        "relation": osm_id_lookup[str(bfs_num)],
                        **metrics,
                    }
                )
        else:
            results.append(
                {
                    "name": name,
                    "kantonsnummer": kantonsnummer,
                    "bezirksnummer": bezirksnummer,
                    "bfs_nummer": bfs_num,
                    "relation": "",
                }
            )

    # Find BFS numbers only in OSM (not present in swisstopo)
    # Entries with non-empty relation and NaN iou are OSM-only; entries with
    # empty relation and NaN iou are swisstopo-only (missing in OSM).
    osm_only_bfs = sorted(
        set(osm_lookup.keys()) - swisstopo_bfs_set,
        key=lambda x: int(x) if x.lstrip("-").isdigit() else float("inf"),
    )
    for bfs_num_str in osm_only_bfs:
        results.append(
            {
                "name": osm_name_lookup.get(bfs_num_str, ""),
                "bfs_nummer": (
                    int(bfs_num_str)
                    if bfs_num_str.lstrip("-").isdigit()
                    else bfs_num_str
                ),
                "kantonsnummer": None,
                "bezirksnummer": None,
                "relation": osm_id_lookup.get(bfs_num_str, ""),
            }
        )
    print(f"Found {len(osm_only_bfs)} BFS numbers only in OSM")

    return pd.DataFrame(results)


def compare_dataframes(gdf_swisstopo, gdf_osm):
    """Compare the two GeoDataFrames."""

    print("\n" + "=" * 60)
    print("COMPARISON")
    print("=" * 60)

    print("\nSwissTopo:")
    print(f"  - Features: {len(gdf_swisstopo)}")
    print(f"  - CRS: {gdf_swisstopo.crs}")
    print(f"  - Bounds: {gdf_swisstopo.total_bounds}")

    print("\nOSM:")
    print(f"  - Features: {len(gdf_osm)}")
    print(f"  - CRS: {gdf_osm.crs}")
    print(f"  - Bounds: {gdf_osm.total_bounds}")

    # Check for BFS_NUMMER overlap
    if (
        "bfs_nummer" in gdf_swisstopo.columns
        and "swisstopo:BFS_NUMMER" in gdf_osm.columns
    ):
        swisstopo_bfs = set(gdf_swisstopo["bfs_nummer"].astype(str))
        osm_bfs = set(gdf_osm["swisstopo:BFS_NUMMER"].astype(str))

        common = swisstopo_bfs & osm_bfs
        only_swisstopo = swisstopo_bfs - osm_bfs
        only_osm = osm_bfs - swisstopo_bfs

        print("\nBFS_NUMMER comparison:")
        print(f"  - In both datasets: {len(common)}")
        print(f"  - Only in SwissTopo: {len(only_swisstopo)}")
        print(f"  - Only in OSM: {len(only_osm)}")


def load_historical_data():
    """Load historical comparison data"""
    history_dir = "history"
    if not os.path.exists(history_dir):
        return pd.DataFrame()

    csv_files = sorted(
        [
            f
            for f in os.listdir(history_dir)
            if f.startswith("results_") and f.endswith(".csv")
        ]
    )

    if not csv_files:
        return pd.DataFrame()

    historical_data = []
    for csv_file in csv_files:
        date_str = csv_file.replace("results_", "").replace(".csv", "")
        try:
            df = pd.read_csv(os.path.join(history_dir, csv_file))
            df["date"] = pd.to_datetime(date_str)
            historical_data.append(df)
        except Exception as e:
            print(f"Warning: Could not load {csv_file}: {e}")

    if historical_data:
        return pd.concat(historical_data, ignore_index=True)
    return pd.DataFrame()


def create_trend_visualizations(results_df, historical_df):
    """Create trend charts showing improvements over time"""
    print("Creating trend visualizations...")

    # Add current results to historical data
    current_date = datetime.now()
    current_results = results_df.copy()
    current_results["date"] = current_date

    if len(historical_df) > 0:
        all_data = pd.concat([historical_df, current_results], ignore_index=True)
    else:
        all_data = current_results

    # Calculate summary statistics by date
    summary = (
        all_data.groupby("date")
        .agg(
            {
                "iou": ["mean", "median", "count"],
                "area_diff_pct": "mean",
                "symmetric_diff_pct": "mean",
            }
        )
        .reset_index()
    )

    summary.columns = [
        "date",
        "mean_iou",
        "median_iou",
        "count",
        "mean_area_diff",
        "mean_sym_diff",
    ]

    # Calculate quality distribution over time
    quality_over_time = []
    for date in all_data["date"].unique():
        date_data = all_data[all_data["date"] == date]
        matched = date_data["iou"].notna()
        matched_data = date_data[matched]

        if len(matched_data) > 0:
            quality_over_time.append(
                {
                    "date": date,
                    "Excellent": (matched_data["iou"] >= 0.98).sum(),
                    "Good": (
                        (matched_data["iou"] >= 0.95) & (matched_data["iou"] < 0.98)
                    ).sum(),
                    "Fair": (
                        (matched_data["iou"] >= 0.90) & (matched_data["iou"] < 0.95)
                    ).sum(),
                    "Poor": (matched_data["iou"] < 0.90).sum(),
                    "Missing": (~matched).sum(),
                }
            )

    quality_df = pd.DataFrame(quality_over_time)

    # Create interactive Plotly charts
    if len(summary) > 1:
        # IoU trend chart
        fig_iou = go.Figure()
        fig_iou.add_trace(
            go.Scatter(
                x=summary["date"],
                y=summary["mean_iou"],
                mode="lines+markers",
                name="Mean IoU",
                line=dict(color="#3498db", width=3),
            )
        )
        fig_iou.add_trace(
            go.Scatter(
                x=summary["date"],
                y=summary["median_iou"],
                mode="lines+markers",
                name="Median IoU",
                line=dict(color="#2ecc71", width=3, dash="dash"),
            )
        )
        fig_iou.update_layout(
            title="Boundary Quality Trend (IoU Over Time)",
            xaxis_title="Date",
            yaxis_title="Intersection over Union (IoU)",
            hovermode="x unified",
            template="plotly_white",
            height=500,
        )
        fig_iou.write_html("output/iou_trend.html")

        # Quality distribution stacked area chart
        fig_quality = go.Figure()
        colors = {
            "Excellent": "#2ecc71",
            "Good": "#3498db",
            "Fair": "#f39c12",
            "Poor": "#e74c3c",
            "Missing": "#888888",
        }

        for quality in ["Excellent", "Good", "Fair", "Poor", "Missing"]:
            if quality in quality_df.columns:
                fig_quality.add_trace(
                    go.Scatter(
                        x=quality_df["date"],
                        y=quality_df[quality],
                        mode="lines",
                        name=quality,
                        stackgroup="one",
                        fillcolor=colors[quality],
                        line=dict(width=0.5, color=colors[quality]),
                    )
                )

        fig_quality.update_layout(
            title="Quality Distribution Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Municipalities",
            hovermode="x unified",
            template="plotly_white",
            height=500,
        )
        fig_quality.write_html("output/quality_distribution.html")

        print("Trend visualizations saved")
    else:
        print("Not enough historical data for trends (need at least 2 data points)")


KANTON = {
    1: "ZH",
    2: "BE",
    3: "LU",
    4: "UR",
    5: "SZ",
    6: "OW",
    7: "NW",
    8: "GL",
    9: "ZG",
    10: "FR",
    11: "SO",
    12: "BS",
    13: "BL",
    14: "SH",
    15: "AR",
    16: "AI",
    17: "SG",
    18: "GR",
    19: "AG",
    20: "TG",
    21: "TI",
    22: "VD",
    23: "VS",
    24: "NE",
    25: "GE",
    26: "JU",
}

_CANTON_HEX = [
    "#4e9af1",
    "#f4a036",
    "#56c97a",
    "#e05c5c",
    "#a78bfa",
    "#f472b6",
    "#34d4c8",
    "#facc15",
    "#fb923c",
    "#86efac",
    "#67e8f9",
    "#c084fc",
    "#fda4af",
    "#a3e635",
    "#38bdf8",
    "#e879f9",
    "#4ade80",
    "#fbbf24",
    "#f87171",
    "#60a5fa",
    "#34d399",
    "#e2e8f0",
    "#d946ef",
    "#fb7185",
    "#818cf8",
    "#2dd4bf",
]


def _build_municipality_pivot(df, metric_column):
    """Return bfs_nummer x date pivot for a metric, keeping municipalities present in >=2 snapshots."""
    working = df.copy()
    working[metric_column] = pd.to_numeric(working[metric_column], errors="coerce")
    working = working.dropna(subset=["bfs_nummer", "_date"])

    pivot = working.pivot_table(
        index="bfs_nummer", columns="_date", values=metric_column, aggfunc="first"
    )
    if pivot.empty:
        return pivot

    pivot.columns = pd.to_datetime(pivot.columns)
    pivot = pivot.sort_index(axis=1)
    pivot = pivot[pivot.notna().sum(axis=1) >= 2]
    return pivot


def _attach_names(pivot, df):
    """Map bfs_nummer to latest known municipality name."""
    latest_date = df["_date"].max()
    latest = df[df["_date"] == latest_date].drop_duplicates("bfs_nummer")
    name_map = latest.set_index("bfs_nummer")["name"]
    mapped = pd.Series(pivot.index.map(name_map), index=pivot.index)
    fallback = pd.Series(pivot.index.astype(str), index=pivot.index)
    return mapped.fillna(fallback)


def _attach_canton(pivot, df):
    """Map bfs_nummer to latest known canton abbreviation."""
    latest_date = df["_date"].max()
    latest = df[df["_date"] == latest_date].drop_duplicates("bfs_nummer")
    canton_map = latest.set_index("bfs_nummer")["kantonsnummer"]
    mapped = pd.Series(pivot.index.map(canton_map), index=pivot.index)
    return mapped.map(
        lambda value: KANTON.get(int(value), str(value)) if pd.notna(value) else "?"
    )


def _compute_changes(pivot, min_delta):
    """Compute first/last metric deltas and keep municipalities above threshold."""
    first = pivot.ffill(axis=1).bfill(axis=1).iloc[:, 0]
    last = pivot.ffill(axis=1).bfill(axis=1).iloc[:, -1]
    delta = last - first

    changed = pivot[delta.abs() >= min_delta].copy()
    meta = pd.DataFrame(
        {
            "first_value": first[changed.index],
            "last_value": last[changed.index],
            "net_delta": delta[changed.index],
            "abs_delta": delta[changed.index].abs(),
        }
    )
    return changed, meta


def _build_canton_palette(cantons_dict):
    abbrevs = sorted(set(cantons_dict.values()))
    return {
        canton: _CANTON_HEX[i % len(_CANTON_HEX)] for i, canton in enumerate(abbrevs)
    }


def _hex_to_rgb01(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def _add_plotly_changes_panel(
    fig,
    subset_pivot,
    subset_meta,
    names,
    cantons,
    canton_palette,
    row,
    max_abs,
    legend_cantons_shown,
    metric_label,
    delta_scale=1.0,
    bar_hover_precision=4,
    show_reference_line=False,
    reference_line_value=0.0,
    reference_line_color="#2a5a2a",
):
    scale = max(max_abs, 1e-12)

    for bfs, row_data in subset_meta.iterrows():
        series = subset_pivot.loc[bfs].dropna()
        if len(series) < 2:
            continue

        alpha = 0.20 + 0.75 * (row_data["abs_delta"] / scale) ** 0.5
        canton = cantons.get(bfs, "?")
        hex_color = canton_palette.get(canton, "#aaaaaa")
        red, green, blue = _hex_to_rgb01(hex_color)
        color = (
            f"rgba({int(red * 255)},{int(green * 255)},{int(blue * 255)},{alpha:.2f})"
        )

        municipality_name = names.get(bfs, str(bfs))
        hover = (
            f"<b>{municipality_name}</b> ({canton})<br>"
            f"BFS: {bfs}<br>"
            f"First: {row_data['first_value']:.6f}<br>"
            f"Last:  {row_data['last_value']:.6f}<br>"
            f"Δ {metric_label}: {row_data['net_delta']:+.6f}"
        )

        show_legend = canton not in legend_cantons_shown
        if show_legend:
            legend_cantons_shown.add(canton)

        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines",
                name=canton,
                legendgroup=canton,
                line=dict(color=color, width=1.2),
                hovertemplate=hover + "<extra></extra>",
                showlegend=show_legend,
            ),
            row=row,
            col=1,
        )

    if show_reference_line:
        fig.add_hline(
            y=reference_line_value,
            line_dash="dot",
            line_color=reference_line_color,
            opacity=0.5,
            row=row,
            col=1,
        )

    n_bars = min(40, len(subset_meta))
    top = subset_meta.nlargest(n_bars, "abs_delta").sort_values("net_delta")
    bar_labels = [
        f"{names.get(bfs, str(bfs))} ({cantons.get(bfs, '?')})" for bfs in top.index
    ]
    bar_colors = [
        canton_palette.get(cantons.get(bfs, "?"), "#aaaaaa") for bfs in top.index
    ]

    fig.add_trace(
        go.Bar(
            x=top["net_delta"].values * delta_scale,
            y=bar_labels,
            orientation="h",
            marker_color=bar_colors,
            marker_opacity=0.85,
            hovertemplate=f"%{{y}}: %{{x:.{bar_hover_precision}f}}<extra></extra>",
            showlegend=False,
        ),
        row=row,
        col=2,
    )


def _plot_metric_changes_plotly(metric_results, names, cantons, output_file):
    from plotly.subplots import make_subplots

    names_dict = names.to_dict()
    cantons_dict = cantons.to_dict()
    canton_palette = _build_canton_palette(cantons_dict)

    fig = make_subplots(
        rows=2,
        cols=2,
        column_widths=[0.65, 0.35],
        row_heights=[0.5, 0.5],
        vertical_spacing=0.12,
        subplot_titles=[
            "Increases — trajectories",
            "Top increases",
            "Decreases — trajectories",
            "Top decreases",
        ],
    )

    legend_cantons_shown = set()
    metric_trace_map = {}

    for item in metric_results:
        trace_start = len(fig.data)
        pivot_changed = item["pivot_changed"]
        increases_meta = item["increases_meta"]
        decreases_meta = item["decreases_meta"]

        if len(increases_meta):
            _add_plotly_changes_panel(
                fig,
                pivot_changed.loc[increases_meta.index],
                increases_meta,
                names_dict,
                cantons_dict,
                canton_palette,
                row=1,
                max_abs=item["max_abs"],
                legend_cantons_shown=legend_cantons_shown,
                metric_label=item["label"],
                delta_scale=item["delta_scale"],
                bar_hover_precision=item["bar_hover_precision"],
                show_reference_line=item["show_reference_line"],
                reference_line_value=item["reference_line_value"],
                reference_line_color=item["reference_line_color"],
            )

        if len(decreases_meta):
            _add_plotly_changes_panel(
                fig,
                pivot_changed.loc[decreases_meta.index],
                decreases_meta,
                names_dict,
                cantons_dict,
                canton_palette,
                row=2,
                max_abs=item["max_abs"],
                legend_cantons_shown=legend_cantons_shown,
                metric_label=item["label"],
                delta_scale=item["delta_scale"],
                bar_hover_precision=item["bar_hover_precision"],
                show_reference_line=item["show_reference_line"],
                reference_line_value=item["reference_line_value"],
                reference_line_color=item["reference_line_color"],
            )

        trace_end = len(fig.data)
        metric_trace_map[item["label"]] = list(range(trace_start, trace_end))

    if not metric_trace_map:
        fig.write_html(output_file)
        return

    metric_labels = [
        item["label"] for item in metric_results if item["label"] in metric_trace_map
    ]
    default_label = "IoU" if "IoU" in metric_labels else metric_labels[0]

    for idx, trace in enumerate(fig.data):
        trace.visible = idx in metric_trace_map[default_label]

    buttons = []
    total_traces = len(fig.data)
    for item in metric_results:
        label = item["label"]
        if label not in metric_trace_map:
            continue

        visible = [False] * total_traces
        for index in metric_trace_map[label]:
            visible[index] = True

        increases_count = len(item["increases_meta"])
        decreases_count = len(item["decreases_meta"])

        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {"visible": visible},
                    {
                        "title": f"Per-municipality {label} changes over time (coloured by canton)",
                        "xaxis2.title.text": item["delta_axis_label"],
                        "xaxis4.title.text": item["delta_axis_label"],
                        "yaxis.title.text": label,
                        "yaxis3.title.text": label,
                        "annotations[0].text": f"{label} increases — trajectories ({increases_count:,} municipalities)",
                        "annotations[1].text": f"Top increases ({item['delta_axis_label']})",
                        "annotations[2].text": f"{label} decreases — trajectories ({decreases_count:,} municipalities)",
                        "annotations[3].text": f"Top decreases ({item['delta_axis_label']})",
                    },
                ],
            )
        )

    fig.update_layout(
        title=f"Per-municipality {default_label} changes over time (coloured by canton)",
        hovermode="closest",
        height=900,
        legend=dict(
            title="Canton",
            tracegroupgap=2,
        ),
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=0.5,
                y=1.15,
                xanchor="center",
                yanchor="top",
            )
        ],
    )

    for row in (1, 2):
        for col in (1, 2):
            fig.update_xaxes(showgrid=True, zeroline=False, row=row, col=col)
            fig.update_yaxes(showgrid=True, zeroline=False, row=row, col=col)

        fig.update_xaxes(title_text="Snapshot date", row=row, col=1)

    default_item = next(
        item for item in metric_results if item["label"] == default_label
    )
    fig.update_xaxes(
        title_text=default_item["delta_axis_label"],
        zerolinewidth=1,
        row=1,
        col=2,
    )
    fig.update_xaxes(
        title_text=default_item["delta_axis_label"],
        zerolinewidth=1,
        row=2,
        col=2,
    )
    fig.update_yaxes(title_text=default_label, row=1, col=1)
    fig.update_yaxes(title_text=default_label, row=2, col=1)

    fig.write_html(output_file)


def _get_metric_specs():
    return [
        {
            "column": "iou",
            "label": "IoU",
            "min_delta": 0.0001,
            "delta_scale": 100.0,
            "delta_axis_label": "Net Δ IoU (×100)",
            "bar_hover_precision": 4,
            "show_reference_line": True,
            "reference_line_value": 1.0,
            "reference_line_color": "#2a5a2a",
        },
        {
            "column": "area_diff_pct",
            "label": "Area Diff [%]",
            "min_delta": 0.01,
            "delta_scale": 1.0,
            "delta_axis_label": "Net Δ Area Diff [%]",
            "bar_hover_precision": 3,
            "show_reference_line": False,
            "reference_line_value": 0.0,
            "reference_line_color": "#444444",
        },
        {
            "column": "symmetric_diff_pct",
            "label": "Symmetric Diff [%]",
            "min_delta": 0.01,
            "delta_scale": 1.0,
            "delta_axis_label": "Net Δ Symmetric Diff [%]",
            "bar_hover_precision": 3,
            "show_reference_line": False,
            "reference_line_value": 0.0,
            "reference_line_color": "#444444",
        },
        {
            "column": "hausdorff_distance",
            "label": "Hausdorff Distance [m]",
            "min_delta": 0.1,
            "delta_scale": 1.0,
            "delta_axis_label": "Net Δ Hausdorff Distance [m]",
            "bar_hover_precision": 3,
            "show_reference_line": False,
            "reference_line_value": 0.0,
            "reference_line_color": "#444444",
        },
        {
            "column": "swisstopo_area",
            "label": "Area swisstopo [m²]",
            "min_delta": 1.0,
            "delta_scale": 1.0,
            "delta_axis_label": "Net Δ Area swisstopo [m²]",
            "bar_hover_precision": 1,
            "show_reference_line": False,
            "reference_line_value": 0.0,
            "reference_line_color": "#444444",
        },
    ]


def create_iou_changes_plot(min_delta=0.0001):
    """Create detailed per-municipality metric changes plot in output/iou_changes.html."""
    print("Creating metric changes plot...")

    metric_specs = _get_metric_specs()
    metric_specs[0]["min_delta"] = min_delta

    try:
        df = load_historical_data().copy()
        if df.empty:
            print("No historical data found for metric changes plot")
            return False

        df["_date"] = pd.to_datetime(df["date"])
        metric_results = []
        names = None
        cantons = None

        for spec in metric_specs:
            column = spec["column"]
            if column not in df.columns:
                continue

            pivot = _build_municipality_pivot(df, column)
            if pivot.empty:
                continue

            if names is None:
                names = _attach_names(pivot, df)
                cantons = _attach_canton(pivot, df)

            pivot_changed, meta = _compute_changes(pivot, spec["min_delta"])
            if pivot_changed.empty:
                continue

            metric_results.append(
                {
                    "label": spec["label"],
                    "delta_scale": spec["delta_scale"],
                    "delta_axis_label": spec["delta_axis_label"],
                    "bar_hover_precision": spec["bar_hover_precision"],
                    "show_reference_line": spec["show_reference_line"],
                    "reference_line_value": spec["reference_line_value"],
                    "reference_line_color": spec["reference_line_color"],
                    "pivot_changed": pivot_changed,
                    "increases_meta": meta[meta["net_delta"] > 0],
                    "decreases_meta": meta[meta["net_delta"] < 0],
                    "max_abs": max(meta["abs_delta"].max(), 1e-12),
                }
            )

        if not metric_results:
            print("Not enough historical metric changes to plot")
            return False

        _plot_metric_changes_plotly(
            metric_results, names, cantons, "output/iou_changes.html"
        )
        print("Metric changes plot saved")
        return True
    except SystemExit as e:
        print(f"Skipping metric changes plot: {e}")
        return False
    except Exception as e:
        print(f"Warning: Failed to generate metric changes plot: {e}")
        return False


def generate_report(results_df, historical_df):
    """Generate comparison report"""
    report_lines = []
    report_lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    # Classify result rows by how they were populated in compare_boundaries:
    #   - matched:          iou is not NaN (comparison succeeded)
    #   - swisstopo-only:   relation == "" and iou is NaN (no OSM counterpart)
    #   - OSM-only:         relation != "" and iou is NaN (no swisstopo counterpart)
    matched_df = results_df[results_df["iou"].notna()]
    only_swisstopo_df = results_df[
        (results_df["relation"] == "") & results_df["iou"].isna()
    ]
    only_osm_df = results_df[
        (results_df["relation"] != "") & results_df["iou"].isna()
    ]
    matched = len(matched_df)
    missing = len(only_swisstopo_df)
    total = matched + missing

    report_lines.append("\n## Dataset Overview")
    report_lines.append("\n| Metric | Value |")
    report_lines.append("|--------|-------|")
    report_lines.append(f"| Total Swisstopo municipalities | {total} |")
    report_lines.append(f"| Matched in OSM | {matched} ({matched/total*100:.1f}%) |")
    report_lines.append(f"| Missing in OSM | {missing} ({missing/total*100:.1f}%) |")
    report_lines.append(f"|  Only in OSM (not in Swisstopo) | {len(only_osm_df)}")

    if matched > 0:
        report_lines.append("\n## Accuracy Metrics (for matched municipalities)")
        report_lines.append("\n| Metric | Value |")
        report_lines.append("|--------|-------|")
        report_lines.append(f"| Mean IoU | {matched_df['iou'].mean():.4f} |")
        report_lines.append(f"| Median IoU | {matched_df['iou'].median():.4f} |")
        report_lines.append(
            f"| Mean area difference | {matched_df['area_diff_pct'].mean():.2f}% |"
        )
        report_lines.append(
            f"| Mean symmetric difference | {matched_df['symmetric_diff_pct'].mean():.2f}% |"
        )
        report_lines.append(
            f"| Mean Hausdorff distance | {matched_df['hausdorff_distance'].mean():.3f} m |"
        )

        excellent = (matched_df["iou"] >= 0.98).sum()
        good = ((matched_df["iou"] >= 0.95) & (matched_df["iou"] < 0.98)).sum()
        fair = ((matched_df["iou"] >= 0.90) & (matched_df["iou"] < 0.95)).sum()
        poor = (matched_df["iou"] < 0.90).sum()

        report_lines.append("\n## Quality Distribution")
        report_lines.append("\n| Quality | Count | Percentage |")
        report_lines.append("|---------|-------|------------|")
        report_lines.append(
            f"| Excellent (IoU ≥ 0.98) | {excellent} | {excellent/matched*100:.1f}% |"
        )
        report_lines.append(
            f"| Good (IoU ≥ 0.95) | {good} | {good/matched*100:.1f}% |"
        )
        report_lines.append(
            f"| Fair (IoU ≥ 0.90) | {fair} | {fair/matched*100:.1f}% |"
        )
        report_lines.append(
            f"| Poor (IoU < 0.90) | {poor} | {poor/matched*100:.1f}% |"
        )

        # Historical comparison
        if len(historical_df) > 0:
            prev_date = historical_df["date"].max()
            prev_data = historical_df[historical_df["date"] == prev_date]
            prev_matched = prev_data["iou"].notna()

            if prev_matched.sum() > 0:
                prev_mean_iou = prev_data[prev_matched]["iou"].mean()
                current_mean_iou = matched_df["iou"].mean()
                iou_change = current_mean_iou - prev_mean_iou

                report_lines.append(
                    f"\n## Historical Comparison (vs {prev_date.strftime('%Y-%m-%d')})"
                )
                report_lines.append("\n| Metric | Value |")
                report_lines.append("|--------|-------|")
                report_lines.append(f"| Previous mean IoU | {prev_mean_iou:.4f} |")
                report_lines.append(f"| Current mean IoU | {current_mean_iou:.4f} |")
                report_lines.append(
                    f"| Change | {iou_change:+.4f} ({iou_change/prev_mean_iou*100:+.2f}%) |"
                )

        report_lines.append("\n## Worst 10 Matches (by IoU)")
        worst = matched_df.nsmallest(10, "iou")[
            ["name", "bfs_nummer", "iou", "area_diff_pct"]
        ]
        report_lines.append("\n" + worst.to_markdown(index=False))

        report_lines.append("\n## Most Improved (if historical data available)")
        if len(historical_df) > 0:
            # Find municipalities that improved
            prev_date = historical_df["date"].max()
            prev_data = historical_df[historical_df["date"] == prev_date].set_index(
                "bfs_nummer"
            )

            improvements = []
            for idx, row in matched_df.iterrows():
                bfs = row["bfs_nummer"]
                if bfs in prev_data.index and pd.notna(prev_data.loc[bfs, "iou"]):
                    prev_iou = prev_data.loc[bfs, "iou"]
                    curr_iou = row["iou"]
                    improvement = curr_iou - prev_iou
                    if improvement > 0.001:  # Significant improvement
                        improvements.append(
                            {
                                "name": row["name"],
                                "bfs_nummer": bfs,
                                "prev_iou": prev_iou,
                                "curr_iou": curr_iou,
                                "improvement": improvement,
                            }
                        )

            if improvements:
                imp_df = pd.DataFrame(improvements).nlargest(10, "improvement")
                report_lines.append("\n" + imp_df.to_markdown(index=False))
            else:
                report_lines.append("\nNo significant improvements detected.")
        else:
            report_lines.append("\n_(Insufficient historical data)_")

    # BFS numbers only in Swisstopo (missing in OSM)
    if len(only_swisstopo_df) > 0:
        report_lines.append(
            "\n## BFS numbers only in Swisstopo (missing in OSM) (showing first 20):"
        )
        swisstopo_only_list = only_swisstopo_df.head(20)[["name", "bfs_nummer"]]
        report_lines.append(swisstopo_only_list.to_string(index=False))

    # BFS numbers only in OSM (not in Swisstopo)
    if len(only_osm_df) > 0:
        report_lines.append(
            "\n## BFS numbers only in OSM (not in Swisstopo) (showing first 20):"
        )
        osm_only_list = only_osm_df.head(20)[["name", "bfs_nummer", "relation"]]
        report_lines.append("\n" + osm_only_list.to_markdown(index=False))

    report_text = "\n".join(report_lines)
    print(report_text)

    # Save reports
    with open("output/comparison_report.md", "w") as f:
        f.write(report_text)

    # Save CSV (without geometry columns for CSV)
    csv_df = results_df.drop(columns=["geometry", "osm_geometry"], errors="ignore")

    # Convert bfs_nummer, kantonsnummer, and bezirksnummer to integer
    csv_df["bfs_nummer"] = csv_df["bfs_nummer"].astype(
        "Int64"
    )  # Int64 handles NaN values
    csv_df["kantonsnummer"] = csv_df["kantonsnummer"].astype("Int64")
    csv_df["bezirksnummer"] = csv_df["bezirksnummer"].astype("Int64")

    # Reorder columns
    column_order = [
        "name",
        "relation",
        "bfs_nummer",
        "bezirksnummer",
        "kantonsnummer",
        "iou",
        "area_diff_pct",
        "hausdorff_distance",
        "symmetric_diff_pct",
        "swisstopo_area",
        "osm_area",
        "geom_type",
    ]
    csv_df = csv_df[[col for col in column_order if col in csv_df.columns]]

    csv_df.to_csv(
        "output/detailed_results.csv",
        header=[
            "Name",
            "OSM Relation",
            "BFS Number",
            "Bezirksnummer",
            "Kantonsnummer",
            "IoU",
            "Area Diff [%]",
            "Hausdorff Distance [m]",
            "Symmetric Diff [%]",
            "Area swisstopo [m²]",
            "Area OSM [m²]",
            "Geometry Type",
        ],
        index=False,
    )

    # Save to history
    timestamp = datetime.now().strftime("%Y%m%d")
    csv_df.to_csv(f"history/results_{timestamp}.csv", index=False)

    return results_df


def create_map_visualization(results_df, swisstopo_gdf):
    """Create an interactive Leaflet map of municipality IoU quality on an OSM background."""
    print("Creating map visualization...")

    try:
        # Reproject to WGS84 and compute a representative point that lies within each polygon
        gdf_wgs84 = swisstopo_gdf.to_crs("EPSG:4326").copy()
        gdf_wgs84["_point"] = gdf_wgs84.geometry.representative_point()

        # Build a lookup from bfs_nummer → result row (drop duplicates defensively)
        results_indexed = (
            results_df.drop_duplicates("bfs_nummer").set_index("bfs_nummer")
        )

        features = []
        for _, row in gdf_wgs84.iterrows():
            bfs = int(row["bfs_nummer"])
            point = row["_point"]
            name = row.get("name", row.get("NAME", str(bfs)))

            props = {"name": name, "bfs_nummer": bfs}

            if bfs in results_indexed.index:
                r = results_indexed.loc[bfs]
                props["iou"] = (
                    float(r["iou"]) if pd.notna(r.get("iou")) else None
                )
                props["relation"] = str(r.get("relation", ""))
                props["area_diff_pct"] = (
                    float(r["area_diff_pct"])
                    if pd.notna(r.get("area_diff_pct"))
                    else None
                )
                props["hausdorff_distance"] = (
                    float(r["hausdorff_distance"])
                    if pd.notna(r.get("hausdorff_distance"))
                    else None
                )
                props["symmetric_diff_pct"] = (
                    float(r["symmetric_diff_pct"])
                    if pd.notna(r.get("symmetric_diff_pct"))
                    else None
                )
            else:
                props["iou"] = None
                props["relation"] = ""

            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [point.x, point.y],
                    },
                    "properties": props,
                }
            )

        geojson_data = json.dumps(
            {"type": "FeatureCollection", "features": features}
        )

        # Determine the actual IoU range for a bandwidth-scaled color ramp
        iou_values = [
            f["properties"]["iou"]
            for f in features
            if f["properties"]["iou"] is not None
        ]
        iou_min = min(iou_values) if iou_values else 0.0
        iou_max = max(iou_values) if iou_values else 1.0
        # Round to 4 decimal places for display in the legend
        legend_min = round(iou_min, 4)
        legend_max = round(iou_max, 4)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Swiss Municipality Boundary Quality Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        html, body {{ height: 100%; margin: 0; padding: 0; }}
        #map {{ height: 100%; width: 100%; }}
        .legend {{
            background: white;
            padding: 10px 14px;
            border-radius: 6px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            line-height: 1.6;
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        .legend h4 {{ margin: 0 0 6px 0; font-size: 14px; }}
        .legend-gradient {{
            width: 160px;
            height: 14px;
            background: linear-gradient(to right, hsl(0,80%,45%), hsl(60,80%,45%), hsl(120,80%,45%));
            border: 1px solid #aaa;
            border-radius: 3px;
            margin-bottom: 2px;
        }}
        .legend-labels {{
            display: flex;
            justify-content: space-between;
            width: 160px;
            font-size: 11px;
            color: #555;
        }}
        .legend-missing {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 6px;
            font-size: 12px;
        }}
        .legend-missing-dot {{
            width: 12px; height: 12px;
            background: #888888;
            border-radius: 50%;
            border: 1px solid #555;
            flex-shrink: 0;
        }}
    </style>
</head>
<body>
<div id="map"></div>
<script>
    var data = {geojson_data};
    var ioUMin = {iou_min};
    var ioUMax = {iou_max};

    var map = L.map('map').setView([46.82, 8.22], 8);

    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }}).addTo(map);

    function iouToColor(iou) {{
        if (iou === null || iou === undefined || isNaN(iou)) {{
            return '#888888';
        }}
        // Map the actual data bandwidth (ioUMin..ioUMax) to hue 0° (red) .. 120° (green)
        var range = ioUMax - ioUMin;
        var t = range > 0 ? Math.min(1, Math.max(0, (iou - ioUMin) / range)) : 1;
        var hue = Math.round(t * 120);
        return 'hsl(' + hue + ',80%,40%)';
    }}

    L.geoJSON(data, {{
        pointToLayer: function(feature, latlng) {{
            var iou = feature.properties.iou;
            return L.circleMarker(latlng, {{
                radius: 5,
                fillColor: iouToColor(iou),
                color: '#222',
                weight: 0.6,
                opacity: 0.9,
                fillOpacity: 0.85
            }});
        }},
        onEachFeature: function(feature, layer) {{
            var p = feature.properties;
            var iouText = (p.iou !== null && p.iou !== undefined) ? p.iou.toFixed(6) : 'N/A (not in OSM)';
            var areaDiffText = (p.area_diff_pct !== null && p.area_diff_pct !== undefined) ? p.area_diff_pct.toFixed(4) + '%' : '—';
            var hausdorffText = (p.hausdorff_distance !== null && p.hausdorff_distance !== undefined) ? p.hausdorff_distance.toFixed(3) + ' m' : '—';
            var symDiffText = (p.symmetric_diff_pct !== null && p.symmetric_diff_pct !== undefined) ? p.symmetric_diff_pct.toFixed(4) + '%' : '—';
            var osmLink = p.relation ? '<a href="https://osm.org/relation/' + p.relation + '" target="_blank">relation/' + p.relation + '</a>' : '—';
            layer.bindPopup(
                '<b>' + p.name + '</b> (BFS ' + p.bfs_nummer + ')<br>' +
                'OSM: ' + osmLink + '<br>' +
                'IoU: <b>' + iouText + '</b><br>' +
                'Area diff: ' + areaDiffText + '<br>' +
                'Hausdorff: ' + hausdorffText + '<br>' +
                'Symmetric diff: ' + symDiffText
            );
            layer.on('mouseover', function() {{ this.openPopup(); }});
            layer.on('mouseout', function() {{ this.closePopup(); }});
            layer.on('click', function() {{ this.openPopup(); }});
        }}
    }}).addTo(map);

    // Legend
    var legend = L.control({{position: 'bottomright'}});
    legend.onAdd = function() {{
        var div = L.DomUtil.create('div', 'legend');
        div.innerHTML =
            '<h4>IoU Quality</h4>' +
            '<div class="legend-gradient"></div>' +
            '<div class="legend-labels">' +
            '  <span>Worse<br>({legend_min})</span>' +
            '  <span style="text-align:right">Better<br>({legend_max})</span>' +
            '</div>' +
            '<div class="legend-missing">' +
            '  <div class="legend-missing-dot"></div>' +
            '  <span>Not matched in OSM</span>' +
            '</div>';
        return div;
    }};
    legend.addTo(map);
</script>
</body>
</html>"""

        with open("output/map.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("Map visualization saved to output/map.html")
    except Exception as e:
        print(f"Warning: Failed to create map visualization: {e}")


def create_index_page():
    """Create HTML to display CSV table"""
    readme_text = ""
    readme_path = Path("README.md")
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_text = f.read()

    readme_section = ""
    if readme_text:
        readme_json = json.dumps(readme_text)
        readme_section = f"""
    <section class=\"framed-section\">
        <div id=\"readme-content\"></div>
        <script>
            (function() {{
                const readmeMarkdown = {readme_json};
                const target = document.getElementById('readme-content');
                if (!target) return;
                if (window.marked) {{
                    target.innerHTML = marked.parse(readmeMarkdown);
                }} else {{
                    target.textContent = readmeMarkdown;
                }}
            }})();
        </script>
    </section>"""

    changes_plot_section = ""
    changes_plot_path = Path("output/iou_changes.html")
    if changes_plot_path.exists():
        changes_plot_section = """
    <section class=\"framed-section\" id=\"changes-plot\">
        <h3>Metric Changes Over Time</h3>
        <iframe src=\"iou_changes.html\" title=\"Metric changes plot\"></iframe>
    </section>"""

    map_section = ""
    map_path = Path("output/map.html")
    if map_path.exists():
        map_section = """
    <section class=\"framed-section\" id=\"quality-map\">
        <h3>Municipality Quality Map</h3>
        <iframe src=\"map.html\" title=\"Municipality quality map\" style=\"width:100%;height:600px;border:0;\"></iframe>
    </section>"""

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>swissBOUNDARIES3D <-> OpenStreetMap</title>
    <link href="https://unpkg.com/tabulator-tables@5.5.0/dist/css/tabulator.min.css" rel="stylesheet">
    <script src="https://unpkg.com/tabulator-tables@5.5.0/dist/js/tabulator.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.20/jspdf.plugin.autotable.min.js"></script>

    <style>
        body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f4f4f9; }
        .controls { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 15px; 
            gap: 10px;
            flex-wrap: wrap;
        }
        .search-container { flex-grow: 1; }
        #search-input { 
            padding: 8px; width: 100%; max-width: 400px; 
            border: 1px solid #ccc; border-radius: 4px; 
        }
        button { 
            padding: 8px 15px; cursor: pointer; 
            background: #007bff; color: white; border: none; border-radius: 4px;
        }
        button:hover { background: #0056b3; }
        #csv-table { border: 1px solid #333; border-radius: 4px; background: white; }
        .framed-section {
            margin-top: 20px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 15px;
        }
        #changes-plot iframe {
            width: 100%;
            height: 980px;
            border: 0;
        }
    </style>
</head>
<body>

    <h2><a href="https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d">swissBOUNDARIES3D</a> <-> <a href="https://overpass-turbo.eu/s/2jcH">OpenStreetMap</a></h2>
    
    <p>
        Comparison of Swiss municipality boundaries between official Swisstopo data (<a href="https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d">swissBOUNDARIES3D</a>) and <a href="https://www.openstreetmap.org/#map=9/46.823/7.880">OpenStreetMap</a>.<br>
        The table below shows the latest comparison results for each municipality, including metrics like IoU, area difference, Hausdorff distance, and more.<br>
        You can search, sort, and download the data in various formats.<br>
        For detailed explanations of the metrics and methodology, please refer to the README section below, which is directly pulled from <a href="https://github.com/habi/swissboundaries">the code repository</a>.<br>
        The bottom of the page shows a plot of the calculated metrics over time.
    </p>

    <div class="controls">
        <div class="search-container">
            <input type="text" id="search-input" placeholder="Search all columns...">
        </div>
        <div class="button-group">
            <button id="download-csv">CSV</button>
            <button id="download-json">JSON</button>
            <button id="download-pdf">PDF</button>
        </div>
    </div>

    <div id="csv-table"></div>

    __README_SECTION__
    __MAP_SECTION__
    __CHANGES_PLOT_SECTION__

    <script>
        var table;

        Papa.parse("detailed_results.csv", {
            download: true,
            header: true,
            complete: function(results) {
                table = new Tabulator("#csv-table", {
                    data: results.data,
                    layout: "fitColumns",
                    height: "600px",
                    renderVertical: "virtual",
                    pagination: false,
                    columns: [
                        {title: "Name", field: "Name"},
                        {
                            title: "OSM Relation", 
                            field: "OSM Relation", 
                            formatter: function(cell, formatterParams, onRendered) {
                                var value = cell.getValue();
                                if (value && value !== '' && value !== 'Not found in OSM') {
                                    return '<a href="https://osm.org/relation/' + value + '" target="_blank">' + value + '</a>';
                                } else if (value === '') {
                                    return 'Not found in OSM';
                                }
                                return value;
                            }
                        },
                        {
                            title: "BFS Number", 
                            field: "BFS Number", 
                            formatter: function(cell, formatterParams, onRendered) {
                                var value = cell.getValue();
                                if (value) {
                                    return '<a href="https://raw.githubusercontent.com/habi/swissboundaries/refs/heads/main/output/swisstopo_geojson/' + value + '.geojson" target="_blank">' + value + '</a>';
                                }
                                return value;
                            }
                        },
                        {title: "Bezirksnummer", field: "Bezirksnummer"},
                        {
                            title: "Kantonsnummer", 
                            field: "Kantonsnummer", 
                            formatter: function(cell, formatterParams, onRendered) {
                                var value = cell.getValue();
                                if (value) {
                                    return '<a href="https://wiki.openstreetmap.org/wiki/Key:swisstopo:KANTONSNUM#' + value + '" target="_blank">' + value + '</a>';
                                }
                                return value;
                            }
                        },
                        {title: "IoU", field: "IoU", formatter: "money", formatterParams: {precision: 4}},   
                        {
                            title: "Area Diff [%]",
                            field: "Area Diff [%]",
                            sorter: function(a, b) {
                                var aNum = parseFloat(a);
                                var bNum = parseFloat(b);

                                var aIsNum = !isNaN(aNum);
                                var bIsNum = !isNaN(bNum);

                                if (!aIsNum && !bIsNum) return 0;
                                if (!aIsNum) return 1;
                                if (!bIsNum) return -1;

                                return aNum - bNum;
                            },
                            formatter: "money",
                            formatterParams: {precision: 2}
                        },
                        {title: "Hausdorff Distance [m]", field: "Hausdorff Distance [m]"},
                        {title: "Symmetric Diff [%]", field: "Symmetric Diff [%]", formatter: "money", formatterParams: {precision: 2}},
                        {title: "Area swisstopo [m²]", field: "Area swisstopo [m²]", formatter: "money", formatterParams: {precision: 0}},
                        {title: "Area OSM [m²]", field: "Area OSM [m²]", formatter: "money", formatterParams: {precision: 0}},
                    ],
                });

                // SEARCH LOGIC
                // Define a custom filter function that checks all columns
                function customFilter(data, filterParams){
                    var searchValue = filterParams.value.toLowerCase();
                    var match = false;

                    for(var key in data){
                        if(String(data[key]).toLowerCase().includes(searchValue)){
                            match = true;
                        }
                    }
                    return match;
                }

                // Trigger filter on input
                document.getElementById("search-input").addEventListener("keyup", function(e){
                    table.setFilter(customFilter, {value: e.target.value});
                    if(!e.target.value){
                        table.clearFilter();
                    }
                });
            }
        });

        // DOWNLOADS
        document.getElementById("download-csv").addEventListener("click", () => table.download("csv", "export.csv"));
        document.getElementById("download-json").addEventListener("click", () => table.download("json", "export.json"));
        document.getElementById("download-pdf").addEventListener("click", () => table.download("pdf", "export.pdf"));
    </script>
</body>
</html>"""

    html_content = html_content.replace("__README_SECTION__", readme_section)
    html_content = html_content.replace("__MAP_SECTION__", map_section)
    html_content = html_content.replace(
        "__CHANGES_PLOT_SECTION__", changes_plot_section
    )

    with open("output/index.html", "w") as f:
        f.write(html_content)

    print("CSV table page created")


# Main execution
if __name__ == "__main__":
    # Create necessary directories
    for dir_name in ["history", "output"]:
        os.makedirs(dir_name, exist_ok=True)

    # Load data
    gpkg_file = "swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
    target_crs = "EPSG:2056"  # https://epsg.io/2056
    swisstopo = load_swisstopo_municipalities(gpkg_file, target_crs)
    osm = load_osm_boundaries(target_crs)

    # Compare if both loaded successfully
    if swisstopo is not None and osm is not None:
        compare_dataframes(swisstopo, osm)

    # Save out swisstopo boundaries as individual geoJSON files
    if swisstopo is not None:
        swisstopo_date = os.environ.get("SWISSTOPO_DATE", None)
        save_boundaries_as_geojson(swisstopo, "output/swisstopo_geojson", source_date=swisstopo_date)

    if swisstopo is not None and osm is not None and len(osm) > 0:
        # Compare boundaries
        results = compare_boundaries(swisstopo, osm)

        # Load historical data
        historical = load_historical_data()

        # Generate report
        report = generate_report(results, historical)
        create_trend_visualizations(results, historical)
        create_iou_changes_plot()
        create_map_visualization(results, swisstopo)

        # Create inde page for display
        create_index_page()

        print("\nComparison complete!")
    else:
        if swisstopo is None:
            print("ERROR: Failed to load SwissTopo data")
        if osm is None or len(osm) == 0:
            print("ERROR: Failed to retrieve OSM data")
        exit(1)
