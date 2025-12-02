# swissboundaries
Matching boundaries from swissBOUNDARIES3D to OpenStreetMap

This repository used the ideas presented in https://github.com/stalker314314/osm-admin-boundary-conflation and Claude.ai to produce a report on the matching.

The intital prompt to Claude.ai was

> I have the boundaries of the swiss municipalities in https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2025-04/swissboundaries3d_2025-04_2056_5728.gpkg.zip.
> Help me produce a report on how well these match geographically with the boundaries mapped in OpenStreetMap, preferrably via Overpass Turbo.
> The boundaries in the geopackage have `bfs_nummer=355`, the boundaries in OSM have `swisstopo:BFS_NUMMER=355` as a matching ID.

> Can you query Overpass in Python, too?

> Can you make this all work in a GitHub action?
----
# Swiss Municipality Boundary Comparison

Automated comparison of Swiss municipality boundaries between official Swisstopo data and OpenStreetMap.

## 🎯 Purpose

This repository automatically compares the geographic accuracy of municipality boundaries in OpenStreetMap against the official Swiss Swisstopo boundaries. It runs monthly to track OpenStreetMap data quality over time.

## 📊 Latest Results

Check the [reports](./reports/) directory for the latest comparison results, or view the Actions tab for the most recent run summary.

## 🔄 Automation

- **Schedule**: Runs automatically on the 1st of each month at 2 AM UTC
- **Manual Trigger**: Can be triggered manually from the Actions tab
- **Data Sources**:
  - Official: [Swisstopo SwissBOUNDARIES3D](https://www.swisstopo.admin.ch/en/geodata/landscape/boundaries3d.html)
  - Community: OpenStreetMap via Overpass API

## 📈 Metrics

The comparison calculates:

- **IoU (Intersection over Union)**: Measures boundary overlap quality (1.0 = perfect match)
- **Area Difference**: Percentage deviation in total area
- **Hausdorff Distance**: Maximum distance between boundary points
- **Symmetric Difference**: Amount of non-overlapping area

### Quality Categories

- **Excellent**: IoU ≥ 0.98
- **Good**: IoU ≥ 0.95
- **Fair**: IoU ≥ 0.90
- **Poor**: IoU < 0.90

## 🚀 Running Locally
```bash
# Install dependencies
pip install geopandas shapely pandas requests pyogrio

# Download and extract Swisstopo data
wget https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2025-04/swissboundaries3d_2025-04_2056_5728.gpkg.zip
unzip swissboundaries3d_2025-04_2056_5728.gpkg.zip

# Run comparison (use the script from the GitHub Action)
python compare_boundaries.py
```

## 📁 Output Files

- `reports/comparison_report.txt`: Human-readable summary report
- `reports/detailed_results.csv`: Per-municipality metrics in CSV format
- `osm_boundaries.geojson`: Downloaded OSM boundaries for inspection

## 🤝 Contributing

Contributions are welcome! If you find boundary discrepancies:

1. Check the detailed results to identify problematic municipalities
2. Verify the boundaries in OpenStreetMap
3. Improve OSM data if needed using JOSM or iD editor
4. The next automated run will reflect your improvements

## 📝 Matching Criteria

Boundaries are matched using:
- **Swisstopo**: `bfs_nummer` field (official BFS municipality number)
- **OpenStreetMap**: `swisstopo:BFS_NUMMER` tag

## ⚖️ License

Data sources:
- Swisstopo data: [Terms of Use](https://www.swisstopo.admin.ch/en/home/meta/conditions/geodata/ogd.html)
- OpenStreetMap data: [ODbL](https://www.openstreetmap.org/copyright)

## 🔗 Links

- [Swisstopo Geodata Portal](https://www.swisstopo.admin.ch/en/geodata-portal)
- [OpenStreetMap Switzerland](https://www.openstreetmap.ch/)
- [Overpass API](https://overpass-api.de/)
