# Swiss Municipality Boundary Comparison

Comparison of Swiss municipality boundaries between official Swisstopo data ([swissBOUNDARIES3D](https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d)) and [OpenStreetMap](https://www.openstreetmap.org/#map=9/46.823/7.880)

This repository uses the ideas presented in https://github.com/stalker314314/osm-admin-boundary-conflation and support from Claude.ai, ChatGPT and Google Gemini to produce a report on the matching of the official swisstopo boundaries to the boundaries mapped in OpenStreetMap.

The initial prompts to Claude.ai were:

> I have the boundaries of the swiss municipalities in https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2025-04/swissboundaries3d_2025-04_2056_5728.gpkg.zip.
> Help me produce a report on how well these match geographically with the boundaries mapped in OpenStreetMap, preferrably via Overpass Turbo.
> The boundaries in the geopackage have `bfs_nummer=355`, the boundaries in OSM have `swisstopo:BFS_NUMMER=355` as a matching ID.

> Can you query Overpass in Python, too?

> Can you make this all work in a GitHub action?
----

## Latest Results

You can check the [latest comparison results](https://github.com/habi/swissboundaries/blob/main/output/detailed_results.csv), or view the most recent run summary in [the Actions tab].
The latest results are shown as a (searchable) table on http://boundaries.osm.ch/
Historic data is saved as CSV files to the [history](./history/) directory.

## Automation

- **Schedule**: Runs daily at 2 AM UTC via a [GitHub Action](https://github.com/habi/swissboundaries/blob/main/.github/workflows/compare-boundaries.yml)
- **Manual Trigger**: Can be triggered manually from the Actions tab
- **Data Sources**:
  - Official: [Swisstopo SwissBOUNDARIES3D](https://www.swisstopo.admin.ch/en/geodata/landscape/boundaries3d.html)
  - Community: OpenStreetMap via Overpass API

## Metrics

The comparison calculates:

- **[IoU (Intersection over Union)](https://github.com/habi/swissboundaries/blob/1157cd462a9c157f0ee31245e4305265c1474e74/compare_boundaries.py#L260)**: Measures boundary overlap quality (1.0 = perfect match).
- **[Area Difference](https://github.com/habi/swissboundaries/blob/1157cd462a9c157f0ee31245e4305265c1474e74/compare_boundaries.py#L261)**: Percentage deviation in total area
- **[Hausdorff Distance](https://github.com/habi/swissboundaries/blob/1157cd462a9c157f0ee31245e4305265c1474e74/compare_boundaries.py#L269)**: Maximum distance between boundary points
- **[Symmetric Difference](https://github.com/habi/swissboundaries/blob/1157cd462a9c157f0ee31245e4305265c1474e74/compare_boundaries.py#L262)**: Amount of non-overlapping area

## 🚀 Running Locally

```bash
# Install dependencies
pip install geopandas shapely pandas requests pyogrio

# Download and extract Swisstopo data
# If you do this manually, get the freshest version available on https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d
# The workflow file in the GitHub repo downloads the newest one via the swisstopo API: https://github.com/habi/swissboundaries/blob/main/.github/workflows/compare-boundaries.yml
wget https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip
unzip swissboundaries3d*.zip

# Run comparison (use the script from the GitHub Action)
python compare_boundaries.py
```

## Output Files

- [`output/comparison_report.txt`](http://boundaries.osm.ch/comparison_report.txt): Human-readable summary report
- [`output/detailed_results.csv`](http://boundaries.osm.ch/detailed_results.csv): Per-municipality metrics in CSV format.
  This file is shown at the top of the page at http://boundaries.osm.ch/

## Contributing

Contributions are welcome! If you find boundary discrepancies:

1. Check the detailed results to identify problematic municipalities
2. Verify the boundaries in OpenStreetMap
3. Improve OSM data if needed using JOSM or iD editor
4. The next automated run will reflect your improvements

## Matching Criteria

Boundaries are matched using:

- **Swisstopo**: `bfs_nummer` field (official BFS municipality number)
- **OpenStreetMap**: `swisstopo:BFS_NUMMER` tag

## License

Data sources:

- Swisstopo data: [Terms of Use](https://www.swisstopo.admin.ch/en/home/meta/conditions/geodata/ogd.html)
- OpenStreetMap data: [ODbL](https://www.openstreetmap.org/copyright)

## Links

- [Swisstopo Geodata Portal](https://www.swisstopo.admin.ch/en/geodata-portal)
- [OpenStreetMap Switzerland](https://www.openstreetmap.ch/)
- [Swiss Overpass API](http://overpass.osm.ch/)
