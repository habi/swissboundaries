import geopandas as gpd
import pandas as pd
import requests
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, UTC
from pathlib import Path
from shapely.geometry import mapping, MultiLineString, LineString, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import polygonize, unary_union, transform
from pyproj import Transformer
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OVERPASS_CACHE_PATH = Path("output/overpass_cache.json")
OVERPASS_CACHE_TTL_SECONDS = 4 * 60 * 60
BFS_REMOVALS_PATH = Path("output/bfs_removals.json")
IOU_DETERIORATION_THRESHOLD = 0.001
AREA_DIFF_DETERIORATION_THRESHOLD_PCT_POINTS = 0.001
HAUSDORFF_DETERIORATION_THRESHOLD_M = 1.0
BOUNDARY_DIFF_MAP_ZOOM = 16
LV95_TO_WGS84 = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)
OSM_API_BASE_URL = "https://api.openstreetmap.org/api/0.6"


def normalize_relation_id(value):
    relation_num = pd.to_numeric(value, errors="coerce")
    return str(int(relation_num)) if pd.notna(relation_num) else ""


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


def load_bfs_removal_tracker(path=BFS_REMOVALS_PATH):
    """Load the persistent BFS removal tracker from disk.

    Returns a dict keyed by BFS number (as string) with removal metadata.
    """
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {str(k): v for k, v in data.items()}
    except Exception as e:
        print(f"Warning: Could not load BFS removal tracker: {e}")
        return {}


