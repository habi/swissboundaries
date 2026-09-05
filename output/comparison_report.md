Generated: 2026-09-05 06:44:36 UTC

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
| Mean IoU                  | 0.9998 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.005% |
| Mean symmetric difference | 0.018% |
| Mean Hausdorff distance   | 1.0851 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-04)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.006% |
| Current mean area difference     |   0.005% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.119 |
| Current mean Hausdorff distance  |   1.085 |
| Hausdorff change                 |  -0.034 |

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
| Rongellen     |         3711 | 0.998083 |     0.00449142  |

## Most Improved (if historical data available)

| name        |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Puplinge    |         6636 |   0.998129 |   0.999993 |    0.0018633  |    1685526 |
| Flurlingen  |           29 |   0.998132 |   0.999992 |    0.00185916 |    1682124 |
| Feuerthalen |           27 |   0.998732 |   0.999991 |    0.00125903 |    1682121 |
| Presinge    |         6635 |   0.998783 |   0.999994 |    0.00121012 |    1685525 |
| Dörflingen  |         2915 |   0.998889 |   0.999995 |    0.00110652 |    1683644 |
| Buchs (ZH)  |           83 |   0.998955 |   0.999994 |    0.00103939 |    1682098 |

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
  • Hallau (BFS 2971)  — first detected: 2026-09-04  — OSM relation: https://www.openstreetmap.org/relation/1683654
  • Wilchingen (BFS 2974)  — first detected: 2026-09-04  — OSM relation: https://www.openstreetmap.org/relation/1683721