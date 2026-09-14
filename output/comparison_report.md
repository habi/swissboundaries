Generated: 2026-09-14 07:37:41 UTC

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
| Mean area difference      | 0.004% |
| Mean symmetric difference | 0.013% |
| Mean Hausdorff distance   | 0.8141 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-13)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.004% |
| Current mean area difference     |   0.004% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.881 |
| Current mean Hausdorff distance  |   0.814 |
| Hausdorff change                 |  -0.067 |

## Worst 10 Matches (by IoU)

| name          |   bfs_nummer |      iou |   area_diff_pct |
|:--------------|-------------:|---------:|----------------:|
| Eschenz       |         4806 | 0.982101 |      1.5445     |
| Prévonloup    |         5683 | 0.997366 |      0.0700191  |
| Lovatens      |         5674 | 0.997373 |      0.0372413  |
| Chêne-Pâquier |         5908 | 0.99773  |      0.0210398  |
| Willadingen   |          423 | 0.997933 |      0.0548498  |
| Giebenach     |         2826 | 0.998    |      0.00184768 |
| Hellsau       |          408 | 0.998087 |      0.0493622  |
| Rümlingen     |         2859 | 0.998115 |      0.0180965  |
| Bettingen     |         2702 | 0.998261 |      0.0699435  |
| Studen (BE)   |          749 | 0.998329 |      0.0299392  |

## Most Improved (if historical data available)

| name        |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Henniez     |         5819 |   0.997866 |   0.999554 |    0.00168873 |    1685001 |
| Ramlinsburg |         2832 |   0.998383 |   0.999993 |    0.00160999 |    1683691 |
| Lully (VD)  |         5639 |   0.99891  |   0.999989 |    0.00107876 |    1685036 |
| Hölstein    |         2886 |   0.998959 |   0.999995 |    0.00103645 |    1683659 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

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

## Resolved: swisstopo:BFS_NUMMER tag restored in OSM (2):
  • Isenthal (BFS 1211)  — first detected: 2026-09-13  — OSM relation: https://www.openstreetmap.org/relation/1683085
  • Wolfenschiessen (BFS 1511)  — first detected: 2026-09-13  — OSM relation: https://www.openstreetmap.org/relation/1683122