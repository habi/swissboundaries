Generated: 2026-09-01 07:21:18 UTC

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
| Mean IoU                  | 0.9998 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.006% |
| Mean symmetric difference | 0.022% |
| Mean Hausdorff distance   | 1.2261 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-31)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.006% |
| Current mean area difference     |   0.006% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.244 |
| Current mean Hausdorff distance  |   1.226 |
| Hausdorff change                 |  -0.018 |

## Worst 10 Matches (by IoU)

| name            |   bfs_nummer |      iou |   area_diff_pct |
|:----------------|-------------:|---------:|----------------:|
| Eschenz         |         4806 | 0.981541 |     1.52918     |
| Dozwil          |         4406 | 0.996898 |     0.103515    |
| Prévonloup      |         5683 | 0.997366 |     0.0700191   |
| Lovatens        |         5674 | 0.997373 |     0.0372413   |
| Obergerlafingen |         2528 | 0.997484 |     0.0485894   |
| Chêne-Pâquier   |         5908 | 0.99773  |     0.0210398   |
| Willadingen     |          423 | 0.997933 |     0.0548498   |
| Gy              |         6624 | 0.997952 |     0.0613426   |
| Vich            |         5732 | 0.997957 |     0.000700454 |
| Hersberg        |         2827 | 0.997983 |     0.0583234   |

## Most Improved (if historical data available)

| name     |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:---------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Mauensee |         1091 |   0.998365 |   0.999994 |    0.00162912 |    1682895 |
| Sursee   |         1103 |   0.998922 |   0.999995 |    0.00107268 |    1682923 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name     |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:---------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Cormoret |          432 |    1682413 | https://www.openstreetmap.org/relation/1682413 | https://www.openstreetmap.org/?mlat=47.132918&mlon=7.058290#map=16/47.132918/7.058290 |              3.702 |             21.191 |       17.489 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Nods     |          724 |    1682582 | https://www.openstreetmap.org/relation/1682582 | https://www.openstreetmap.org/?mlat=47.132918&mlon=7.058290#map=16/47.132918/7.058290 |              3.9   |             21.191 |       17.291 | https://www.openstreetmap.org/changeset/44224658  | nyuriks          | 2016-12-07T02:43:59Z  |

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