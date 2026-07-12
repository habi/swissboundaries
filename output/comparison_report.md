Generated: 2026-07-12 05:30:43 UTC

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
| Mean IoU                  | 0.9994 |
| Median IoU                | 0.9997 |
| Mean area difference      | 0.011% |
| Mean symmetric difference | 0.057% |
| Mean Hausdorff distance   | 3.1161 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-11)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean Hausdorff distance |   3.134 |
| Current mean Hausdorff distance  |   3.116 |
| Hausdorff change                 |  -0.018 |

## Worst 10 Matches (by IoU)

| name           |   bfs_nummer |      iou |   area_diff_pct |
|:---------------|-------------:|---------:|----------------:|
| Eschenz        |         4806 | 0.981348 |      1.54249    |
| Rueyres        |         5534 | 0.995282 |      0.0684165  |
| Hagneck        |          736 | 0.995824 |      0.00469874 |
| Regensberg     |           95 | 0.996442 |      0.0295773  |
| Kilchberg (BL) |         2851 | 0.9965   |      0.0323861  |
| Känerkinden    |         2850 | 0.996793 |      0.0345198  |
| Fürstenau      |         3633 | 0.996862 |      0.00192794 |
| Dozwil         |         4406 | 0.996898 |      0.103515   |
| Tecknau        |         2862 | 0.996983 |      0.036558   |
| Kammersrohr    |         2549 | 0.996999 |      0.0526844  |

## Most Improved (if historical data available)

| name                     |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:-------------------------|-------------:|-----------:|-----------:|--------------:|
| Walliswil bei Niederbipp |          990 |   0.996749 |   0.99999  |    0.00324115 |
| Madulain                 |         3783 |   0.998198 |   0.999735 |    0.00153743 |
| Zuoz                     |         3791 |   0.998732 |   0.999939 |    0.00120665 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name   |   bfs_nummer |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m |
|:-------|-------------:|-------------------:|-------------------:|-------------:|
| Binn   |         6054 |              0.016 |              2.352 |        2.336 |

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