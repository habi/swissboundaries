Generated: 2026-07-21 05:22:42 UTC

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
| Median IoU                | 0.9998 |
| Mean area difference      | 0.010% |
| Mean symmetric difference | 0.054% |
| Mean Hausdorff distance   | 2.5995 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-20)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.606 |
| Current mean Hausdorff distance  |   2.599 |
| Hausdorff change                 |  -0.007 |

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

| name                      |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:--------------------------|-------------:|-----------:|-----------:|--------------:|
| Niederried bei Interlaken |          588 |   0.998555 |   0.999995 |    0.00144009 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name         |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Berolle      |         5424 |    1684850 | https://www.openstreetmap.org/relation/1684850 | https://www.openstreetmap.org/?mlat=46.586009&mlon=6.311299#map=16/46.586009/6.311299 |          0.0370339   |           0.040939   |            0.00390504 | https://www.openstreetmap.org/changeset/175582214 | kartler175       | 2025-12-06T11:49:18Z  |
| Mollens (VD) |         5431 |    1685051 | https://www.openstreetmap.org/relation/1685051 | https://www.openstreetmap.org/?mlat=46.589932&mlon=6.324544#map=16/46.589932/6.324544 |          0.0252693   |           0.028953   |            0.0036837  | https://www.openstreetmap.org/changeset/180865006 | SimonPoole       | 2026-04-04T17:10:49Z  |
| Silvaplana   |         3790 |    1684170 | https://www.openstreetmap.org/relation/1684170 | https://www.openstreetmap.org/?mlat=46.446530&mlon=9.845913#map=16/46.446530/9.845913 |          3.65472e-05 |           0.00106559 |            0.00102904 | https://www.openstreetmap.org/changeset/185364662 | SimonPoole       | 2026-07-08T19:38:27Z  |

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name       |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Silvaplana |         3790 |    1684170 | https://www.openstreetmap.org/relation/1684170 | https://www.openstreetmap.org/?mlat=46.446530&mlon=9.845913#map=16/46.446530/9.845913 |              0.016 |              7.122 |        7.106 | https://www.openstreetmap.org/changeset/185364662 | SimonPoole       | 2026-07-08T19:38:27Z  |
| Samedan    |         3786 |    1684150 | https://www.openstreetmap.org/relation/1684150 | https://www.openstreetmap.org/?mlat=46.446530&mlon=9.845913#map=16/46.446530/9.845913 |              0.016 |              7.122 |        7.106 | https://www.openstreetmap.org/changeset/185020361 | SimonPoole       | 2026-07-03T06:15:50Z  |

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