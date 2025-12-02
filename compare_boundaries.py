import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union
import json
import requests
import time
from datetime import datetime

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
            
            with open('osm_boundaries.geojson', 'w') as f:
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
    municipalities = gdf[gdf['objektart'] == 'Gemeindegebiet'].copy()
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
                    'name': name,
                    **metrics
                })
        else:
            results.append({
                'bfs_nummer': bfs_num,
                'name': name,
                'status': 'Missing in OSM'
            })
    
    return pd.DataFrame(results)

def generate_report(results_df):
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
        
        report_lines.append(f"\nWorst 10 Matches (by IoU):")
        worst = matched_df.nsmallest(10, 'iou')[['name', 'bfs_nummer', 'iou', 'area_diff_pct']]
        report_lines.append(worst.to_string(index=False))
    
    # Missing municipalities
    missing_df = results_df[results_df['status'] == 'Missing in OSM']
    if len(missing_df) > 0:
        report_lines.append(f"\nMissing Municipalities (showing first 20):")
        missing_list = missing_df.head(20)[['name', 'bfs_nummer']]
        report_lines.append(missing_list.to_string(index=False))
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # Save report
    with open('reports/comparison_report.txt', 'w') as f:
        f.write(report_text)
    
    # Save CSV
    results_df.to_csv('reports/detailed_results.csv', index=False)
    
    return results_df

# Main execution
if __name__ == "__main__":
    import os
    os.makedirs('reports', exist_ok=True)
    
    swisstopo = load_swisstopo_data('swissBOUNDARIES3D_1_5_LV95_LN02.gpkg')
    osm = query_overpass_osm()
    
    if osm is not None and len(osm) > 0:
        results = compare_boundaries(swisstopo, osm)
        report = generate_report(results)
        print("\nComparison complete!")
    else:
        print("ERROR: Failed to retrieve OSM data")
        exit(1)
