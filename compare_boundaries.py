import geopandas as gpd
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import os
from pathlib import Path

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
    [out:json][timeout:90];
    area["ISO3166-1"="CH"][admin_level=2];
    (
      relation["boundary"="administrative"]["swisstopo:BFS_NUMMER"](area);
      way["boundary"="administrative"]["swisstopo:BFS_NUMMER"](area);
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
        
        # Convert to GeoDataFrame (OSM data is in WGS84)
        gdf = gpd.GeoDataFrame.from_features(geojson['features'], crs="EPSG:4326")
        
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
    """Create a GeoJSON feature from an OSM element."""
    
    properties = {
        'osm_id': element.get('id'),
        'osm_type': element.get('type'),
        **element.get('tags', {})
    }
    
    geometry = None
    
    # Handle ways
    if element['type'] == 'way' and 'geometry' in element:
        coords = [[node['lon'], node['lat']] for node in element['geometry']]
        
        if len(coords) > 2 and coords[0] == coords[-1]:
            geometry = {
                "type": "Polygon",
                "coordinates": [coords]
            }
        else:
            geometry = {
                "type": "LineString",
                "coordinates": coords
            }
    
    # Handle relations
    elif element['type'] == 'relation' and 'members' in element:
        outer_ways = []
        inner_ways = []
        
        for member in element['members']:
            if 'geometry' in member:
                coords = [[node['lon'], node['lat']] for node in member['geometry']]
                
                if member.get('role') == 'outer':
                    outer_ways.append(coords)
                elif member.get('role') == 'inner':
                    inner_ways.append(coords)
        
        if outer_ways:
            merged_outer = merge_ways(outer_ways)
            
            if merged_outer:
                merged_inners = []
                if inner_ways:
                    for inner_group in group_connected_ways(inner_ways):
                        merged_inner = merge_ways(inner_group)
                        if merged_inner:
                            merged_inners.append(merged_inner)
                
                geometry = {
                    "type": "Polygon",
                    "coordinates": [merged_outer] + merged_inners
                }
    
    if geometry:
        return {
            "type": "Feature",
            "properties": properties,
            "geometry": geometry
        }
    
    return None


def merge_ways(ways):
    """Merge multiple ways into a single closed ring."""
    if not ways:
        return None
    
    if len(ways) == 1:
        return ways[0]
    
    merged = list(ways[0])
    remaining = list(ways[1:])
    
    while remaining:
        added = False
        for i, way in enumerate(remaining):
            if merged[-1] == way[0]:
                merged.extend(way[1:])
                remaining.pop(i)
                added = True
                break
            elif merged[-1] == way[-1]:
                merged.extend(reversed(way[:-1]))
                remaining.pop(i)
                added = True
                break
            elif merged[0] == way[-1]:
                merged = way[:-1] + merged
                remaining.pop(i)
                added = True
                break
            elif merged[0] == way[0]:
                merged = list(reversed(way[1:])) + merged
                remaining.pop(i)
                added = True
                break
        
        if not added:
            break
    
    if merged[0] != merged[-1]:
        merged.append(merged[0])
    
    return merged


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


def load_swisstopo_municipalities(gpkg_path, target_crs="EPSG:2056"):
    """
    Load municipalities from swissBOUNDARIES3D GeoPackage.
    
    Args:
        gpkg_path: Path to the swissBOUNDARIES3D_1_5_LV95_LN02.gpkg file
        target_crs: Target coordinate reference system (default: WGS84)
    
    Returns:
        GeoDataFrame with municipalities
    """
    
    if not Path(gpkg_path).exists():
        print(f"Error: File not found: {gpkg_path}")
        return None
    
    print(f"Loading SwissTopo municipalities from: {gpkg_path}")
    
    try:
        # Read the municipalities layer
        gdf = gpd.read_file(gpkg_path, layer="tlm_hoheitsgebiet")
        print(f"  - Loaded {len(gdf)} total features")

        # Filter for Swiss municipalities only
        gdf = gdf[(gdf['objektart'] == 'Gemeindegebiet') & (gdf['icc'] == 'CH')].copy()
        
        print(f"  - Loaded {len(gdf)} Swiss municipalities")
        print(f"  - Original CRS: {gdf.crs}")
        
        # Reproject if needed
        if str(gdf.crs) != target_crs:
            gdf = gdf.to_crs(target_crs)
            print(f"  - Reprojected to: {target_crs}")
        
        print(f"  - Columns: {', '.join(gdf.columns)}")
        
        return gdf
        
    except Exception as e:
        print(f"Error loading SwissTopo data: {e}")
        return None


def save_boundaries_as_geojson(gdf, output_folder):
    """Save each boundary as individual GeoJSON files."""
    from shapely.geometry import mapping
    from shapely.ops import transform
    os.makedirs(output_folder, exist_ok=True)
    
    # Convert to WGS84 (EPSG:4326) for GeoJSON output
    # GeoJSON specification requires WGS84 coordinates (latitude/longitude)
    gdf_wgs84 = gdf.to_crs("EPSG:4326")
    
    # Function to strip Z coordinate
    def remove_z(geom):
        if geom.has_z:
            return transform(lambda x, y, z=None: (x, y), geom)
        return geom
    
    for idx, row in gdf_wgs84.iterrows():
        bfs_num = row['bfs_nummer']
        geom = row.geometry
        
        # Remove Z coordinate (elevation) if present - GeoJSON should be 2D
        geom_2d = remove_z(geom)
        
        feature = {
            "type": "Feature",
            "properties": {
                "bfs_nummer": bfs_num
            },
            "geometry": mapping(geom_2d)
        }
        geojson = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        output_path = os.path.join(output_folder, f"{bfs_num}.geojson")
        with open(output_path, 'w') as f:
            import json
            json.dump(geojson, f)
    
    print(f"Saved boundaries to {output_folder}")


def calculate_metrics(geom1, geom2):
    """Calculate comparison metrics in projected coordinates (EPSG:2056)"""
    try:
        # Debug: Check geometry properties
        # print(f"  Swisstopo geom: type={geom1.geom_type}, bounds={geom1.bounds}, area={geom1.area}")
        # print(f"  OSM geom: type={geom2.geom_type}, bounds={geom2.bounds}, area={geom2.area}")
        
        # Fix invalid geometries
        if not geom1.is_valid:
            print("  Fixing invalid Swisstopo geometry")
            geom1 = geom1.buffer(0)
        if not geom2.is_valid:
            print("  Fixing invalid OSM geometry")
            geom2 = geom2.buffer(0)
        
        if geom1.is_empty or geom2.is_empty:
            print("  Empty geometry detected")
            return None
        
        # Geometries are already in EPSG:2056 (loaded with target_crs="EPSG:2056")
        # No conversion needed - data is already in projected coordinates for accurate area calculations
        geom1_proj = geom1
        geom2_proj = geom2
        
        # print(f"    Calculating intersection...")
        intersection = geom1_proj.intersection(geom2_proj)
        # print(f"    Intersection: type={intersection.geom_type}, area={intersection.area}")
        
        # print(f"    Calculating union...")
        union = geom1_proj.union(geom2_proj)
        # print(f"    Union: type={union.geom_type}, area={union.area}")
        
        iou = intersection.area / union.area if union.area > 0 else 0
        # print(f"    IoU calculation: {intersection.area} / {union.area} = {iou}")
        
        area_diff = abs(geom1_proj.area - geom2_proj.area) / geom1_proj.area * 100 if geom1_proj.area > 0 else 0
        
        # Calculate Hausdorff distance with validation
        try:
            hausdorff = geom1_proj.hausdorff_distance(geom2_proj)
        except (ValueError, RuntimeWarning):
            hausdorff = float('nan')
        
        sym_diff_area = geom1_proj.symmetric_difference(geom2_proj).area
        sym_diff_pct = sym_diff_area / geom1_proj.area * 100 if geom1_proj.area > 0 else 0
        
        return {
            'iou': iou,
            'area_diff_pct': area_diff,
            'hausdorff_distance': hausdorff,
            'symmetric_diff_pct': sym_diff_pct,
            'swisstopo_area': geom1_proj.area,
            'osm_area': geom2_proj.area
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
        bfs_num = str(row['bfs_nummer'])
        
        if bfs_num in osm_lookup:
            metrics = calculate_metrics(
                row.geometry,
                osm_lookup[bfs_num])
            if metrics:
                osm_id = str(osm_gdf[osm_gdf['swisstopo:BFS_NUMMER'] == bfs_num]['osm_id'].values[0])
                results.append({
                    'name': name,
                    'bfs_nummer': bfs_num,
                    'relation': osm_id,
                    **metrics
                })
        else:
            results.append({
                'name': name,
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
        report_lines.append(f"  Mean Hausdorff distance: {matched_df['hausdorff_distance'].mean():.6f}°")
        
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
    csv_df.to_csv('output/detailed_results.csv',
                  header=['Name', 'BFS Number', 'OSM Relation', 'IoU', 'Area Diff (%)',
                          'Hausdorff Distance (°)', 'Symmetric Diff (%)',
                          'Area swisstopo (m²)', 'Area OSM (m²)'],
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
                        {title: "Name", field: "Name", width: 200},
                        {
                            title: "BFS Number", 
                            field: "BFS Number", 
                            width: 120,
                            formatter: function(cell, formatterParams, onRendered) {
                                var value = cell.getValue();
                                if (value) {
                                    return '<a href="https://raw.githubusercontent.com/habi/swissboundaries/refs/heads/main/output/swisstopo_geojson/' + value + '.geojson" target="_blank">' + value + '</a>';
                                }
                                return value;
                            }
                        },
                        {
                            title: "OSM Relation", 
                            field: "OSM Relation", 
                            width: 150,
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
                        {title: "IoU", field: "IoU", width: 100, formatter: "money", formatterParams: {precision: 4}},
                        {title: "Area Diff (%)", field: "Area Diff (%)", width: 130, formatter: "money", formatterParams: {precision: 2}},
                        {title: "Hausdorff Distance (°)", field: "Hausdorff Distance (°)", width: 180},
                        {title: "Symmetric Diff (%)", field: "Symmetric Diff (%)", width: 150, formatter: "money", formatterParams: {precision: 2}},
                        {title: "Area swisstopo (m²)", field: "Area swisstopo (m²)", width: 150, formatter: "money", formatterParams: {precision: 0}},
                        {title: "Area OSM (m²)", field: "Area OSM (m²)", width: 150, formatter: "money", formatterParams: {precision: 0}},
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


# Main execution
if __name__ == "__main__":
    # Create necessary directories
    for dir_name in ['history', 'output']:
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
        save_boundaries_as_geojson(swisstopo, 'output/swisstopo_geojson')

    if osm is not None and len(osm) > 0:
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
        print("ERROR: Failed to retrieve OSM data")
        exit(1)
