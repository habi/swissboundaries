Generated: 2026-09-04 07:00:11 UTC

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
| Mean symmetric difference | 0.019% |
| Mean Hausdorff distance   | 1.1187 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-03)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.006% |
| Current mean area difference     |   0.006% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.162 |
| Current mean Hausdorff distance  |   1.119 |
| Hausdorff change                 |  -0.043 |

## Worst 10 Matches (by IoU)

| name          |   bfs_nummer |      iou |   area_diff_pct |
|:--------------|-------------:|---------:|----------------:|
| Eschenz       |         4806 | 0.982101 |     1.5445      |
| Dozwil        |         4406 | 0.996898 |     0.103515    |
| Prévonloup    |         5683 | 0.997366 |     0.0700191   |
| Lovatens      |         5674 | 0.997373 |     0.0372413   |
| Chêne-Pâquier |         5908 | 0.99773  |     0.0210398   |
| Willadingen   |          423 | 0.997933 |     0.0548498   |
| Gy            |         6624 | 0.997952 |     0.0613426   |
| Vich          |         5732 | 0.997957 |     0.000700454 |
| Giebenach     |         2826 | 0.998    |     0.00184768  |
| Dänikon       |           85 | 0.998079 |     0.0359194   |

## Most Improved (if historical data available)

| name                |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:--------------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Obergerlafingen     |         2528 |   0.997484 |   0.999989 |    0.00250512 |    1683562 |
| Niederönz           |          982 |   0.998182 |   0.999993 |    0.00181023 |    1682580 |
| Berken              |          972 |   0.998222 |   0.999991 |    0.00176909 |    1682377 |
| Inkwil              |          980 |   0.998464 |   0.999993 |    0.00152949 |    1682490 |
| Heimenhausen        |          977 |   0.998553 |   0.999995 |    0.00144155 |    1682473 |
| Bolken              |         2514 |   0.998708 |   0.999993 |    0.00128419 |    1683485 |
| Gachnang            |         4571 |   0.998729 |   0.999996 |    0.00126728 |    1684523 |
| Sils im Domleschg   |         3640 |   0.998731 |   0.999994 |    0.00126299 |    1684168 |
| Ellikon an der Thur |          218 |   0.998827 |   0.999994 |    0.00116717 |    1682116 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## BFS numbers only in Swisstopo (missing in OSM) (showing first 20):
| name       |   bfs_nummer |
|:-----------|-------------:|
| Hallau     |         2971 |
| Wilchingen |         2974 |

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

## Municipalities whose swisstopo:BFS_NUMMER tag was removed from OSM (2):
  • Hallau (BFS 2971)  — OSM relation: https://www.openstreetmap.org/relation/1683654
  • Wilchingen (BFS 2974)  — OSM relation: https://www.openstreetmap.org/relation/1683721