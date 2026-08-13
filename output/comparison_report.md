Generated: 2026-08-13 04:13:46 UTC

## Dataset Overview

| Metric                         | Value |
|--------------------------------|------:|
| Total Swisstopo municipalities |  2123 |
| Matched in OSM                 |  2121 |
| Missing in OSM                 |     2 |
| Only in OSM (not in Swisstopo) |     9 |

## Accuracy Metrics (for matched municipalities)

| Metric                    | Value  |
|---------------------------|--------|
| Mean IoU                  | 0.9996 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.009% |
| Mean symmetric difference | 0.037% |
| Mean Hausdorff distance   | 1.7935 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-12)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.009% |
| Current mean area difference     |   0.009% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.827 |
| Current mean Hausdorff distance  |   1.794 |
| Hausdorff change                 |  -0.034 |

## Worst 10 Matches (by IoU)

| name            |   bfs_nummer |      iou |   area_diff_pct |
|:----------------|-------------:|---------:|----------------:|
| Eschenz         |         4806 | 0.981348 |       1.54249   |
| Dozwil          |         4406 | 0.996898 |       0.103515  |
| Dättlikon       |          215 | 0.997101 |       0.0819724 |
| Borex           |         5706 | 0.997201 |       0.0270045 |
| Prévonloup      |         5683 | 0.997366 |       0.0700191 |
| Lovatens        |         5674 | 0.997373 |       0.0372413 |
| Masein          |         3663 | 0.997455 |       0.0107846 |
| Obergerlafingen |         2528 | 0.997484 |       0.0485894 |
| Jaberg          |          868 | 0.997524 |       0.0534641 |
| Chêne-Bourg     |         6613 | 0.997545 |       0.149029  |

## Most Improved (if historical data available)

| name            |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:----------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Oberengstringen |          245 |   0.997905 |   0.99999  |    0.00208447 |    1682176 |
| Ipsach          |          739 |   0.998453 |   0.999992 |    0.00153886 |    1682494 |
| Port            |          745 |   0.998514 |   0.999991 |    0.00147699 |    1682609 |
| Weesen          |         3316 |   0.998611 |   0.999994 |    0.00138258 |    1683963 |
| Nidau           |          743 |   0.998878 |   0.999991 |    0.0011126  |    1682573 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name       |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Buchs (SG) |         3271 |    1683869 | https://www.openstreetmap.org/relation/1683869 | https://www.openstreetmap.org/?mlat=47.158983&mlon=9.493800#map=16/47.158983/9.493800 |              0.016 |             15.288 |       15.272 | https://www.openstreetmap.org/changeset/180952632 | SimonPoole       | 2026-04-06T15:06:25Z  |
| Schaan     |         7005 |    1155952 | https://www.openstreetmap.org/relation/1155952 | https://www.openstreetmap.org/?mlat=47.112380&mlon=9.622924#map=16/47.112380/9.622924 |              2.046 |             15.288 |       13.242 | https://www.openstreetmap.org/changeset/185461449 | SimonPoole       | 2026-07-10T09:05:06Z  |

## BFS numbers only in Swisstopo (missing in OSM) (showing first 20):
| name                  |   bfs_nummer |
|:----------------------|-------------:|
| Büsingen am Hochrhein |         7101 |
| Campione d'Italia     |         7301 |

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