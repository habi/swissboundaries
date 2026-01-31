import geopandas as gpd
import pandas as pd
import requests
import json
import os
from datetime import datetime
from pathlib import Path
from shapely.geometry import mapping, MultiLineString
from shapely.ops import polygonize, unary_union
import plotly.graph_objects as go

def load_osm_boundaries(target_crs="EPSG:2056"):
    """
    Query Overpass API for Swiss boundaries with swisstopo:BFS_NUMMER.
    
    Args:
        target_crs: Target coordinate reference system (default: WGS84)
    
    Returns:
        GeoDataFrame with OSM boundaries
    """
    
    print("Querying Overpass API for OSM boundaries...")
    
    # Overpass QL query
    overpass_query = """
    [out:json][timeout:120];
    area["ISO3166-1"="CH"][admin_level=2]->.switzerland;
    (
      relation["boundary"="administrative"]["swisstopo:BFS_NUMMER"](area.switzerland);
    );
    out geom;
    """
    
    try:
        response = requests.post(
            "http://overpass.osm.ch/api/interpreter",
            data=overpass_query,
            timeout=120
        )
        response.raise_for_status()
        
        osm_data = response.json()
        
        if not osm_data.get('elements'):
            print("  - No boundaries found with swisstopo:BFS_NUMMER tag")
            return None
        
        print(f"  - Found {len(osm_data['elements'])} OSM elements")
        
        # Convert to GeoJSON
        geojson = osm_to_geojson(osm_data)
          
        if not geojson['features']:
            print("  - Error: No valid features created from OSM data")
            return None
            
        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geojson['features'], crs="EPSG:4326")
        
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
    
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for element in osm_data.get('elements', []):
        feature = create_feature(element)
        if feature:
            geojson['features'].append(feature)
    
    return geojson


def create_feature(element):
    """Convert OSM element to Polygon/MultiPolygon for Area Metrics."""
    e_type = element.get('type')
    tags = element.get('tags', {})
    bfs_num = tags.get('swisstopo:BFS_NUMMER')

    if e_type == 'relation':
        member_geoms = []
        for member in element.get('members', []):
            if member.get('type') == 'way' and 'geometry' in member:
                # out geom provides the geometry list directly
                points = [[pt['lon'], pt['lat']] for pt in member['geometry']]
                member_geoms.append(points)
        
        if not member_geoms:
            return None

        # To get Area Metrics, we must polygonize the lines
        mls = MultiLineString(member_geoms)
        polygons = list(polygonize(mls))
        
        if polygons:
            final_geom = unary_union(polygons)
        else:
            # If it won't polygonize, we can't do area metrics effectively
            return None

        return {
            "type": "Feature",
            "id": f"relation/{element['id']}",
            "properties": {
                "osm_id": element['id'],
                "swisstopo:BFS_NUMMER": bfs_num,
                **tags
            },
            "geometry": mapping(final_geom)
        }
    return None


def load_swisstopo_municipalities(shp_path, target_crs="EPSG:2056"):
    """Load municipalities from local shapefile as Polygons to preserve Area Metrics."""
    try:
        print(f"Loading SwissTopo shapefile from {shp_path}...")
        
        # Read the shapefile
        gdf = gpd.read_file(shp_path)
        
        # Filter for municipalities (Gemeindegebiet) in Switzerland
        if 'objektart' in gdf.columns and 'icc' in gdf.columns:
            gdf = gdf[(gdf['objektart'] == 'Gemeindegebiet') & (gdf['icc'] == 'CH')].copy()
        else:
            # If columns don't exist, just use all features
            print("  - Note: Could not filter by objektart/icc, using all features")
        
        # Ensure correct CRS
        if gdf.crs != target_crs:
            gdf = gdf.to_crs(target_crs)
        
        # Force 2D immediately
        gdf.geometry = gdf.geometry.apply(force_2d)
        
        # Ensure geometries are valid for area calculations
        gdf.geometry = gdf.geometry.make_valid()
        
        print(f"  - Loaded {len(gdf)} municipalities from shapefile")
        print(f"  - Columns: {', '.join(gdf.columns)}")
        
        return gdf
    except Exception as e:
        print(f"Error loading SwissTopo shapefile: {e}")
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
                    if (way[0] == group_way[0] or way[0] == group_way[-1] or
                        way[-1] == group_way[0] or way[-1] == group_way[-1]):
                        current_group.append(remaining.pop(i))
                        changed = True
                        break
        
        groups.append(current_group)
    
    return groups


