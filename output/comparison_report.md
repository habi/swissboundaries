Generated: 2026-09-22 07:23:52 UTC

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
| Mean IoU                  | 0.9999 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.003% |
| Mean symmetric difference | 0.008% |
| Mean Hausdorff distance   | 0.5789 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-21)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.003% |
| Current mean area difference     |   0.003% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.589 |
| Current mean Hausdorff distance  |   0.579 |
| Hausdorff change                 |  -0.010 |

## Worst 10 Matches (by IoU)

| name          |   bfs_nummer |      iou |   area_diff_pct |
|:--------------|-------------:|---------:|----------------:|
| Eschenz       |         4806 | 0.982101 |      1.5445     |
| Prévonloup    |         5683 | 0.997366 |      0.0700191  |
| Chêne-Pâquier |         5908 | 0.99773  |      0.0210398  |
| Willadingen   |          423 | 0.997933 |      0.0548498  |
| Hellsau       |          408 | 0.998087 |      0.0493622  |
| Bettingen     |         2702 | 0.998261 |      0.0699435  |
| Lovatens      |         5674 | 0.998371 |      0.0597391  |
| Finsterhennen |          493 | 0.998379 |      0.013268   |
| Egolzwil      |         1127 | 0.998399 |      0.0015237  |
| Wasterkingen  |           70 | 0.998502 |      0.00389107 |

## Most Improved (if historical data available)

| name           |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:---------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Curtilles      |         5669 |   0.998576 |   0.999995 |    0.00141827 |    1684939 |
| Starrkirch-Wil |         2584 |   0.998902 |   0.999991 |    0.00108893 |    1683578 |

## Most Deteriorated (if historical data available)

| name                     |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_iou |   curr_iou |   deterioration | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-----------:|-----------:|----------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Walliswil bei Niederbipp |          990 |    1682712 | https://www.openstreetmap.org/relation/1682712 | https://www.openstreetmap.org/?mlat=47.228228&mlon=7.714260#map=16/47.228228/7.714260 |    0.99999 |   0.998847 |      0.00114275 | https://www.openstreetmap.org/changeset/185557201 | habi             | 2026-07-11T19:49:40Z  |

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name                     |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Bannwil                  |          323 |    1682370 | https://www.openstreetmap.org/relation/1682370 | https://www.openstreetmap.org/?mlat=47.228228&mlon=7.714260#map=16/47.228228/7.714260 |              0.015 |             30.209 |       30.194 | https://www.openstreetmap.org/changeset/187696558 | SimonPoole       | 2026-08-19T15:18:36Z  |
| Walliswil bei Niederbipp |          990 |    1682712 | https://www.openstreetmap.org/relation/1682712 | https://www.openstreetmap.org/?mlat=47.228228&mlon=7.714260#map=16/47.228228/7.714260 |              0.008 |             12.635 |       12.627 | https://www.openstreetmap.org/changeset/185557201 | habi             | 2026-07-11T19:49:40Z  |

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