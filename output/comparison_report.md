Generated: 2026-08-20 02:58:00 UTC

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
| Mean IoU                  | 0.9997 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.007% |
| Mean symmetric difference | 0.030% |
| Mean Hausdorff distance   | 1.5112 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-19)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.007% |
| Current mean area difference     |   0.007% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.541 |
| Current mean Hausdorff distance  |   1.511 |
| Hausdorff change                 |  -0.030 |

## Worst 10 Matches (by IoU)

| name            |   bfs_nummer |      iou |   area_diff_pct |
|:----------------|-------------:|---------:|----------------:|
| Eschenz         |         4806 | 0.981348 |       1.54249   |
| Dozwil          |         4406 | 0.996898 |       0.103515  |
| Borex           |         5706 | 0.997201 |       0.0270045 |
| Prévonloup      |         5683 | 0.997366 |       0.0700191 |
| Lovatens        |         5674 | 0.997373 |       0.0372413 |
| Obergerlafingen |         2528 | 0.997484 |       0.0485894 |
| Chêne-Bourg     |         6613 | 0.997545 |       0.149029  |
| Crassier        |         5714 | 0.997672 |       0.147564  |
| Chêne-Pâquier   |         5908 | 0.99773  |       0.0210398 |
| Gurbrü          |          665 | 0.997743 |       0.0243696 |

## Most Improved (if historical data available)

| name             |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:-----------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Bannwil          |          323 |   0.998312 |   0.999994 |    0.0016825  |    1682370 |
| Vucherens        |         5692 |   0.998351 |   0.999994 |    0.00164334 |    1685197 |
| Teuffenthal (BE) |          940 |   0.998463 |   0.999994 |    0.00153097 |    1682680 |
| Cuarnens         |         5479 |   0.998734 |   0.999995 |    0.00126168 |    1684934 |
| Syens            |         5688 |   0.998827 |   0.999992 |    0.00116531 |    1685159 |
| Fahy             |         6789 |   0.998854 |   0.999997 |    0.00114254 |    1685599 |
| Moiry            |         5490 |   0.998893 |   0.999996 |    0.00110306 |    1685050 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

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