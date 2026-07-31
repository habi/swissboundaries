Generated: 2026-07-31 05:37:34 UTC

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
| Mean IoU                  | 0.9995 |
| Median IoU                | 0.9999 |
| Mean area difference      | 0.010% |
| Mean symmetric difference | 0.049% |
| Mean Hausdorff distance   | 2.3036 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-30)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.330 |
| Current mean Hausdorff distance  |   2.304 |
| Hausdorff change                 |  -0.026 |

## Worst 10 Matches (by IoU)

| name         |   bfs_nummer |      iou |   area_diff_pct |
|:-------------|-------------:|---------:|----------------:|
| Eschenz      |         4806 | 0.981348 |     1.54249     |
| Hagneck      |          736 | 0.995824 |     0.00469874  |
| Regensberg   |           95 | 0.996442 |     0.0295773   |
| Känerkinden  |         2850 | 0.996793 |     0.0345198   |
| Fürstenau    |         3633 | 0.996862 |     0.00192794  |
| Dozwil       |         4406 | 0.996898 |     0.103515    |
| Kammersrohr  |         2549 | 0.996999 |     0.0526844   |
| Lichtensteig |         3374 | 0.997039 |     0.015559    |
| Dättlikon    |          215 | 0.997101 |     0.0819724   |
| Wilen (TG)   |         4786 | 0.997113 |     0.000589726 |

## Most Improved (if historical data available)

| name             |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:-----------------|-------------:|-----------:|-----------:|--------------:|
| Tobel-Tägerschen |         4776 |   0.998011 |   0.999993 |    0.00198274 |
| Le Bémont (JU)   |         6741 |   0.998456 |   0.999995 |    0.00153835 |
| Montfaucon       |         6751 |   0.998508 |   0.999995 |    0.00148711 |
| Affeltrangen     |         4711 |   0.998611 |   0.999996 |    0.00138466 |
| Bussnang         |         4921 |   0.998625 |   0.999996 |    0.00137073 |
| Les Genevez (JU) |         6748 |   0.998665 |   0.999997 |    0.00133166 |
| Bettwiesen       |         4716 |   0.997574 |   0.998765 |    0.00119165 |
| Lommis           |         4741 |   0.99885  |   0.999996 |    0.001146   |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name       |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Braunau    |         4723 |    1684510 | https://www.openstreetmap.org/relation/1684510 | https://www.openstreetmap.org/?mlat=47.491621&mlon=9.066454#map=16/47.491621/9.066454 |           0.00415989 |            0.0322073 |            0.0280474  | https://www.openstreetmap.org/changeset/44212692  | nyuriks          | 2016-12-06T15:37:35Z  |
| Bettwiesen |         4716 |    1684504 | https://www.openstreetmap.org/relation/1684504 | https://www.openstreetmap.org/?mlat=47.488903&mlon=9.022329#map=16/47.488903/9.022329 |           0.00370366 |            0.0138256 |            0.0101219  | https://www.openstreetmap.org/changeset/57681359  | SimonPoole       | 2018-03-31T07:32:53Z  |
| Tramelan   |          446 |    1682688 | https://www.openstreetmap.org/relation/1682688 | https://www.openstreetmap.org/?mlat=47.233772&mlon=7.143813#map=16/47.233772/7.143813 |           0.00619887 |            0.014648  |            0.00844914 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |

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