def save_boundaries_as_geojson(gdf, output_folder):
    """Saves Polygons as a FeatureCollection of individual LineString segments."""
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure we are in WGS84 for GeoJSON standard
    gdf_wgs84 = gdf.to_crs("EPSG:4326")

    for bfs_num, group in gdf_wgs84.groupby('bfs_nummer'):
        features = []
        
        for _, row in group.iterrows():
            # 1. Get the boundary (this turns Polygon -> LineString/MultiLineString)
            boundary = row.geometry.boundary
            
            # 2. EXPLOSION LOGIC: Break into individual parts
            # Handles MultiLineStrings (multiple rings/exclaves)
            if hasattr(boundary, 'geoms'):
                parts = list(boundary.geoms)
            else:
                parts = [boundary]

            for part in parts:
                # 3. Create a unique feature for every single segment
                # This ensures the GeoJSON is a collection of lines, not one big one
                features.append({
                    "type": "Feature",
                    "properties": {
                        "bfs_nummer": int(bfs_num),
                        "segment_length_m": row.geometry.length if hasattr(row.geometry, 'length') else 0
                    },
                    "geometry": mapping(part)
                })
        
        # 4. Wrap everything in a FeatureCollection
        geojson_output = {
            "type": "FeatureCollection",
            "features": features
        }
        
        file_path = os.path.join(output_folder, f"{int(bfs_num)}.geojson")
        with open(file_path, 'w') as f:
            json.dump(geojson_output, f, indent=2)

    print(f"  - Successfully saved {len(gdf_wgs84['bfs_nummer'].unique())} exploded GeoJSON files.")


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
            area_diff = abs(geom1.area - geom2.area) / geom1.area * 100 if geom1.area > 0 else 0
            sym_diff_area = geom1.symmetric_difference(geom2).area
            sym_diff_pct = sym_diff_area / geom1.area * 100 if geom1.area > 0 else 0
        else: # For Lines, Area metrics are meaningless
            iou = area_diff = sym_diff_pct = float('nan')

        # Distance metrics, helpful for conflation
        try:
            hausdorff = geom1.hausdorff_distance(geom2)
        except:
            hausdorff = float('nan')

        return {
            'iou': iou,
            'area_diff_pct': area_diff,
            'hausdorff_distance': hausdorff,
            'symmetric_diff_pct': sym_diff_pct,
            'swisstopo_area': geom1.area,
            'osm_area': geom2.area,
            'geom_type': geom1.geom_type
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None


def compare_boundaries(swisstopo_gdf, osm_gdf):
    """Compare matching boundaries"""
    print("Comparing boundaries...")
    
    results = []
    osm_lookup = {}
    
    for idx, row in osm_gdf.iterrows():
        bfs_num = row.get('swisstopo:BFS_NUMMER')
        if bfs_num:
            osm_lookup[str(bfs_num)] = row.geometry
    
    print(f"OSM lookup contains {len(osm_lookup)} municipalities")
    
    for idx, row in swisstopo_gdf.iterrows():
        name = row.get('name', row.get('NAME', 'Unknown'))        
        bfs_num = int(row['bfs_nummer'])
        kantonsnummer = int(row.get('kantonsnummer')) if pd.notna(row.get('kantonsnummer')) else None
        bezirksnummer = int(row.get('bezirksnummer')) if pd.notna(row.get('bezirksnummer')) else None
        
        if str(bfs_num) in osm_lookup:
            metrics = calculate_metrics(
                row.geometry,
                osm_lookup[str(bfs_num)])
            if metrics:
                osm_id = str(osm_gdf[osm_gdf['swisstopo:BFS_NUMMER'] == str(bfs_num)]['osm_id'].values[0])
                results.append({
                    'name': name,
                    'bfs_nummer': bfs_num,
                    'kantonsnummer': kantonsnummer,
                    'bezirksnummer': bezirksnummer,
                    'relation': osm_id,
                    **metrics
                })
        else:
            results.append({
                'name': name,
                'kantonsnummer': kantonsnummer,                
                'bezirksnummer': bezirksnummer,                
                'bfs_nummer': bfs_num,
                'relation': ''
            })
    
    return pd.DataFrame(results)


def compare_dataframes(gdf_swisstopo, gdf_osm):
    """Compare the two GeoDataFrames."""
    
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)
    
    print("\nSwissTopo:")
    print(f"  - Features: {len(gdf_swisstopo)}")
    print(f"  - CRS: {gdf_swisstopo.crs}")
    print(f"  - Bounds: {gdf_swisstopo.total_bounds}")
    
    print("\nOSM:")
    print(f"  - Features: {len(gdf_osm)}")
    print(f"  - CRS: {gdf_osm.crs}")
    print(f"  - Bounds: {gdf_osm.total_bounds}")
    
    # Check for BFS_NUMMER overlap
    if 'BFS_NUMMER' in gdf_swisstopo.columns and 'swisstopo:BFS_NUMMER' in gdf_osm.columns:
        swisstopo_bfs = set(gdf_swisstopo['BFS_NUMMER'].astype(str))
        osm_bfs = set(gdf_osm['swisstopo:BFS_NUMMER'].astype(str))
        
        common = swisstopo_bfs & osm_bfs
        only_swisstopo = swisstopo_bfs - osm_bfs
        only_osm = osm_bfs - swisstopo_bfs
        
        print("\nBFS_NUMMER comparison:")
        print(f"  - In both datasets: {len(common)}")
        print(f"  - Only in SwissTopo: {len(only_swisstopo)}")
        print(f"  - Only in OSM: {len(only_osm)}")



