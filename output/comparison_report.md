Generated: 2026-07-10 06:05:47 UTC

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
| Mean IoU                  | 0.9993 |
| Median IoU                | 0.9996 |
| Mean area difference      | 0.012% |
| Mean symmetric difference | 0.066% |
| Mean Hausdorff distance   | 3.7757 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2119 |     99.906 |
| IoU ≥ 0.95 |     2 |      0.094 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-09)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean Hausdorff distance |   3.776 |
| Current mean Hausdorff distance  |   3.776 |
| Hausdorff change                 |  +0.000 |

## Worst 10 Matches (by IoU)

| name         |   bfs_nummer |      iou |   area_diff_pct |
|:-------------|-------------:|---------:|----------------:|
| Schellenberg |         7011 | 0.969995 |       0.0607881 |
| Gamprin      |         7009 | 0.977739 |       0.0666107 |
| Eschen       |         7007 | 0.98084  |       0.127358  |
| Eschenz      |         4806 | 0.981348 |       1.54249   |
| Planken      |         7006 | 0.98298  |       0.171595  |
| Mauren       |         7008 | 0.98507  |       0.162911  |
| Vaduz        |         7001 | 0.989127 |       0.167184  |
| Schaan       |         7005 | 0.990377 |       0.192447  |
| Ruggell      |         7010 | 0.991607 |       0.115829  |
| Triesenberg  |         7004 | 0.993716 |       0.20695   |

## Most Improved (if historical data available)

| name    |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:--------|-------------:|-----------:|-----------:|--------------:|
| Gamprin |         7009 |   0.973196 |   0.977739 |    0.00454324 |
| Eschen  |         7007 |   0.979042 |   0.98084  |    0.00179798 |

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