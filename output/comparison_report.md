Generated: 2026-09-30 08:05:17 UTC

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
| Mean area difference      | 0.002% |
| Mean symmetric difference | 0.006% |
| Mean Hausdorff distance   | 0.4663 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-29)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.002% |
| Current mean area difference     |   0.002% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.478 |
| Current mean Hausdorff distance  |   0.466 |
| Hausdorff change                 |  -0.011 |

## Worst 10 Matches (by IoU)

| name               |   bfs_nummer |      iou |   area_diff_pct |
|:-------------------|-------------:|---------:|----------------:|
| Eschenz            |         4806 | 0.982101 |     1.5445      |
| Prévonloup         |         5683 | 0.997366 |     0.0700191   |
| Bettingen          |         2702 | 0.998261 |     0.0699435   |
| Lovatens           |         5674 | 0.998371 |     0.0597391   |
| Willadingen        |          423 | 0.998632 |     2.82363e-05 |
| Romanel-sur-Morges |         5645 | 0.998662 |     0.0979852   |
| Finsterhennen      |          493 | 0.9987   |     0.0147253   |
| Hellsau            |          408 | 0.998749 |     0.0152137   |
| Wiggiswil          |          553 | 0.998797 |     0.0462724   |
| Höchstetten        |          410 | 0.998831 |     0.0257002   |

## Most Improved (if historical data available)

| name     |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:---------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Egolzwil |         1127 |   0.998399 |   0.999993 |    0.00159374 |    1682827 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name   |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Horgen |          295 |    1682144 | https://www.openstreetmap.org/relation/1682144 | https://www.openstreetmap.org/?mlat=47.253450&mlon=8.620531#map=16/47.253450/8.620531 |              0.016 |              3.977 |        3.961 | https://www.openstreetmap.org/changeset/186758808 | SimonPoole       | 2026-08-01T11:47:59Z  |

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