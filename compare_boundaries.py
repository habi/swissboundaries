import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union
import json
import requests
import time
from datetime import datetime
import folium
from folium import plugins
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import os

OVERPASS_URL = "http://overpass.osm.ch/api/interpreter"

def query_overpass_osm():
    """Query Overpass API for Swiss municipality boundaries"""
    print("Querying Overpass API for OSM boundaries...")
    
    overpass_query = """
    [out:json][timeout:300];
    area["ISO3166-1"="CH"][admin_level=2]->.switzerland;
    (
        relation["boundary"="administrative"]["admin_level"="8"]["swisstopo:BFS_NUMMER"](area.switzerland);
    );
    out geom;
    """
    
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3...")
            response = requests.post(
                OVERPASS_URL,
                data={'data': overpass_query},
                timeout=400
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"Retrieved {len(data.get('elements', []))} relations")
            
            features = []
            for element in data.get('elements', []):
                if element['type'] == 'relation':
                    tags = element.get('tags', {})
                    bfs_num = tags.get('swisstopo:BFS_NUMMER')
                    
                    if bfs_num and 'members' in element:
                        try:
                            coords = []
                            for member in element['members']:
                                if member['type'] == 'way' and member.get('role') == 'outer':
                                    way_coords = [(node['lon'], node['lat']) 
                                                for node in member.get('geometry', [])]
                                    if way_coords:
                                        coords.append(way_coords)
                            
                            if coords:
                                if len(coords) == 1:
                                    geom = Polygon(coords[0])
                                else:
                                    polygons = [Polygon(c) for c in coords if len(c) >= 3]
                                    geom = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]

                                geom = fix_geometry(geom)                                

                                feature = {
                                    'type': 'Feature',
                                    'properties': {
                                        'swisstopo:BFS_NUMMER': bfs_num,
                                        'name': tags.get('name', ''),
                                        'osm_id': element['id']
                                    },
                                    'geometry': mapping(geom)
                                }
                                features.append(feature)
                        except Exception as e:
                            print(f"Warning: Could not process relation {element['id']}: {e}")
            
            geojson = {'type': 'FeatureCollection', 'features': features}
            
            timestamp = datetime.now().strftime('%Y%m%d')
            with open(f'history/osm_boundaries_{timestamp}.geojson', 'w') as f:
                json.dump(geojson, f)
            
            gdf = gpd.GeoDataFrame.from_features(geojson, crs='EPSG:4326')

            print("Fixing OSM geometries...")
            gdf["geometry"] = gdf["geometry"].apply(fix_geometry)

            print(f"Successfully created GeoDataFrame with {len(gdf)} features")
            return gdf
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(30)
    
    return None

def load_swisstopo_data(gpkg_path):
    """Load official Swisstopo boundaries"""
    print("Loading Swisstopo data...")
    gdf = gpd.read_file(gpkg_path, layer="tlm_hoheitsgebiet")
    municipalities = gdf[(gdf['objektart'] == 'Gemeindegebiet') & (gdf['icc'] == 'CH')].copy()
    municipalities = municipalities.to_crs('EPSG:4326')
    print(f"Loaded {len(municipalities)} municipalities")
    return municipalities


def fix_geometry(geom):
    """Fix invalid geometries using buffer(0) and unary_union fallback."""
    if geom.is_valid:
        return geom

    # Try standard fix
    fixed = geom.buffer(0)
    if fixed.is_valid:
        return fixed

    # Fallback: explode, union, rebuild
    try:
        if isinstance(geom, (Polygon, MultiPolygon)):
            fixed = unary_union(geom)
            if fixed.is_valid:
                return fixed
    except:
        pass

    return geom  # last resort