def load_historical_data():
    """Load historical comparison data"""
    history_dir = 'history'
    if not os.path.exists(history_dir):
        return pd.DataFrame()
    
    csv_files = sorted([f for f in os.listdir(history_dir) if f.startswith('results_') and f.endswith('.csv')])
    
    if not csv_files:
        return pd.DataFrame()
    
    historical_data = []
    for csv_file in csv_files:
        date_str = csv_file.replace('results_', '').replace('.csv', '')
        try:
            df = pd.read_csv(os.path.join(history_dir, csv_file))
            df['date'] = pd.to_datetime(date_str)
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
    current_results['date'] = current_date
    
    if len(historical_df) > 0:
        all_data = pd.concat([historical_df, current_results], ignore_index=True)
    else:
        all_data = current_results
    
    # Calculate summary statistics by date
    summary = all_data.groupby('date').agg({
        'iou': ['mean', 'median', 'count'],
        'area_diff_pct': 'mean',
        'symmetric_diff_pct': 'mean'
    }).reset_index()
    
    summary.columns = ['date', 'mean_iou', 'median_iou', 'count', 'mean_area_diff', 'mean_sym_diff']
    
    # Calculate quality distribution over time
    quality_over_time = []
    for date in all_data['date'].unique():
        date_data = all_data[all_data['date'] == date]
        matched = date_data['iou'].notna()
        matched_data = date_data[matched]
        
        if len(matched_data) > 0:
            quality_over_time.append({
                'date': date,
                'Excellent': (matched_data['iou'] >= 0.98).sum(),
                'Good': ((matched_data['iou'] >= 0.95) & (matched_data['iou'] < 0.98)).sum(),
                'Fair': ((matched_data['iou'] >= 0.90) & (matched_data['iou'] < 0.95)).sum(),
                'Poor': (matched_data['iou'] < 0.90).sum(),
                'Missing': (~matched).sum()
            })
    
    quality_df = pd.DataFrame(quality_over_time)
    
    # Create interactive Plotly charts
    if len(summary) > 1:
        # IoU trend chart
        fig_iou = go.Figure()
        fig_iou.add_trace(go.Scatter(
            x=summary['date'], y=summary['mean_iou'],
            mode='lines+markers',
            name='Mean IoU',
            line=dict(color='#3498db', width=3)
        ))
        fig_iou.add_trace(go.Scatter(
            x=summary['date'], y=summary['median_iou'],
            mode='lines+markers',
            name='Median IoU',
            line=dict(color='#2ecc71', width=3, dash='dash')
        ))
        fig_iou.update_layout(
            title='Boundary Quality Trend (IoU Over Time)',
            xaxis_title='Date',
            yaxis_title='Intersection over Union (IoU)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        fig_iou.write_html('output/iou_trend.html')
        
        # Quality distribution stacked area chart
        fig_quality = go.Figure()
        colors = {'Excellent': '#2ecc71', 'Good': '#3498db', 'Fair': '#f39c12', 'Poor': '#e74c3c', 'Missing': '#888888'}
        
        for quality in ['Excellent', 'Good', 'Fair', 'Poor', 'Missing']:
            if quality in quality_df.columns:
                fig_quality.add_trace(go.Scatter(
                    x=quality_df['date'],
                    y=quality_df[quality],
                    mode='lines',
                    name=quality,
                    stackgroup='one',
                    fillcolor=colors[quality],
                    line=dict(width=0.5, color=colors[quality])
                ))
        
        fig_quality.update_layout(
            title='Quality Distribution Over Time',
            xaxis_title='Date',
            yaxis_title='Number of Municipalities',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        fig_quality.write_html('output/quality_distribution.html')
        
        print("Trend visualizations saved")
    else:
        print("Not enough historical data for trends (need at least 2 data points)")    


def generate_report(results_df, historical_df):
    """Generate comparison report"""
    report_lines = []
    report_lines.append("Swiss municipality boundary comparison report")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    total = len(results_df)
    matched = results_df['iou'].notna().sum()
    missing = total - matched
    
    report_lines.append("\nDataset Overview:")
    report_lines.append("  Total Swisstopo municipalities: {total}")
    report_lines.append(f"  Matched in OSM: {matched} ({matched/total*100:.1f}%)")
    report_lines.append(f"  Missing in OSM: {missing} ({missing/total*100:.1f}%)")
    
    if matched > 0:
        matched_df = results_df[results_df['iou'].notna()]
        
        report_lines.append("\nAccuracy Metrics (for matched municipalities):")
        report_lines.append(f"  Mean IoU: {matched_df['iou'].mean():.4f}")
        report_lines.append(f"  Median IoU: {matched_df['iou'].median():.4f}")
        report_lines.append(f"  Mean area difference: {matched_df['area_diff_pct'].mean():.2f}%")
        report_lines.append(f"  Mean symmetric difference: {matched_df['symmetric_diff_pct'].mean():.2f}%")
        report_lines.append(f"  Mean Hausdorff distance: {matched_df['hausdorff_distance'].mean():.6f}m")
        
        excellent = (matched_df['iou'] >= 0.98).sum()
        good = ((matched_df['iou'] >= 0.95) & (matched_df['iou'] < 0.98)).sum()
        fair = ((matched_df['iou'] >= 0.90) & (matched_df['iou'] < 0.95)).sum()
        poor = (matched_df['iou'] < 0.90).sum()
        
        report_lines.append("\nQuality Distribution:")
        report_lines.append(f"  Excellent (IoU ≥ 0.98): {excellent} ({excellent/matched*100:.1f}%)")
        report_lines.append(f"  Good (IoU ≥ 0.95): {good} ({good/matched*100:.1f}%)")
        report_lines.append(f"  Fair (IoU ≥ 0.90): {fair} ({fair/matched*100:.1f}%)")
        report_lines.append(f"  Poor (IoU < 0.90): {poor} ({poor/matched*100:.1f}%)")
        
        # Historical comparison
        if len(historical_df) > 0:
            prev_date = historical_df['date'].max()
            prev_data = historical_df[historical_df['date'] == prev_date]
            prev_matched = prev_data['iou'].notna()
            
            if prev_matched.sum() > 0:
                prev_mean_iou = prev_data[prev_matched]['iou'].mean()
                current_mean_iou = matched_df['iou'].mean()
                iou_change = current_mean_iou - prev_mean_iou
                
                report_lines.append(f"\nHistorical Comparison (vs {prev_date.strftime('%Y-%m-%d')}):")
                report_lines.append(f"  Previous mean IoU: {prev_mean_iou:.4f}")
                report_lines.append(f"  Current mean IoU: {current_mean_iou:.4f}")
                report_lines.append(f"  Change: {iou_change:+.4f} ({iou_change/prev_mean_iou*100:+.2f}%)")
        
        report_lines.append("\nWorst 10 Matches (by IoU):")
        worst = matched_df.nsmallest(10, 'iou')[['name', 'bfs_nummer', 'iou', 'area_diff_pct']]
        report_lines.append(worst.to_string(index=False))
        
        report_lines.append("\nMost Improved (if historical data available):")
        if len(historical_df) > 0:
            # Find municipalities that improved
            prev_date = historical_df['date'].max()
            prev_data = historical_df[historical_df['date'] == prev_date].set_index('bfs_nummer')
            
            improvements = []
            for idx, row in matched_df.iterrows():
                bfs = row['bfs_nummer']
                if bfs in prev_data.index and pd.notna(prev_data.loc[bfs, 'iou']):
                    prev_iou = prev_data.loc[bfs, 'iou']
                    curr_iou = row['iou']
                    improvement = curr_iou - prev_iou
                    if improvement > 0.001:  # Significant improvement
                        improvements.append({
                            'name': row['name'],
                            'bfs_nummer': bfs,
                            'prev_iou': prev_iou,
                            'curr_iou': curr_iou,
                            'improvement': improvement
                        })
            
            if improvements:
                imp_df = pd.DataFrame(improvements).nlargest(10, 'improvement')
                report_lines.append(imp_df.to_string(index=False))
            else:
                report_lines.append("  No significant improvements detected")
        else:
            report_lines.append("  (Insufficient historical data)")
    
    # Missing municipalities
    missing_df = results_df[results_df['relation'] == 'Not found in OSM']
    if len(missing_df) > 0:
        report_lines.append("\nMissing Municipalities (showing first 20):")
        missing_list = missing_df.head(20)[['name', 'bfs_nummer']]
        report_lines.append(missing_list.to_string(index=False))
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # Save reports
    with open('output/comparison_report.txt', 'w') as f:
        f.write(report_text)

    # Save CSV (without geometry columns for CSV)
    csv_df = results_df.drop(columns=['geometry', 'osm_geometry'], errors='ignore')
    
    # Convert bfs_nummer, kantonsnummer, and bezirksnummer to integer
    csv_df['bfs_nummer'] = csv_df['bfs_nummer'].astype('Int64')  # Int64 handles NaN values
    csv_df['kantonsnummer'] = csv_df['kantonsnummer'].astype('Int64')
    csv_df['bezirksnummer'] = csv_df['bezirksnummer'].astype('Int64')
    
    # Reorder columns
    column_order = ['name', 'relation', 'bfs_nummer', 'bezirksnummer', 'kantonsnummer', 
                    'iou', 'area_diff_pct', 'hausdorff_distance', 'symmetric_diff_pct',
                    'swisstopo_area', 'osm_area', 'geom_type']
    csv_df = csv_df[[col for col in column_order if col in csv_df.columns]]
    
    csv_df.to_csv('output/detailed_results.csv',
                  header=[
                      'Name', 'OSM Relation', 'BFS Number', 'Bezirksnummer', 'Kantonsnummer',
                      'IoU', 'Area Diff [%]',
                      'Hausdorff Distance [m]', 'Symmetric Diff [%]',
                      'Area swisstopo [m²]', 'Area OSM [m²]', 'Geometry Type'
                  ],
                  index=False)

    # Save to history
    timestamp = datetime.now().strftime('%Y%m%d')
    csv_df.to_csv(f'history/results_{timestamp}.csv', index=False)
    
    return results_df


def create_csv_table_page():
    """Create HTML to display CSV table"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>swissBOUNDARIES3D <-> OpenStreetMap</title>
    <link href="https://unpkg.com/tabulator-tables@5.5.0/dist/css/tabulator.min.css" rel="stylesheet">
    <script src="https://unpkg.com/tabulator-tables@5.5.0/dist/js/tabulator.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
    
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
    </style>
</head>
<body>

    <h2><a href="https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d">swissBOUNDARIES3D</a> <-> <a href="https://overpass-turbo.eu/s/2jcH">OpenStreetMap</a></h2>
    
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
                        {title: "Area Diff [%]", field: "Area Diff [%]", formatter: "money", formatterParams: {precision: 2}},
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
    
    with open('output/index.html', 'w') as f:
        f.write(html_content)
    
    print("CSV table page created")


if __name__ == "__main__":
    # Create necessary directories
    for dir_name in ['history', 'output']:
        os.makedirs(dir_name, exist_ok=True)
    
    # Load data - shapefile should be provided by workflow
    shp_path = "swissBOUNDARIES3D_1_5_TLM_HOHEITSGEBIET.shp"
    target_crs = "EPSG:2056"  # https://epsg.io/2056
    swisstopo = load_swisstopo_municipalities(shp_path, target_crs)
    osm = load_osm_boundaries(target_crs)

    # Compare if both loaded successfully
    if swisstopo is not None and osm is not None:
        compare_dataframes(swisstopo, osm)

    # Save out swisstopo boundaries as individual geoJSON files
    if swisstopo is not None:
        save_boundaries_as_geojson(swisstopo, 'output/swisstopo_geojson')

    if swisstopo is not None and osm is not None and len(osm) > 0:
        # Compare boundaries
        results = compare_boundaries(swisstopo, osm)
        
        # Load historical data
        historical = load_historical_data()
        
        # Generate report
        report = generate_report(results, historical)
        create_trend_visualizations(results, historical)

        # Create inde page for display
        create_csv_table_page()
                
        print("\nComparison complete!")
    else:
        if swisstopo is None:
            print("ERROR: Failed to load SwissTopo data")
        if osm is None or len(osm) == 0:
            print("ERROR: Failed to retrieve OSM data")
        exit(1)
