Generated: 2026-08-17 03:00:40 UTC

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
| Mean area difference      | 0.008% |
| Mean symmetric difference | 0.033% |
| Mean Hausdorff distance   | 1.6224 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-16)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.008% |
| Current mean area difference     |   0.008% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.654 |
| Current mean Hausdorff distance  |   1.622 |
| Hausdorff change                 |  -0.031 |

## Worst 10 Matches (by IoU)

| name             |   bfs_nummer |      iou |   area_diff_pct |
|:-----------------|-------------:|---------:|----------------:|
| Eschenz          |         4806 | 0.981348 |       1.54249   |
| Dozwil           |         4406 | 0.996898 |       0.103515  |
| Borex            |         5706 | 0.997201 |       0.0270045 |
| Prévonloup       |         5683 | 0.997366 |       0.0700191 |
| Lovatens         |         5674 | 0.997373 |       0.0372413 |
| Obergerlafingen  |         2528 | 0.997484 |       0.0485894 |
| Chêne-Bourg      |         6613 | 0.997545 |       0.149029  |
| Crassier         |         5714 | 0.997672 |       0.147564  |
| Rüti bei Lyssach |          422 | 0.997693 |       0.0357847 |
| Chêne-Pâquier    |         5908 | 0.99773  |       0.0210398 |

## Most Improved (if historical data available)

| name                        |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:----------------------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Deisswil bei Münchenbuchsee |          535 |   0.997951 |   0.999989 |    0.00203823 |    1682418 |
| Auswil                      |          322 |   0.998522 |   0.999993 |    0.00147094 |    1682368 |
| Zuzwil (BE)                 |          557 |   0.998052 |   0.999158 |    0.00110567 |    1682738 |

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