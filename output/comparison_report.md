Generated: 2026-08-01 05:29:23 UTC

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
| Mean Hausdorff distance   | 2.2745 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-31)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.304 |
| Current mean Hausdorff distance  |   2.275 |
| Hausdorff change                 |  -0.029 |

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

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name               |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Chavannes-le-Chêne |         5907 |    1684891 | https://www.openstreetmap.org/relation/1684891 | https://www.openstreetmap.org/?mlat=46.774159&mlon=6.769095#map=16/46.774159/6.769095 |          0.0235048   |           0.031621   |            0.0081162  | https://www.openstreetmap.org/changeset/44213420  | nyuriks          | 2016-12-06T16:07:17Z  |
| St. Ursen          |         2304 |    1683404 | https://www.openstreetmap.org/relation/1683404 | https://www.openstreetmap.org/?mlat=46.779301&mlon=7.200905#map=16/46.779301/7.200905 |          0.000453813 |           0.00339955 |            0.00294574 | https://www.openstreetmap.org/changeset/180873360 | SimonPoole       | 2026-04-04T21:08:18Z  |
| La Sonnaz          |         2235 |    1683346 | https://www.openstreetmap.org/relation/1683346 | https://www.openstreetmap.org/?mlat=46.825113&mlon=7.125363#map=16/46.825113/7.125363 |          0.0020406   |           0.00443018 |            0.00238958 | https://www.openstreetmap.org/changeset/44222265  | nyuriks          | 2016-12-06T22:59:46Z  |

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