def calculate_metrics(geom1, geom2):
    """Calculate comparison metrics"""
    try:
        geom1 = fix_geometry(geom1)
        geom2 = fix_geometry(geom2)

        intersection = geom1.intersection(geom2).area
        union = geom1.union(geom2).area
        iou = intersection / union if union > 0 else 0
        
        area_diff = abs(geom1.area - geom2.area) / geom1.area * 100
        hausdorff = geom1.hausdorff_distance(geom2)
        sym_diff_area = geom1.symmetric_difference(geom2).area
        sym_diff_pct = sym_diff_area / geom1.area * 100
        
        return {
            'iou': iou,
            'area_diff_pct': area_diff,
            'hausdorff_distance': hausdorff,
            'symmetric_diff_pct': sym_diff_pct,
            'swisstopo_area': geom1.area,
            'osm_area': geom2.area
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
        bfs_num = str(row['bfs_nummer'])
        name = row.get('name', row.get('NAME', 'Unknown'))
        
        if bfs_num in osm_lookup:
            metrics = calculate_metrics(fix_geometry(row.geometry), fix_geometry(osm_lookup[bfs_num]))
            if metrics:
                results.append({
                    'bfs_nummer': bfs_num,
                    'status': 'https://osm.org/relation/' + str(osm_gdf[osm_gdf['swisstopo:BFS_NUMMER'] == bfs_num]['osm_id'].values[0]),
                    **metrics
                })
        else:
            results.append({
                'bfs_nummer': bfs_num,
                'name': name,
                'status': 'Missing in OSM'
            })
    
    return pd.DataFrame(results)

def create_interactive_map(results_df, swisstopo_gdf):
    """Create interactive HTML map with Folium"""
    print("Creating interactive map...")
    
    # Center on Switzerland
    m = folium.Map(
        location=[46.8182, 8.2275],
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    # Add tile layers
    folium.TileLayer('CartoDB positron', name='CartoDB Positron').add_to(m)
    
    # Color mapping for quality
    def get_color(iou):
        if pd.isna(iou):
            return '#888888'  # Grey for missing
        elif iou >= 0.98:
            return '#2ecc71'  # Green - Excellent
        elif iou >= 0.95:
            return '#3498db'  # Blue - Good
        elif iou >= 0.90:
            return '#f39c12'  # Orange - Fair
        else:
            return '#e74c3c'  # Red - Poor
    
    # Create feature groups
    excellent_group = folium.FeatureGroup(name='Excellent (IoU ≥ 0.98)')
    good_group = folium.FeatureGroup(name='Good (IoU ≥ 0.95)')
    fair_group = folium.FeatureGroup(name='Fair (IoU ≥ 0.90)')
    poor_group = folium.FeatureGroup(name='Poor (IoU < 0.90)')
    missing_group = folium.FeatureGroup(name='Missing in OSM')
    
    # Add municipalities to appropriate groups
    for idx, row in results_df.iterrows():
        if pd.notna(row.get('geometry')):
            color = get_color(row.get('iou'))
            
            # Determine quality category
            iou = row.get('iou')
            if pd.isna(iou):
                group = missing_group
                quality = 'Missing in OSM'
            elif iou >= 0.98:
                group = excellent_group
                quality = 'Excellent'
            elif iou >= 0.95:
                group = good_group
                quality = 'Good'
            elif iou >= 0.90:
                group = fair_group
                quality = 'Fair'
            else:
                group = poor_group
                quality = 'Poor'
            
            # Create popup
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="margin: 0 0 10px 0;">{row['name']}</h4>
                <table style="width: 100%; font-size: 12px;">
                    <tr><td><b>BFS Number:</b></td><td>{row['bfs_nummer']}</td></tr>
                    <tr><td><b>Quality:</b></td><td><span style="color: {color}; font-weight: bold;">{quality}</span></td></tr>
            """
            
            if pd.notna(iou):
                popup_html += f"""
                    <tr><td><b>IoU:</b></td><td>{iou:.4f}</td></tr>
                    <tr><td><b>Area Diff:</b></td><td>{row['area_diff_pct']:.2f}%</td></tr>
                    <tr><td><b>Sym. Diff:</b></td><td>{row['symmetric_diff_pct']:.2f}%</td></tr>
                    <tr><td><b>Hausdorff:</b></td><td>{row['hausdorff_distance']:.6f}°</td></tr>
                """
            
            popup_html += """
                </table>
            </div>
            """
            
            # Add to map
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'color': color,
                    'weight': 2,
                    'fillOpacity': 0.4
                },
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(group)
    
    # Add all groups to map
    excellent_group.add_to(m)
    good_group.add_to(m)
    fair_group.add_to(m)
    poor_group.add_to(m)
    missing_group.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 180px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
        <p style="margin: 0 0 10px 0; font-weight: bold;">Quality Legend</p>
        <p style="margin: 5px 0;"><span style="color: #2ecc71;">⬤</span> Excellent (IoU ≥ 0.98)</p>
        <p style="margin: 5px 0;"><span style="color: #3498db;">⬤</span> Good (IoU ≥ 0.95)</p>
        <p style="margin: 5px 0;"><span style="color: #f39c12;">⬤</span> Fair (IoU ≥ 0.90)</p>
        <p style="margin: 5px 0;"><span style="color: #e74c3c;">⬤</span> Poor (IoU < 0.90)</p>
        <p style="margin: 5px 0;"><span style="color: #888888;">⬤</span> Missing in OSM</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save('docs/boundary_comparison_map.html')
    print("Interactive map saved to docs/boundary_comparison_map.html")

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
        fig_iou.write_html('docs/iou_trend.html')
        
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
        fig_quality.write_html('docs/quality_distribution.html')
        
        print("Trend visualizations saved")
    else:
        print("Not enough historical data for trends (need at least 2 data points)")    

def generate_report(results_df, historical_df):
    """Generate comparison report"""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("SWISS MUNICIPALITY BOUNDARY COMPARISON REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    report_lines.append("=" * 80)
    
    total = len(results_df)
    matched = results_df['iou'].notna().sum()
    missing = total - matched
    
    report_lines.append(f"\nDataset Overview:")
    report_lines.append(f"  Total Swisstopo municipalities: {total}")
    report_lines.append(f"  Matched in OSM: {matched} ({matched/total*100:.1f}%)")
    report_lines.append(f"  Missing in OSM: {missing} ({missing/total*100:.1f}%)")
    
    if matched > 0:
        matched_df = results_df[results_df['iou'].notna()]
        
        report_lines.append(f"\nAccuracy Metrics (for matched municipalities):")
        report_lines.append(f"  Mean IoU: {matched_df['iou'].mean():.4f}")
        report_lines.append(f"  Median IoU: {matched_df['iou'].median():.4f}")
        report_lines.append(f"  Mean area difference: {matched_df['area_diff_pct'].mean():.2f}%")
        report_lines.append(f"  Mean symmetric difference: {matched_df['symmetric_diff_pct'].mean():.2f}%")
        report_lines.append(f"  Mean Hausdorff distance: {matched_df['hausdorff_distance'].mean():.6f}°")
        
        excellent = (matched_df['iou'] >= 0.98).sum()
        good = ((matched_df['iou'] >= 0.95) & (matched_df['iou'] < 0.98)).sum()
        fair = ((matched_df['iou'] >= 0.90) & (matched_df['iou'] < 0.95)).sum()
        poor = (matched_df['iou'] < 0.90).sum()
        
        report_lines.append(f"\nQuality Distribution:")
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
        
        report_lines.append(f"\nWorst 10 Matches (by IoU):")
        worst = matched_df.nsmallest(10, 'iou')[['name', 'bfs_nummer', 'iou', 'area_diff_pct']]
        report_lines.append(worst.to_string(index=False))
        
        report_lines.append(f"\nMost Improved (if historical data available):")
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
    missing_df = results_df[results_df['status'] == 'Missing in OSM']
    if len(missing_df) > 0:
        report_lines.append(f"\nMissing Municipalities (showing first 20):")
        missing_list = missing_df.head(20)[['name', 'bfs_nummer']]
        report_lines.append(missing_list.to_string(index=False))
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # Save reports
    with open('reports/comparison_report.txt', 'w') as f:
        f.write(report_text)
    
    # Save CSV (without geometry columns for CSV)
    csv_df = results_df.drop(columns=['geometry', 'osm_geometry'], errors='ignore')
    csv_df.to_csv('reports/detailed_results.csv', index=False)
    
    # Save to history
    timestamp = datetime.now().strftime('%Y%m%d')
    csv_df.to_csv(f'history/results_{timestamp}.csv', index=False)
    
    return results_df

def create_dashboard_index():
    """Create main dashboard HTML file"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Swiss Municipality Boundary Comparison Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
            }
            .header p {
                margin: 10px 0 0 0;
                font-size: 1.2em;
                opacity: 0.9;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .card {
                background: white;
                border-radius: 8px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .card h2 {
                margin-top: 0;
                color: #333;
            }
            .button {
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin: 10px 10px 10px 0;
                transition: background 0.3s;
            }
            .button:hover {
                background: #5568d3;
            }
            .iframe-container {
                position: relative;
                width: 100%;
                padding-bottom: 75%;
                margin: 20px 0;
            }
            .iframe-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .stat {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗺️ Swiss Municipality Boundary Comparison</h1>
            <p>Comparing Swisstopo official data with OpenStreetMap</p>
        </div>
        
        <div class="container">
            <div class="card">
                <h2>📊 Interactive Visualizations</h2>
                <p>Explore the comparison data through interactive maps and charts:</p>
                <a href="boundary_comparison_map.html" class="button">🗺️ Interactive Boundary Map</a>
                <a href="iou_trend.html" class="button">📈 Quality Trend Over Time</a>
                <a href="quality_distribution.html" class="button">📊 Quality Distribution Timeline</a>
            </div>
            
            <div class="card">
                <h2>🗺️ Boundary Comparison Map</h2>
                <p>Click on municipalities to see detailed comparison metrics. Use the layer controls to filter by quality.</p>
                <div class="iframe-container">
                    <iframe src="boundary_comparison_map.html"></iframe>
                </div>
            </div>
            
            <div class="card">
                <h2>📈 Historical Trends</h2>
                <p>Track how boundary quality has improved over time:</p>
                <div class="iframe-container">
                    <iframe src="iou_trend.html"></iframe>
                </div>
            </div>
            
            <div class="card">
                <h2>📥 Download Reports</h2>
                <p>Access detailed comparison data:</p>
                <a href="../reports/comparison_report.txt" class="button">📄 Summary Report</a>
                <a href="../reports/detailed_results.csv" class="button">📊 Detailed CSV Data</a>
            </div>
            
            <div class="card">
                <h2>ℹ️ About</h2>
                <p>This dashboard automatically compares Swiss municipality boundaries between official Swisstopo data and OpenStreetMap. The comparison runs monthly to track data quality improvements over time.</p>
                <p><strong>Quality Categories:</strong></p>
                <ul>
                    <li><span style="color: #2ecc71;">⬤ Excellent:</span> IoU ≥ 0.98 (boundaries match almost perfectly)</li>
                    <li><span style="color: #3498db;">⬤ Good:</span> IoU ≥ 0.95 (minor differences)</li>
                    <li><span style="color: #f39c12;">⬤ Fair:</span> IoU ≥ 0.90 (noticeable differences)</li>
                    <li><span style="color: #e74c3c;">⬤ Poor:</span> IoU < 0.90 (significant discrepancies)</li>
                    <li><span style="color: #888888;">⬤ Missing:</span> Not yet mapped in OpenStreetMap</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('docs/index.html', 'w') as f:
        f.write(html_content)
    
    print("Dashboard index created")

# Main execution
if __name__ == "__main__":
    # Create necessary directories
    for dir_name in ['reports', 'history', 'docs']:
        os.makedirs(dir_name, exist_ok=True)
    
    # Load data
    swisstopo = load_swisstopo_data('swissBOUNDARIES3D_1_5_LV95_LN02.gpkg')
    osm = query_overpass_osm()
    
    if osm is not None and len(osm) > 0:
        # Compare boundaries
        results = compare_boundaries(swisstopo, osm)
        
        # Load historical data
        historical = load_historical_data()
        
        # Generate report
        report = generate_report(results, historical)
        
        # Create visualizations
        create_interactive_map(results, swisstopo)
        create_trend_visualizations(results, historical)
        create_dashboard_index()
        
        print("\nComparison complete! Check the docs/ folder for interactive visualizations.")
    else:
        print("ERROR: Failed to retrieve OSM data")
        exit(1)
