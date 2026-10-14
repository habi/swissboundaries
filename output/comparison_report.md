Generated: 2026-10-14 07:09:42 UTC

## Dataset Overview

| Metric                         | Value |
|--------------------------------|------:|
| Total Swisstopo municipalities |  2123 |
| Matched in OSM                 |  2123 |
| Missing in OSM                 |     0 |
| Only in OSM (not in Swisstopo) |     9 |

## Accuracy Metrics (for matched municipalities)

| Metric                    | Value  |
|---------------------------|--------|
| Mean IoU                  | 1.0000 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.001% |
| Mean symmetric difference | 0.002% |
| Mean Hausdorff distance   | 0.2800 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-10-13)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.001% |
| Current mean area difference     |   0.001% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.299 |
| Current mean Hausdorff distance  |   0.280 |
| Hausdorff change                 |  -0.019 |

## Worst 10 Matches (by IoU)

| name         |   bfs_nummer |      iou |   area_diff_pct |
|:-------------|-------------:|---------:|----------------:|
| Eschenz      |         4806 | 0.982101 |      1.5445     |
| Lalden       |         6286 | 0.999085 |      0.0372583  |
| Urmein       |         3670 | 0.9992   |      0.0672536  |
| Choulex      |         6614 | 0.999326 |      0.002777   |
| Oppligen     |          622 | 0.999331 |      0.0214784  |
| Kiesen       |          611 | 0.999333 |      0.0126941  |
| Prévondavaux |         2038 | 0.999389 |      0.00192274 |
| Vandoeuvres  |         6642 | 0.999405 |      0.00271839 |
| Münchenwiler |          669 | 0.999413 |      0.0045179  |
| Flerden      |         3662 | 0.999429 |      0.047769   |

## Most Improved (if historical data available)

| name               |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:-------------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Romanel-sur-Morges |         5645 |   0.998662 |   0.999989 |    0.00132738 |    1685126 |
| Wiggiswil          |          553 |   0.998797 |   0.99999  |    0.00119341 |    1682722 |
| Brenzikofen        |          606 |   0.998841 |   0.999994 |    0.00115282 |    1682390 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name   |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Porza  |         5214 |    1684741 | https://www.openstreetmap.org/relation/1684741 | https://www.openstreetmap.org/?mlat=46.026216&mlon=8.965209#map=16/46.026216/8.965209 |              0.015 |              2.853 |        2.838 | https://www.openstreetmap.org/changeset/179395429 | SimonPoole       | 2026-03-05T12:54:23Z  |
| Lugano |         5192 |    2888417 | https://www.openstreetmap.org/relation/2888417 | https://www.openstreetmap.org/?mlat=46.026216&mlon=8.965209#map=16/46.026216/8.965209 |              1.08  |              2.853 |        1.773 | https://www.openstreetmap.org/changeset/182692765 | Yan Bakhmat      | 2026-05-15T11:10:36Z  |

## BFS numbers only in OSM (not in Swisstopo) (showing first 20):

| name                            |   bfs_nummer |   relation |
|:--------------------------------|-------------:|-----------:|
| Staatswald Galm                 |         2391 |    1683405 |
| Comunanza Cadenazzo/Monteceneri |         5391 |    1684666 |
| Comunanza Capriasca/Lugano      |         5394 |    1684667 |
| Thunersee                       |         9073 |    1682683 |
| Brienzersee                     |         9089 |    1682392 |
| Bielersee (BE)                  |         9149 |    1682381 |
| Bielersee (NE)                  |         9150 |    1685453 |
| Lac de Neuchâtel (BE)           |         9152 |   18625441 |
| Lac de Neuchâtel (NE)           |         9155 |    1685500 |