def save_bfs_removal_tracker(tracker, path=BFS_REMOVALS_PATH):
    """Save the persistent BFS removal tracker to disk."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tracker, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save BFS removal tracker: {e}")


def load_osm_boundaries(target_crs="EPSG:2056"):
    """
    Query Overpass API for Swiss and Liechtenstein admin boundaries.

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
    area["ISO3166-1"="LI"][admin_level=2]->.liechtenstein;
    (
      relation["boundary"="administrative"]["admin_level"="8"]["type"!="historic"]["ref:FR:SIREN"!~".*"]["ref:at:gkz"!~".*"]["de:amtlicher_gemeindeschluessel"!~".*"]["ref:ISTAT"!~".*"](area.switzerland);
      relation["boundary"="administrative"]["admin_level"="8"]["type"!="historic"]["ref:at:gkz"!~".*"](area.liechtenstein);
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
            print(
                "  - No boundaries found with either `swisstopo:BFS_NUMMER` or `bfs:OBJECTVAL` tags"
            )
            return None

        print(f"  - Found {len(osm_data['elements'])} OSM elements")

        # Convert to GeoJSON and count which BFS source tag was used.
        bfs_tag_stats = {"swisstopo:BFS_NUMMER": 0, "bfs:OBJECTVAL": 0}
        geojson = osm_to_geojson(osm_data, bfs_tag_stats=bfs_tag_stats)
        print(
            "  - BFS tag normalization: "
            f"swisstopo:BFS_NUMMER={bfs_tag_stats['swisstopo:BFS_NUMMER']}, "
            f"bfs:OBJECTVAL={bfs_tag_stats['bfs:OBJECTVAL']}"
        )

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


def osm_to_geojson(osm_data, bfs_tag_stats=None):
    """Convert OSM JSON format to GeoJSON."""

    geojson = {"type": "FeatureCollection", "features": []}

    for element in osm_data.get("elements", []):
        feature = create_feature(element, bfs_tag_stats=bfs_tag_stats)
        if feature:
            geojson["features"].append(feature)

    return geojson


def create_feature(element, bfs_tag_stats=None):
    """Convert OSM element to Polygon/MultiPolygon for Area Metrics."""
    e_type = element.get("type")
    tags = element.get("tags", {})

    raw_swisstopo_bfs = tags.get("swisstopo:BFS_NUMMER")
    raw_objectval_bfs = tags.get("bfs:OBJECTVAL")

    swisstopo_bfs = (
        str(raw_swisstopo_bfs).strip() if raw_swisstopo_bfs is not None else ""
    )
    objectval_bfs = (
        str(raw_objectval_bfs).strip() if raw_objectval_bfs is not None else ""
    )

    # CH uses swisstopo:BFS_NUMMER, LI uses bfs:OBJECTVAL; normalize to one key.
    if swisstopo_bfs:
        bfs_num = swisstopo_bfs
        bfs_source = "swisstopo:BFS_NUMMER"
    elif objectval_bfs:
        bfs_num = objectval_bfs
        bfs_source = "bfs:OBJECTVAL"
    else:
        bfs_num = None
        bfs_source = None

    if e_type == "relation":
        outer_lines = []
        inner_lines = []
        all_lines = []

        for member in element.get("members", []):
            if member.get("type") == "way" and member.get("geometry"):
                coords = [
                    (pt["lon"], pt["lat"])
                    for pt in member["geometry"]
                    if pt is not None
                ]
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

        if bfs_tag_stats is not None:
            if bfs_source == "swisstopo:BFS_NUMMER":
                bfs_tag_stats["swisstopo:BFS_NUMMER"] = (
                    bfs_tag_stats.get("swisstopo:BFS_NUMMER", 0) + 1
                )
            elif bfs_source == "bfs:OBJECTVAL":
                bfs_tag_stats["bfs:OBJECTVAL"] = (
                    bfs_tag_stats.get("bfs:OBJECTVAL", 0) + 1
                )

        return {
            "type": "Feature",
            "id": f"relation/{element['id']}",
            "properties": {
                "osm_id": element["id"],
                "country": "LI" if bfs_source == "bfs:OBJECTVAL" else "CH",
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
        gdf = gdf[(gdf["objektart"] == "Gemeindegebiet")].copy()

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
    osm_country_lookup = {}

    for idx, row in osm_gdf.iterrows():
        bfs_num = row.get("swisstopo:BFS_NUMMER")
        if pd.notna(bfs_num) and bfs_num:
            bfs_num_str = str(bfs_num)
            osm_lookup[bfs_num_str] = row.geometry
            osm_id_lookup[bfs_num_str] = str(row.get("osm_id", ""))
            osm_name_lookup[bfs_num_str] = row.get("name", "")
            country = row.get("country", "")
            osm_country_lookup[bfs_num_str] = country if pd.notna(country) else ""

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
                        "country": osm_country_lookup.get(str(bfs_num), "CH") or "CH",
                        "bfs_nummer": bfs_num,
                        "kantonsnummer": kantonsnummer,
                        "bezirksnummer": bezirksnummer,
                        "relation": osm_id_lookup[str(bfs_num)],
                        "geometry": row.geometry,
                        "osm_geometry": osm_lookup[str(bfs_num)],
                        **metrics,
                    }
                )
        else:
            results.append(
                {
                    "name": name,
                    "country": "CH",
                    "kantonsnummer": kantonsnummer,
                    "bezirksnummer": bezirksnummer,
                    "bfs_nummer": bfs_num,
                    "relation": "",
                    "geometry": row.geometry,
                    "osm_geometry": None,
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
                "country": osm_country_lookup.get(bfs_num_str, "") or "LI",
                "bfs_nummer": (
                    int(bfs_num_str)
                    if bfs_num_str.lstrip("-").isdigit()
                    else bfs_num_str
                ),
                "kantonsnummer": None,
                "bezirksnummer": None,
                "relation": osm_id_lookup.get(bfs_num_str, ""),
                "geometry": None,
                "osm_geometry": osm_lookup.get(bfs_num_str),
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

        print("\nBFS number comparison:")
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

    rangeselector_buttons = [
        dict(count=7, label="1W", step="day", stepmode="backward"),
        dict(count=1, label="1M", step="month", stepmode="backward"),
        dict(count=3, label="3M", step="month", stepmode="backward"),
        dict(count=6, label="6M", step="month", stepmode="backward"),
        dict(step="all", label="All"),
    ]

    for row in (1, 2):
        for col in (1, 2):
            fig.update_xaxes(showgrid=True, zeroline=False, row=row, col=col)
            fig.update_yaxes(showgrid=True, zeroline=False, row=row, col=col)

    fig.update_xaxes(
        rangeselector=dict(buttons=rangeselector_buttons),
        title_text="Snapshot date",
        row=1,
        col=1,
    )
    fig.update_xaxes(
        matches="x",
        title_text="Snapshot date",
        row=2,
        col=1,
    )

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


def find_bfs_removal_changeset(relation_id, bfs_tag="swisstopo:BFS_NUMMER", timeout=15):
    """Query the OSM API history for a relation and return the changeset that removed *bfs_tag*.

    Returns a dict with keys 'changeset', 'user', 'timestamp', and 'url' when found,
    or None if the history cannot be retrieved or the tag was never removed.
    """
    url = f"{OSM_API_BASE_URL}/relation/{relation_id}/history.json"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        history = response.json().get("elements", [])
    except Exception as e:
        print(f"Warning: Could not fetch OSM history for relation {relation_id}: {e}")
        return None

    # Walk versions from newest to oldest to find where the tag disappeared.
    # range starts at len-1 and stops before 0, so the minimum i is 1 — which
    # checks history[1] (v2) against history[0] (v1).  A tag cannot be removed
    # in v1 (the initial version), so no valid removal is missed.
    for i in range(len(history) - 1, 0, -1):
        current = history[i]
        previous = history[i - 1]
        current_tags = current.get("tags", {})
        previous_tags = previous.get("tags", {})
        if bfs_tag not in current_tags and bfs_tag in previous_tags:
            changeset_id = current.get("changeset")
            return {
                "changeset": changeset_id,
                "user": current.get("user", "unknown"),
                "timestamp": current.get("timestamp", ""),
                "url": f"https://www.openstreetmap.org/changeset/{changeset_id}",
            }
    return None


def find_latest_relation_changeset(relation_id, timeout=15):
    """Return latest relation changeset metadata or None.

    Args:
        relation_id: OSM relation id as string or int-compatible value.
        timeout: API request timeout in seconds (default: 15).

    Returns a dict with keys 'changeset', 'user', 'timestamp', and 'url',
    or None if the API call fails, the relation has no history, or no
    changeset id is available.
    """
    url = f"{OSM_API_BASE_URL}/relation/{relation_id}/history.json"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        history = response.json().get("elements", [])
    except Exception as e:
        print(
            f"Warning: Could not fetch latest changeset for relation {relation_id}: {e}"
        )
        return None

    if not history:
        return None

    latest = history[-1]
    changeset_id = latest.get("changeset")
    if not changeset_id:
        return None

    return {
        "changeset": changeset_id,
        "user": latest.get("user", "unknown"),
        "timestamp": latest.get("timestamp", ""),
        "url": f"https://www.openstreetmap.org/changeset/{changeset_id}",
    }


def build_boundary_difference_url(geom1, geom2):
    """Build an OSM map link to a representative point of boundary mismatch.

    Args:
        geom1: Swisstopo geometry in EPSG:2056.
        geom2: OSM geometry in EPSG:2056.

    Returns:
        URL string to the likely mismatch location, or empty string when
        geometries are missing/equal or mismatch-point extraction fails.
    """
    try:
        if geom1 is None or geom2 is None:
            return ""
        geom1 = force_2d(geom1)
        geom2 = force_2d(geom2)
        diff = geom1.symmetric_difference(geom2)
        if diff.is_empty:
            return ""

        point = diff.representative_point()
        lon, lat = LV95_TO_WGS84.transform(point.x, point.y)
        return f"https://www.openstreetmap.org/?mlat={lat:.6f}&mlon={lon:.6f}#map={BOUNDARY_DIFF_MAP_ZOOM}/{lat:.6f}/{lon:.6f}"
    except Exception as e:
        print(f"Warning: Could not build boundary difference URL: {e}")
        return ""


def send_deterioration_email(subject, body):
    """Send an email notification about metric deterioration.

    Reads connection settings from environment variables:
      NOTIFICATION_EMAIL – recipient address (required)
      SMTP_HOST          – SMTP server hostname (required)
      SMTP_PORT          – SMTP server port (default: 587)
      SMTP_USER          – SMTP login username (required)
      SMTP_PASSWORD      – SMTP login password (required)

    Returns True if the email was sent successfully, False otherwise.
    """
    to_addr = os.environ.get("NOTIFICATION_EMAIL")
    if not to_addr:
        print("NOTIFICATION_EMAIL not set, skipping email notification.")
        return False

    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_port_str = os.environ.get("SMTP_PORT", "587")
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")

    if not smtp_host or not smtp_user or not smtp_password:
        print("SMTP configuration incomplete, skipping email notification.")
        return False

    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        print(
            f"Warning: SMTP_PORT must be a valid integer, got '{smtp_port_str}'. Skipping email notification."
        )
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_addr
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_addr], msg.as_string())
        print(f"Deterioration notification sent to {to_addr}")
        return True
    except Exception as e:
        print(f"Warning: Could not send deterioration email: {e}")
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
    only_osm_df = results_df[(results_df["relation"] != "") & results_df["iou"].isna()]
    matched = len(matched_df)
    missing = len(only_swisstopo_df)
    total = matched + missing

    report_lines.append("\n## Dataset Overview")
    report_lines.append("\n| Metric                         | Value |")
    report_lines.append("|--------------------------------|------:|")
    report_lines.append(f"| Total Swisstopo municipalities | {total:>5} |")
    report_lines.append(f"| Matched in OSM                 | {matched:>5} |")
    report_lines.append(f"| Missing in OSM                 | {missing:>5} |")
    report_lines.append(f"| Only in OSM (not in Swisstopo) | {len(only_osm_df):>5} |")

    iou_change = None
    area_diff_change = None
    hausdorff_change = None
    deteriorations = []
    area_diff_deteriorations = []
    hausdorff_deteriorations = []
    relation_changeset_cache = {}
    det_df = pd.DataFrame()
    area_det_df = pd.DataFrame()
    hd_det_df = pd.DataFrame()

    if matched > 0:
        report_lines.append("\n## Accuracy Metrics (for matched municipalities)")
        report_lines.append("\n| Metric                    | Value  |")
        report_lines.append("|---------------------------|--------|")
        report_lines.append(
            f"| Mean IoU                  | {matched_df['iou'].mean():.4f} |"
        )
        report_lines.append(
            f"| Median IoU                | {matched_df['iou'].median():.4f} |"
        )
        report_lines.append(
            f"| Mean area difference      | {matched_df['area_diff_pct'].mean():.3f}% |"
        )
        report_lines.append(
            f"| Mean symmetric difference | {matched_df['symmetric_diff_pct'].mean():.3f}% |"
        )
        report_lines.append(
            f"| Mean Hausdorff distance   | {matched_df['hausdorff_distance'].mean():.4f} |"
        )

        excellent = (matched_df["iou"] >= 0.98).sum()
        good = ((matched_df["iou"] >= 0.95) & (matched_df["iou"] < 0.98)).sum()
        fair = ((matched_df["iou"] >= 0.90) & (matched_df["iou"] < 0.95)).sum()
        poor = (matched_df["iou"] < 0.90).sum()

        report_lines.append("\n## Quality Distribution")
        report_lines.append("\n| Quality    | Count | Percentage |")
        report_lines.append("|------------|-------|-----------:|")
        report_lines.append(
            f"| IoU ≥ 0.98 | {excellent:>5} | {excellent/matched*100:>10.3f} |"
        )
        report_lines.append(f"| IoU ≥ 0.95 | {good:>5} | {good/matched*100:>10.3f} |")
        report_lines.append(f"| IoU ≥ 0.90 | {fair:>5} | {fair/matched*100:>10.3f} |")
        report_lines.append(f"| IoU < 0.90 | {poor:>5} | {poor/matched*100:>10.3f} |")

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
                report_lines.append("\n| Metric                           | Value   |")
                report_lines.append("|----------------------------------|---------|")
                report_lines.append(
                    f"| Previous mean IoU                | {prev_mean_iou:7.3f} |"
                )
                report_lines.append(
                    f"| Current mean IoU                 | {current_mean_iou:7.3f} |"
                )
                report_lines.append(
                    f"| Change                           | {iou_change:+7.3f} |"
                )

                prev_mean_area_diff = prev_data[prev_matched]["area_diff_pct"].mean()
                current_mean_area_diff = matched_df["area_diff_pct"].mean()
                area_diff_change = current_mean_area_diff - prev_mean_area_diff
                report_lines.append(
                    f"| Previous mean area difference    | {prev_mean_area_diff:7.3f}% |"
                )
                report_lines.append(
                    f"| Current mean area difference     | {current_mean_area_diff:7.3f}% |"
                )
                report_lines.append(
                    f"| Area difference change           | {area_diff_change:+7.3f}% |"
                )

                # Hausdorff distance historical comparison (higher = worse)
                if "hausdorff_distance" in prev_data.columns:
                    prev_hausdorff_valid = prev_data[
                        prev_matched & prev_data["hausdorff_distance"].notna()
                    ]
                    curr_hausdorff_valid = matched_df[
                        matched_df["hausdorff_distance"].notna()
                    ]
                    if len(prev_hausdorff_valid) > 0 and len(curr_hausdorff_valid) > 0:
                        prev_mean_hausdorff = prev_hausdorff_valid[
                            "hausdorff_distance"
                        ].mean()
                        current_mean_hausdorff = curr_hausdorff_valid[
                            "hausdorff_distance"
                        ].mean()
                        hausdorff_change = current_mean_hausdorff - prev_mean_hausdorff
                        report_lines.append(
                            f"| Previous mean Hausdorff distance | {prev_mean_hausdorff:7.3f} |"
                        )
                        report_lines.append(
                            f"| Current mean Hausdorff distance  | {current_mean_hausdorff:7.3f} |"
                        )
                        report_lines.append(
                            f"| Hausdorff change                 | {hausdorff_change:+7.3f} |"
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

        report_lines.append("\n## Most Deteriorated (if historical data available)")
        if len(historical_df) > 0:
            # Find municipalities that deteriorated in IoU or Hausdorff distance
            prev_date = historical_df["date"].max()
            prev_data = historical_df[historical_df["date"] == prev_date].set_index(
                "bfs_nummer"
            )

            for idx, row in matched_df.iterrows():
                bfs = row["bfs_nummer"]
                if bfs in prev_data.index:
                    relation_id = normalize_relation_id(row.get("relation", ""))
                    osm_url = (
                        f"https://www.openstreetmap.org/relation/{relation_id}"
                        if relation_id
                        else ""
                    )
                    base_entry = {
                        "name": row["name"],
                        "bfs_nummer": bfs,
                        "relation": relation_id,
                        "osm_url": osm_url,
                        "boundary_diff_url": build_boundary_difference_url(
                            row.get("geometry"), row.get("osm_geometry")
                        ),
                    }
                    if pd.notna(prev_data.loc[bfs, "iou"]):
                        prev_iou = prev_data.loc[bfs, "iou"]
                        curr_iou = row["iou"]
                        deterioration = prev_iou - curr_iou
                        if deterioration > IOU_DETERIORATION_THRESHOLD:
                            deteriorations.append(
                                {
                                    **base_entry,
                                    "prev_iou": prev_iou,
                                    "curr_iou": curr_iou,
                                    "deterioration": deterioration,
                                }
                            )
                    if pd.notna(prev_data.loc[bfs, "area_diff_pct"]) and pd.notna(
                        row["area_diff_pct"]
                    ):
                        prev_area_diff = prev_data.loc[bfs, "area_diff_pct"]
                        curr_area_diff = row["area_diff_pct"]
                        area_diff_increase = curr_area_diff - prev_area_diff
                        if (
                            area_diff_increase
                            > AREA_DIFF_DETERIORATION_THRESHOLD_PCT_POINTS
                        ):
                            area_diff_deteriorations.append(
                                {
                                    **base_entry,
                                    "prev_area_diff_pct": prev_area_diff,
                                    "curr_area_diff_pct": curr_area_diff,
                                    "increase_pct_points": area_diff_increase,
                                }
                            )
                    if (
                        "hausdorff_distance" in prev_data.columns
                        and pd.notna(prev_data.loc[bfs, "hausdorff_distance"])
                        and pd.notna(row["hausdorff_distance"])
                    ):
                        prev_hd = prev_data.loc[bfs, "hausdorff_distance"]
                        curr_hd = row["hausdorff_distance"]
                        hd_increase = curr_hd - prev_hd
                        if hd_increase > HAUSDORFF_DETERIORATION_THRESHOLD_M:
                            hausdorff_deteriorations.append(
                                {
                                    **base_entry,
                                    "prev_hausdorff_m": prev_hd,
                                    "curr_hausdorff_m": curr_hd,
                                    "increase_m": hd_increase,
                                }
                            )

            if deteriorations:
                det_df = pd.DataFrame(deteriorations).nlargest(10, "deterioration")
            if area_diff_deteriorations:
                area_det_df = pd.DataFrame(area_diff_deteriorations).nlargest(
                    10, "increase_pct_points"
                )
            if hausdorff_deteriorations:
                hd_det_df = pd.DataFrame(hausdorff_deteriorations).nlargest(
                    10, "increase_m"
                )

            for metric_df in (det_df, area_det_df, hd_det_df):
                if metric_df.empty:
                    continue
                for row_index, row in metric_df.iterrows():
                    relation_id = row.get("relation", "")
                    if not relation_id:
                        continue
                    if relation_id not in relation_changeset_cache:
                        relation_changeset_cache[relation_id] = (
                            find_latest_relation_changeset(relation_id) or {}
                        )
                    changeset = relation_changeset_cache[relation_id]
                    metric_df.at[row_index, "changeset_url"] = changeset.get("url", "")
                    metric_df.at[row_index, "changeset_user"] = changeset.get(
                        "user", ""
                    )
                    metric_df.at[row_index, "changeset_timestamp"] = changeset.get(
                        "timestamp", ""
                    )
            if not det_df.empty:
                report_lines.append("\n" + det_df.to_markdown(index=False))
            else:
                report_lines.append("\nNo significant deteriorations detected.")

            if not area_det_df.empty:
                report_lines.append(
                    "\n## Most Deteriorated in Area Difference (if historical data available)"
                )
                report_lines.append("\n" + area_det_df.to_markdown(index=False))

            if not hd_det_df.empty:
                report_lines.append(
                    "\n## Most Deteriorated in Hausdorff Distance (if historical data available)"
                )
                report_lines.append("\n" + hd_det_df.to_markdown(index=False))
        else:
            report_lines.append("\n_(Insufficient historical data)_")

    # BFS numbers only in Swisstopo (missing in OSM)
    if len(only_swisstopo_df) > 0:
        report_lines.append(
            "\n## BFS numbers only in Swisstopo (missing in OSM) (showing first 20):"
        )
        swisstopo_only_list = only_swisstopo_df.head(20)[["name", "bfs_nummer"]]
        report_lines.append(swisstopo_only_list.to_markdown(index=False))

    # BFS numbers only in OSM (not in Swisstopo)
    if len(only_osm_df) > 0:
        report_lines.append(
            "\n## BFS numbers only in OSM (not in Swisstopo) (showing first 20):"
        )
        osm_only_list = only_osm_df.head(20)[["name", "bfs_nummer", "relation"]]
        report_lines.append("\n" + osm_only_list.to_markdown(index=False))

    # Detect municipalities that were previously matched in OSM but are now swisstopo-only.
    # This means their swisstopo:BFS_NUMMER tag was likely removed from the OSM relation.
    newly_missing = []
    if len(historical_df) > 0 and len(only_swisstopo_df) > 0:
        prev_date = historical_df["date"].max()
        prev_data = historical_df[historical_df["date"] == prev_date]
        prev_matched = prev_data[prev_data["iou"].notna()].copy()
        # Use pd.to_numeric to safely coerce bfs_nummer from CSV (may be float or string).
        prev_matched_bfs = set(
            pd.to_numeric(prev_matched["bfs_nummer"], errors="coerce")
            .dropna()
            .astype(int)
            .astype(str)
        )
        prev_relation_lookup = (
            prev_matched.dropna(subset=["bfs_nummer", "relation"])
            .assign(
                bfs_key=lambda df: pd.to_numeric(df["bfs_nummer"], errors="coerce")
                .dropna()
                .astype(int)
                .astype(str)
            )
            .set_index("bfs_key")["relation"]
            .to_dict()
        )

        for _, row in only_swisstopo_df.iterrows():
            bfs = row["bfs_nummer"]
            if pd.isna(bfs):
                continue
            bfs_key = str(int(bfs))
            if bfs_key in prev_matched_bfs:
                relation_raw = prev_relation_lookup.get(bfs_key, "")
                relation_id = normalize_relation_id(relation_raw)
                entry = {
                    "bfs_nummer": int(bfs),
                    "relation": relation_id,
                    "name": row.get("name", ""),
                }
                if relation_id:
                    entry["osm_url"] = (
                        f"https://www.openstreetmap.org/relation/{relation_id}"
                    )
                    print(
                        f"  - Querying OSM history for relation {relation_id}"
                        f" (BFS {bfs_key}, {entry['name']})..."
                    )
                    changeset_info = find_bfs_removal_changeset(relation_id)
                    if changeset_info:
                        entry["changeset_url"] = changeset_info["url"]
                        entry["changeset_user"] = changeset_info["user"]
                        entry["changeset_timestamp"] = changeset_info["timestamp"]
                newly_missing.append(entry)

    if newly_missing:
        report_lines.append(
            f"\n## Municipalities whose swisstopo:BFS_NUMMER tag was removed from OSM"
            f" ({len(newly_missing)}):"
        )
        for m in newly_missing:
            line = f"  • {m['name']} (BFS {m['bfs_nummer']})"
            if m.get("osm_url"):
                line += f"  — OSM relation: {m['osm_url']}"
            if m.get("changeset_url"):
                line += (
                    f"  — tag removed in changeset {m['changeset_url']}"
                    f" by {m.get('changeset_user', '?')}"
                    f" at {m.get('changeset_timestamp', '?')}"
                )
            report_lines.append(line)

    # Persistent BFS removal tracking: load the tracker, update it, and report
    # unresolved removals from previous runs and any newly restored municipalities.
    bfs_removal_tracker = load_bfs_removal_tracker()
    today_str = datetime.now(UTC).strftime("%Y-%m-%d")

    # Add newly detected removals to the tracker (don't overwrite existing entries)
    for entry in newly_missing:
        bfs_key = str(entry["bfs_nummer"])
        if bfs_key not in bfs_removal_tracker:
            bfs_removal_tracker[bfs_key] = dict(entry, first_detected=today_str)

    # Detect resolutions: tracked municipalities now matched again
    matched_bfs_str = {str(b) for b in matched_df["bfs_nummer"].values}
    resolved_removals = []
    for bfs_key in list(bfs_removal_tracker.keys()):
        if bfs_key in matched_bfs_str:
            resolved_removals.append(bfs_removal_tracker.pop(bfs_key))

    # Persistent unresolved: tracked but NOT newly detected this run
    newly_missing_bfs = {str(e["bfs_nummer"]) for e in newly_missing}
    persistent_missing = [
        entry
        for bfs_key, entry in bfs_removal_tracker.items()
        if bfs_key not in newly_missing_bfs
    ]

    # Save updated tracker
    save_bfs_removal_tracker(bfs_removal_tracker)

    if persistent_missing:
        report_lines.append(
            f"\n## Municipalities with swisstopo:BFS_NUMMER still absent from OSM"
            f" (previously detected, unresolved) ({len(persistent_missing)}):"
        )
        for m in persistent_missing:
            line = f"  • {m['name']} (BFS {m['bfs_nummer']})"
            line += f"  — first detected: {m.get('first_detected', 'unknown')}"
            if m.get("osm_url"):
                line += f"  — OSM relation: {m['osm_url']}"
            if m.get("changeset_url"):
                line += (
                    f"  — tag removed in changeset {m['changeset_url']}"
                    f" by {m.get('changeset_user', '?')}"
                    f" at {m.get('changeset_timestamp', '?')}"
                )
            report_lines.append(line)

    if resolved_removals:
        report_lines.append(
            f"\n## Resolved: swisstopo:BFS_NUMMER tag restored in OSM"
            f" ({len(resolved_removals)}):"
        )
        for m in resolved_removals:
            line = f"  • {m['name']} (BFS {m['bfs_nummer']})"
            line += f"  — first detected: {m.get('first_detected', 'unknown')}"
            if m.get("osm_url"):
                line += f"  — OSM relation: {m['osm_url']}"
            report_lines.append(line)

    report_text = "\n".join(report_lines)
    print(report_text)

    # Save reports
    with open("output/comparison_report.md", "w") as f:
        f.write(report_text)

    # Send email notification if global metrics deteriorated OR any municipality shows significant
    # deterioration OR municipalities newly lost or still have their OSM swisstopo:BFS_NUMMER tag absent.
    iou_deteriorated_global = iou_change is not None and iou_change < 0
    area_diff_deteriorated_global = (
        area_diff_change is not None and area_diff_change > 0
    )
    hausdorff_deteriorated_global = (
        hausdorff_change is not None and hausdorff_change > 0
    )

    iou_deteriorated_local = len(deteriorations) > 0
    area_diff_deteriorated_local = len(area_diff_deteriorations) > 0
    hausdorff_deteriorated_local = len(hausdorff_deteriorations) > 0
    bfs_tags_removed = len(newly_missing) > 0 or len(persistent_missing) > 0
    bfs_tags_restored = len(resolved_removals) > 0

    should_alert = (
        iou_deteriorated_global
        or area_diff_deteriorated_global
        or hausdorff_deteriorated_global
        or iou_deteriorated_local
        or area_diff_deteriorated_local
        or hausdorff_deteriorated_local
        or bfs_tags_removed
        or bfs_tags_restored
    )

    print(
        "Email trigger debug:",
        {
            "iou_change": iou_change,
            "area_diff_change": area_diff_change,
            "hausdorff_change": hausdorff_change,
            "iou_deteriorated_global": iou_deteriorated_global,
            "area_diff_deteriorated_global": area_diff_deteriorated_global,
            "hausdorff_deteriorated_global": hausdorff_deteriorated_global,
            "iou_deteriorated_local": iou_deteriorated_local,
            "area_diff_deteriorated_local": area_diff_deteriorated_local,
            "hausdorff_deteriorated_local": hausdorff_deteriorated_local,
            "deteriorations_count": len(deteriorations),
            "area_diff_deteriorations_count": len(area_diff_deteriorations),
            "hausdorff_deteriorations_count": len(hausdorff_deteriorations),
            "bfs_tags_removed": bfs_tags_removed,
            "newly_missing_count": len(newly_missing),
            "persistent_missing_count": len(persistent_missing),
            "bfs_tags_restored": bfs_tags_restored,
            "resolved_removals_count": len(resolved_removals),
            "should_alert": should_alert,
        },
    )

    if should_alert:
        run_date = datetime.now(UTC).strftime("%Y-%m-%d")
        subject = f"[swissboundaries] Metric deterioration detected on {run_date}"

        alert_parts = []
        if iou_deteriorated_global:
            alert_parts.append(f"Global mean IoU decreased by {abs(iou_change):.4f}")
        if area_diff_deteriorated_global:
            alert_parts.append(
                f"Global mean area difference increased by {area_diff_change:.3f} percentage points"
            )
        if hausdorff_deteriorated_global:
            alert_parts.append(
                f"Global mean Hausdorff distance increased by {hausdorff_change:.3f} m"
            )
        if iou_deteriorated_local:
            worst_iou_det = max(d["deterioration"] for d in deteriorations)
            alert_parts.append(
                f"{len(deteriorations)} municipality(ies) had IoU deterioration > {IOU_DETERIORATION_THRESHOLD:.3f} "
                f"(worst -{worst_iou_det:.4f})"
            )
        if area_diff_deteriorated_local:
            worst_area_diff_det = max(
                d["increase_pct_points"] for d in area_diff_deteriorations
            )
            alert_parts.append(
                f"{len(area_diff_deteriorations)} municipality(ies) had area difference increase > {AREA_DIFF_DETERIORATION_THRESHOLD_PCT_POINTS:.3f} pp "
                f"(worst +{worst_area_diff_det:.3f} pp)"
            )
        if hausdorff_deteriorated_local:
            worst_hd_det = max(d["increase_m"] for d in hausdorff_deteriorations)
            alert_parts.append(
                f"{len(hausdorff_deteriorations)} municipality(ies) had Hausdorff increase > {HAUSDORFF_DETERIORATION_THRESHOLD_M:.1f} m "
                f"(worst +{worst_hd_det:.3f} m)"
            )
        if newly_missing:
            alert_parts.append(
                f"{len(newly_missing)} municipality(ies) newly lost their OSM"
                f" swisstopo:BFS_NUMMER tag"
            )
        if persistent_missing:
            alert_parts.append(
                f"{len(persistent_missing)} municipality(ies) still have their OSM"
                f" swisstopo:BFS_NUMMER tag absent (previously detected)"
            )
        if bfs_tags_restored:
            alert_parts.append(
                f"{len(resolved_removals)} municipality(ies) had their OSM"
                f" swisstopo:BFS_NUMMER tag restored"
            )

        email_lines = [
            f"swissboundaries boundary comparison – {run_date}",
            "",
            "The following deterioration conditions were detected:",
        ]
        for part in alert_parts:
            email_lines.append(f"  • {part}")

        if not det_df.empty:
            email_lines.append("")
            email_lines.append("Top IoU deteriorations (per municipality):")
            for _, item in det_df.iterrows():
                email_lines.append(
                    f"  • {item['name']} (BFS {int(item['bfs_nummer'])}): "
                    f"{item['prev_iou']:.6f} → {item['curr_iou']:.6f} "
                    f"(Δ {-item['deterioration']:+.6f})"
                )
                osm_url = item.get("osm_url")
                changeset_url = item.get("changeset_url")
                boundary_diff_url = item.get("boundary_diff_url")
                if pd.notna(osm_url) and osm_url:
                    email_lines.append(f"    OSM relation: {osm_url}")
                if pd.notna(changeset_url) and changeset_url:
                    email_lines.append(f"    Latest OSM changeset: {changeset_url}")
                if pd.notna(boundary_diff_url) and boundary_diff_url:
                    email_lines.append(
                        f"    Likely deteriorated boundary segment: {boundary_diff_url}"
                    )

        if not area_det_df.empty:
            email_lines.append("")
            email_lines.append("Top area difference increases (per municipality):")
            for _, item in area_det_df.iterrows():
                email_lines.append(
                    f"  • {item['name']} (BFS {int(item['bfs_nummer'])}): "
                    f"{item['prev_area_diff_pct']:.4f}% → {item['curr_area_diff_pct']:.4f}% "
                    f"(Δ {item['increase_pct_points']:+.4f} pp)"
                )
                osm_url = item.get("osm_url")
                changeset_url = item.get("changeset_url")
                boundary_diff_url = item.get("boundary_diff_url")
                if pd.notna(osm_url) and osm_url:
                    email_lines.append(f"    OSM relation: {osm_url}")
                if pd.notna(changeset_url) and changeset_url:
                    email_lines.append(f"    Latest OSM changeset: {changeset_url}")
                if pd.notna(boundary_diff_url) and boundary_diff_url:
                    email_lines.append(
                        f"    Likely deteriorated boundary segment: {boundary_diff_url}"
                    )

        if not hd_det_df.empty:
            email_lines.append("")
            email_lines.append("Top Hausdorff distance increases (per municipality):")
            for _, item in hd_det_df.iterrows():
                email_lines.append(
                    f"  • {item['name']} (BFS {int(item['bfs_nummer'])}): "
                    f"{item['prev_hausdorff_m']:.3f} m → {item['curr_hausdorff_m']:.3f} m "
                    f"(Δ {item['increase_m']:+.3f} m)"
                )
                osm_url = item.get("osm_url")
                changeset_url = item.get("changeset_url")
                boundary_diff_url = item.get("boundary_diff_url")
                if pd.notna(osm_url) and osm_url:
                    email_lines.append(f"    OSM relation: {osm_url}")
                if pd.notna(changeset_url) and changeset_url:
                    email_lines.append(f"    Latest OSM changeset: {changeset_url}")
                if pd.notna(boundary_diff_url) and boundary_diff_url:
                    email_lines.append(
                        f"    Likely deteriorated boundary segment: {boundary_diff_url}"
                    )

        if newly_missing:
            email_lines.append("")
            email_lines.append(
                "Municipalities whose swisstopo:BFS_NUMMER tag was removed from OSM:"
            )
            for m in newly_missing:
                email_lines.append(f"  • {m['name']} (BFS {m['bfs_nummer']})")
                if m.get("osm_url"):
                    email_lines.append(f"    OSM relation:  {m['osm_url']}")
                if m.get("changeset_url"):
                    email_lines.append(
                        f"    Tag removed in changeset: {m['changeset_url']}"
                    )
                    email_lines.append(
                        f"    By: {m.get('changeset_user', '?')}"
                        f" at {m.get('changeset_timestamp', '?')}"
                    )

        if persistent_missing:
            email_lines.append("")
            email_lines.append(
                "Municipalities with swisstopo:BFS_NUMMER still absent from OSM"
                " (previously detected, unresolved):"
            )
            for m in persistent_missing:
                email_lines.append(
                    f"  • {m['name']} (BFS {m['bfs_nummer']})"
                    f"  — first detected: {m.get('first_detected', 'unknown')}"
                )
                if m.get("osm_url"):
                    email_lines.append(f"    OSM relation:  {m['osm_url']}")
                if m.get("changeset_url"):
                    email_lines.append(
                        f"    Tag removed in changeset: {m['changeset_url']}"
                    )
                    email_lines.append(
                        f"    By: {m.get('changeset_user', '?')}"
                        f" at {m.get('changeset_timestamp', '?')}"
                    )

        if resolved_removals:
            email_lines.append("")
            email_lines.append(
                "Municipalities whose swisstopo:BFS_NUMMER tag was restored in OSM:"
            )
            for m in resolved_removals:
                email_lines.append(
                    f"  • {m['name']} (BFS {m['bfs_nummer']})"
                    f"  — first detected missing: {m.get('first_detected', 'unknown')}"
                )
                if m.get("osm_url"):
                    email_lines.append(f"    OSM relation:  {m['osm_url']}")

        email_lines.append("")
        email_lines.append("Full report: https://habi.github.io/swissboundaries/")

        print("Triggering send_deterioration_email()")
        email_sent = send_deterioration_email(subject, "\n".join(email_lines))
        if not email_sent:
            # Emit a GitHub Actions warning annotation so the alert is visible
            # in the workflow run even when email delivery fails.
            print(
                f"::warning::Deterioration detected but email notification could not be sent. "
                f"Conditions: {', '.join(alert_parts)}"
            )

    # Save CSV (without geometry columns for CSV)
    csv_df = results_df.drop(columns=["geometry", "osm_geometry"], errors="ignore")

    # Convert bfs_nummer, kantonsnummer, and bezirksnummer to integer
    csv_df["bfs_nummer"] = pd.to_numeric(csv_df["bfs_nummer"], errors="coerce").astype(
        "Int64"
    )  # Int64 handles NaN values
    csv_df["kantonsnummer"] = pd.to_numeric(
        csv_df["kantonsnummer"], errors="coerce"
    ).astype("Int64")
    csv_df["bezirksnummer"] = pd.to_numeric(
        csv_df["bezirksnummer"], errors="coerce"
    ).astype("Int64")

    # Reorder columns
    column_order = [
        "name",
        "country",
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
    ]
    csv_df = csv_df[[col for col in column_order if col in csv_df.columns]]

    csv_df.to_csv(
        "output/detailed_results.csv",
        header=[
            "Name",
            "Country",
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
        results_indexed = results_df.drop_duplicates("bfs_nummer").set_index(
            "bfs_nummer"
        )

        features = []
        for _, row in gdf_wgs84.iterrows():
            bfs = int(row["bfs_nummer"])
            point = row["_point"]
            name = row.get("name", row.get("NAME", str(bfs)))

            props = {"name": name, "bfs_nummer": bfs}

            if bfs in results_indexed.index:
                r = results_indexed.loc[bfs]
                props["iou"] = float(r["iou"]) if pd.notna(r.get("iou")) else None
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
                props["area_diff_pct"] = None
                props["hausdorff_distance"] = None
                props["symmetric_diff_pct"] = None

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

        geojson_data = json.dumps({"type": "FeatureCollection", "features": features})

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Municipality Boundary Quality Map of Switzerland and the Principality of Liechtenstein</title>
    This interactive map shows the quality of OSM municipality boundaries compared to Swisstopo.
     Each dot represents a municipality, colored from red (low metric) to green (high metric).
     The median value is orange.
     Click on a dot to see details  .
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-providers@2.0.0/leaflet-providers.js"></script>
    <style>
        html, body {{ height: 100%; margin: 0; padding: 0; }}
        #map {{ height: 95%; width: 100%; }}
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
    var map = L.map('map').setView([46.82, 8.22], 8);

    L.tileLayer.provider('Stadia.StamenTonerLite').addTo(map);
    // Stadia API key is managed via "domain authentication" in the (free) account of @habi with 200000 credits/month
    
    var metricConfig = {{
        iou: {{
            label: 'IoU Quality',
            property: 'iou',
            decimals: 6,
            unit: '',
            betterHigh: true
        }},
        area_diff_pct: {{
            label: 'Area Diff [%]',
            property: 'area_diff_pct',
            decimals: 4,
            unit: '%',
            betterHigh: false
        }},
        hausdorff_distance: {{
            label: 'Hausdorff Distance [m]',
            property: 'hausdorff_distance',
            decimals: 3,
            unit: ' m',
            betterHigh: false
        }},
        symmetric_diff_pct: {{
            label: 'Symmetric Diff [%]',
            property: 'symmetric_diff_pct',
            decimals: 4,
            unit: '%',
            betterHigh: false
        }}
    }};

    function isNumber(value) {{
        return value !== null && value !== undefined && !isNaN(value);
    }}

    function quantile(sortedValues, q) {{
        if (!sortedValues.length) return 0;
        var pos = (sortedValues.length - 1) * q;
        var base = Math.floor(pos);
        var rest = pos - base;
        var next = sortedValues[base + 1];
        if (next !== undefined) {{
            return sortedValues[base] + rest * (next - sortedValues[base]);
        }}
        return sortedValues[base];
    }}

    function collectValues(metricKey) {{
        var prop = metricConfig[metricKey].property;
        var values = [];
        for (var i = 0; i < data.features.length; i++) {{
            var v = data.features[i].properties[prop];
            if (isNumber(v)) values.push(v);
        }}
        values.sort(function(a, b) {{ return a - b; }});
        return values;
    }}

    function buildStats(metricKey) {{
        var values = collectValues(metricKey);
        if (!values.length) {{
            return {{ min: 0, max: 1, median: 0.5 }};
        }}
        var mid = Math.floor(values.length / 2);
        var median = values.length % 2 !== 0
            ? values[mid]
            : (values[mid - 1] + values[mid]) / 2;
        return {{
            min: values[0],
            max: values[values.length - 1],
            median: median
        }};
    }}

    function buildMetricRanks(metricKey) {{
        var cfg = metricConfig[metricKey];
        var prop = cfg.property;
        var rows = [];

        for (var i = 0; i < data.features.length; i++) {{
            var props = data.features[i].properties || {{}};
            var value = props[prop];
            var bfs = props.bfs_nummer;
            if (!isNumber(value) || bfs === null || bfs === undefined) continue;
            rows.push({{ bfs: String(bfs), value: value }});
        }}

        var worstSorted = rows.slice().sort(function(a, b) {{
            // IoU: lower is worse. Distance/diff: higher is worse.
            return cfg.betterHigh ? a.value - b.value : b.value - a.value;
        }});
        var bestSorted = rows.slice().sort(function(a, b) {{
            // IoU: higher is better. Distance/diff: lower is better.
            return cfg.betterHigh ? b.value - a.value : a.value - b.value;
        }});

        var ranks = {{
            worst10: {{}},
            nextWorst10: {{}},
            best10: {{}}
        }};

        var worstCount = Math.min(10, worstSorted.length);
        for (var j = 0; j < worstCount; j++) {{
            ranks.worst10[worstSorted[j].bfs] = true;
        }}

        var nextStart = worstCount;
        var nextEnd = Math.min(nextStart + 10, worstSorted.length);
        for (var k = nextStart; k < nextEnd; k++) {{
            var bfs = worstSorted[k].bfs;
            if (!ranks.worst10[bfs]) {{
                ranks.nextWorst10[bfs] = true;
            }}
        }}

        var bestCount = Math.min(10, bestSorted.length);
        for (var m = 0; m < bestCount; m++) {{
            var bestBfs = bestSorted[m].bfs;
            if (!ranks.worst10[bestBfs] && !ranks.nextWorst10[bestBfs]) {{
                ranks.best10[bestBfs] = true;
            }}
        }}

        return ranks;
    }}

    var metricStats = {{
        iou: buildStats('iou'),
        area_diff_pct: buildStats('area_diff_pct'),
        hausdorff_distance: buildStats('hausdorff_distance'),
        symmetric_diff_pct: buildStats('symmetric_diff_pct')
    }};

    var metricRanks = {{
        iou: buildMetricRanks('iou'),
        area_diff_pct: buildMetricRanks('area_diff_pct'),
        hausdorff_distance: buildMetricRanks('hausdorff_distance'),
        symmetric_diff_pct: buildMetricRanks('symmetric_diff_pct')
    }};

    var currentMetric = 'iou';

    function metricValue(props, metricKey) {{
        return props[metricConfig[metricKey].property];
    }}

    function metricToColor(value, metricKey, props) {{
        if (!isNumber(value)) {{
            return '#888888';
        }}

        var bfs = (props && props.bfs_nummer !== null && props.bfs_nummer !== undefined)
            ? String(props.bfs_nummer)
            : null;
        var ranks = metricRanks[metricKey] || {{}};
        if (bfs && ranks.worst10 && ranks.worst10[bfs]) return '#d7191c';
        if (bfs && ranks.nextWorst10 && ranks.nextWorst10[bfs]) return '#f18f01';
        if (bfs && ranks.best10 && ranks.best10[bfs]) return '#1a9641';

        var cfg = metricConfig[metricKey];
        var stats = metricStats[metricKey];
        var range = stats.max - stats.min;
        var t = range > 0 ? Math.min(1, Math.max(0, (value - stats.min) / range)) : 1;
        if (!cfg.betterHigh) {{
            t = 1 - t;
        }}
        var t_median = range > 0 ? Math.min(1, Math.max(0, (stats.median - stats.min) / range)) : 0.5;
        if (!cfg.betterHigh) {{
            t_median = 1 - t_median;
        }}
        var hue;
        if (t <= t_median) {{
            var sub_t = t_median > 0 ? t / t_median : 1;
            hue = Math.round(sub_t * 30);
        }} else {{
            var sub_t = (1 - t_median) > 0 ? (t - t_median) / (1 - t_median) : 1;
            hue = Math.round(30 + sub_t * 90);
        }}
        return 'hsl(' + hue + ',80%,40%)';
    }}

    function metricFillOpacity(value, metricKey, props) {{
        if (!isNumber(value)) {{
            return 0.60;
        }}

        var bfs = (props && props.bfs_nummer !== null && props.bfs_nummer !== undefined)
            ? String(props.bfs_nummer)
            : null;
        var ranks = metricRanks[metricKey] || {{}};
        if (bfs && ranks.worst10 && ranks.worst10[bfs]) return 1.0;
        if (bfs && ranks.nextWorst10 && ranks.nextWorst10[bfs]) return 1.0;
        if (bfs && ranks.best10 && ranks.best10[bfs]) return 1.0;

        return 0.30;
    }}

    function formatMetricValue(value, metricKey) {{
        if (!isNumber(value)) {{
            return 'N/A';
        }}
        var cfg = metricConfig[metricKey];
        return value.toFixed(cfg.decimals) + cfg.unit;
    }}

    var geoLayer = L.geoJSON(data, {{
        pointToLayer: function(feature, latlng) {{
            var props = feature.properties || {{}};
            var value = metricValue(props, currentMetric);
            return L.circleMarker(latlng, {{
                radius: 5,
                fillColor: metricToColor(value, currentMetric, props),
                color: '#222',
                weight: 0.6,
                opacity: 0.9,
                fillOpacity: metricFillOpacity(value, currentMetric, props)
            }});
        }},
        onEachFeature: function(feature, layer) {{
            var p = feature.properties;
            var bsfLink = p.bfs_nummer
                ? '<a href="swisstopo_geojson/' + p.bfs_nummer + '.geojson" target="_blank">' + p.bfs_nummer + '</a>'
                : '—';
            var osmLink = p.relation ? '<a href="https://osm.org/relation/' + p.relation + '" target="_blank">relation/' + p.relation + '</a>' : '—';
            var iouText = (p.iou !== null && p.iou !== undefined) ? p.iou.toFixed(6) : 'N/A (not in OSM)';
            var areaDiffText = (p.area_diff_pct !== null && p.area_diff_pct !== undefined) ? p.area_diff_pct.toFixed(4) + '%' : '—';
            var hausdorffText = (p.hausdorff_distance !== null && p.hausdorff_distance !== undefined) ? p.hausdorff_distance.toFixed(3) + ' m' : '—';
            var symDiffText = (p.symmetric_diff_pct !== null && p.symmetric_diff_pct !== undefined) ? p.symmetric_diff_pct.toFixed(4) + '%' : '—';
            layer.bindPopup(
                '<b>' + p.name + '</b><br>' +
                'BFS: ' + bsfLink + '<br>' +
                'OSM: ' + osmLink + '<br>' +
                'IoU: <b>' + iouText + '</b><br>' +
                'Area diff: ' + areaDiffText + '<br>' +
                'Hausdorff: ' + hausdorffText + '<br>' +
                'Symmetric diff: ' + symDiffText
            );
            layer.on('click', function() {{ this.openPopup(); }});
        }}
    }}).addTo(map);

    var legendDiv = null;

    function updateLegend() {{
        if (!legendDiv) return;
        var cfg = metricConfig[currentMetric];
        var stats = metricStats[currentMetric];
        var leftLabel = cfg.betterHigh
            ? 'Worse<br>(' + formatMetricValue(stats.min, currentMetric) + ')'
            : 'Worse<br>(' + formatMetricValue(stats.max, currentMetric) + ')';
        var rightLabel = cfg.betterHigh
            ? 'Better<br>(' + formatMetricValue(stats.max, currentMetric) + ')'
            : 'Better<br>(' + formatMetricValue(stats.min, currentMetric) + ')';

        legendDiv.innerHTML =
            '<h4>' + cfg.label + '</h4>' +
            '<div class="legend-gradient" style="opacity:0.30"></div>' +
            '<div class="legend-labels">' +
            '  <span>' + leftLabel + '</span>' +
            '  <span style="text-align:right">' + rightLabel + '</span>' +
            '</div>' +
            '<div class="legend-missing">' +
            '  <div class="legend-missing-dot" style="background:#d7191c"></div>' +
            '  <span>Worst 10</span>' +
            '</div>' +
            '<div class="legend-missing">' +
            '  <div class="legend-missing-dot" style="background:#1a9641"></div>' +
            '  <span>Best 10</span>' +
            '</div>' +
            '<div class="legend-missing">' +
            '  <div class="legend-missing-dot" style="background:#4c78a8; opacity:0.30"></div>' +
            '  <span>All others (semitransparent)</span>' +
            '</div>' +
            '<div class="legend-missing">' +
            '  <div class="legend-missing-dot"></div>' +
            '  <span>Not matched in OSM</span>' +
            '</div>';
    }}

    function updateLayerStyles() {{
        geoLayer.eachLayer(function(layer) {{
            if (!layer.feature || !layer.setStyle) return;
            var props = layer.feature.properties || {{}};
            var value = metricValue(props, currentMetric);
            layer.setStyle({{
                fillColor: metricToColor(value, currentMetric, props),
                fillOpacity: metricFillOpacity(value, currentMetric, props)
            }});
        }});
        updateLegend();
    }}

    // Metric switcher
    var metricSwitcher = L.control({{position: 'topright'}});
    metricSwitcher.onAdd = function() {{
        var div = L.DomUtil.create('div', 'legend');
        div.style.padding = '8px 10px';
        div.innerHTML =
            '<label for="metric-select" style="display:block;font-weight:600;margin-bottom:4px;">Map metric</label>' +
            '<select id="metric-select" style="width:170px;">' +
            '  <option value="iou">IoU</option>' +
            '  <option value="area_diff_pct">Area Diff [%]</option>' +
            '  <option value="hausdorff_distance">Hausdorff [m]</option>' +
            '  <option value="symmetric_diff_pct">Symmetric Diff [%]</option>' +
            '</select>';
        L.DomEvent.disableClickPropagation(div);
        return div;
    }};
    metricSwitcher.addTo(map);

    // Legend
    var legend = L.control({{position: 'bottomright'}});
    legend.onAdd = function() {{
        legendDiv = L.DomUtil.create('div', 'legend');
        updateLegend();
        return legendDiv;
    }};
    legend.addTo(map);

    var select = document.getElementById('metric-select');
    if (select) {{
        select.addEventListener('change', function(evt) {{
            currentMetric = evt.target.value;
            updateLayerStyles();
        }});
    }}

    updateLayerStyles();
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

    def read_markdown_file(path: Path) -> str:
        if not path.exists():
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    readme_text = read_markdown_file(Path("README.md"))

    readme_section = ""
    if readme_text:
        readme_json = json.dumps(readme_text)
        readme_section = f"""
    <section class=\"framed-section\" id=\"readme-section\">
        <h3>README</h3>
        <div id=\"readme-content\"></div>
        <script>
            const readmeMarkdown = {readme_json};
            const readmeTarget = document.getElementById('readme-content');
            if (readmeTarget) {{
                if (window.marked) {{
                    readmeTarget.innerHTML = marked.parse(readmeMarkdown);
                }} else {{
                    readmeTarget.textContent = readmeMarkdown;
                }}
            }}
        </script>
    </section>"""

    report_text = read_markdown_file(Path("output/comparison_report.md"))

    report_section = ""
    if report_text:
        report_json = json.dumps(report_text)
        report_section = f"""
    <section class=\"framed-section\" id=\"comparison-report-section\">
        <h3>Comparison Report</h3>
        <div id=\"comparison-report-content\"></div>
        <script>
            const reportMarkdown = {report_json};
            const reportTarget = document.getElementById('comparison-report-content');
            if (reportTarget) {{
                if (window.marked) {{
                    reportTarget.innerHTML = marked.parse(reportMarkdown);
                }} else {{
                    reportTarget.textContent = reportMarkdown;
                }}
            }}
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
        body { font-family: 'Segoe UI', sans-serif; padding: 110px 20px 20px 20px; background: #f4f4f9; }
        .site-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #f4f4f9;
            z-index: 1000;
            padding: 10px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        .site-header h1 { margin: 0; font-size: 1.4em; }
        .site-header .jump-links {
            margin-top: 8px;
            font-size: 0.95em;
        }
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

    <header class="site-header">
        <h1><a href="https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d">swissBOUNDARIES3D</a> <-> <a href="https://overpass-turbo.eu/s/2jcH">OpenStreetMap</a></h1>
        <div class="jump-links">
            <strong>Jump to:</strong>
            <a href="#table-section">Table</a> |
            <a href="#readme-section">README</a> |
            <a href="#comparison-report-section">Comparison Report</a> |
            <a href="#quality-map">Map</a> |
            <a href="#changes-plot">Plots</a>
        </div>
    </header>
    
    <p>
        Comparison of municipality boundaries of Switzerland and the Principality of Liechtenstein between official Swisstopo data (<a href="https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d">swissBOUNDARIES3D</a>) and <a href="https://www.openstreetmap.org/#map=9/46.823/7.880">OpenStreetMap</a>.<br>
        The table below shows the latest comparison results for each municipality, including metrics like IoU, area difference, Hausdorff distance, and more.<br>
        You can search, sort, and download the data in various formats.<br>
        For detailed explanations of the metrics and methodology, please refer to the README section below, which is directly pulled from <a href="https://github.com/habi/swissboundaries">the code repository</a>.<br>
        The bottom of the page shows a plot of the calculated metrics over time.
    </p>

    <section id="table-section">
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
    </section>

    __README_SECTION__
    __REPORT_SECTION__
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
                        {title: "Country", field: "Country"},
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
    html_content = html_content.replace("__REPORT_SECTION__", report_section)
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
        save_boundaries_as_geojson(
            swisstopo, "output/swisstopo_geojson", source_date=swisstopo_date
        )

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

        # Create index page for display
        create_index_page()

        print("\nComparison complete!")
    else:
        if swisstopo is None:
            print("ERROR: Failed to load SwissTopo data")
        if osm is None or len(osm) == 0:
            print("ERROR: Failed to retrieve OSM data")
        exit(1)
