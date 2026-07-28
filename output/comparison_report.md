Generated: 2026-07-28 05:16:34 UTC

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
| Mean symmetric difference | 0.051% |
| Mean Hausdorff distance   | 2.4009 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-27)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.429 |
| Current mean Hausdorff distance  |   2.401 |
| Hausdorff change                 |  -0.028 |

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

| name           |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:---------------|-------------:|-----------:|-----------:|--------------:|
| Kilchberg (BL) |         2851 |   0.9965   |   0.99999  |    0.00349044 |
| Tecknau        |         2862 |   0.996983 |   0.999991 |    0.00300731 |
| Bätterkinden   |          533 |   0.998525 |   0.999995 |    0.00147065 |
| Röschenz       |         2791 |   0.998747 |   0.999996 |    0.00124932 |
| Zeglingen      |         2868 |   0.998947 |   0.999996 |    0.00104818 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name                  |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:----------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Wenslingen            |         2865 |    1683720 | https://www.openstreetmap.org/relation/1683720 | https://www.openstreetmap.org/?mlat=47.434032&mlon=7.923827#map=16/47.434032/7.923827 |           0.0023004  |            0.0384233 |            0.0361229  | https://www.openstreetmap.org/changeset/44222992  | nyuriks          | 2016-12-07T00:02:40Z  |
| Aefligen              |          401 |    1682358 | https://www.openstreetmap.org/relation/1682358 | https://www.openstreetmap.org/?mlat=47.086677&mlon=7.553568#map=16/47.086677/7.553568 |           0.0164946  |            0.0395424 |            0.0230478  | https://www.openstreetmap.org/changeset/44193656  | nyuriks          | 2016-12-05T21:59:16Z  |
| Le Grand-Saconnex     |         6623 |    1685504 | https://www.openstreetmap.org/relation/1685504 | https://www.openstreetmap.org/?mlat=46.222566&mlon=6.116197#map=16/46.222566/6.116197 |           0.00340724 |            0.0258145 |            0.0224073  | https://www.openstreetmap.org/changeset/182073338 | 9_tab            | 2026-05-01T12:58:45Z  |
| Rünenberg             |         2860 |    1683702 | https://www.openstreetmap.org/relation/1683702 | https://www.openstreetmap.org/?mlat=47.428208&mlon=7.866115#map=16/47.428208/7.866115 |           0.0153534  |            0.0321792 |            0.0168257  | https://www.openstreetmap.org/changeset/44224875  | nyuriks          | 2016-12-07T03:13:53Z  |
| Wiler bei Utzenstorf  |          554 |    1682724 | https://www.openstreetmap.org/relation/1682724 | https://www.openstreetmap.org/?mlat=47.163302&mlon=7.557789#map=16/47.163302/7.557789 |           0.0112713  |            0.0233568 |            0.0120854  | https://www.openstreetmap.org/changeset/186459147 | SimonPoole       | 2026-07-27T13:56:32Z  |
| Wisen (SO)            |         2502 |    1683589 | https://www.openstreetmap.org/relation/1683589 | https://www.openstreetmap.org/?mlat=47.390362&mlon=7.876400#map=16/47.390362/7.876400 |           0.0224076  |            0.0311834 |            0.00877585 | https://www.openstreetmap.org/changeset/44222992  | nyuriks          | 2016-12-07T00:02:38Z  |
| Lüterkofen-Ichertswil |         2455 |    1683546 | https://www.openstreetmap.org/relation/1683546 | https://www.openstreetmap.org/?mlat=47.154381&mlon=7.486179#map=16/47.154381/7.486179 |           0.00432636 |            0.0119761 |            0.00764976 | https://www.openstreetmap.org/changeset/143401303 | b-jazz-bot       | 2023-10-31T06:07:19Z  |
| Lohn-Ammannsegg       |         2526 |    1683541 | https://www.openstreetmap.org/relation/1683541 | https://www.openstreetmap.org/?mlat=47.183295&mlon=7.530571#map=16/47.183295/7.530571 |           0.0364167  |            0.0434899 |            0.00707319 | https://www.openstreetmap.org/changeset/44195583  | nyuriks          | 2016-12-05T23:52:13Z  |
| Ersigen               |          405 |    5817429 | https://www.openstreetmap.org/relation/5817429 | https://www.openstreetmap.org/?mlat=47.086230&mlon=7.611367#map=16/47.086230/7.611367 |           0.017451   |            0.0239537 |            0.00650269 | https://www.openstreetmap.org/changeset/186459147 | SimonPoole       | 2026-07-27T13:56:32Z  |
| Zielebach             |          556 |    1682736 | https://www.openstreetmap.org/relation/1682736 | https://www.openstreetmap.org/?mlat=47.162461&mlon=7.569506#map=16/47.162461/7.569506 |           0.0261017  |            0.0313984 |            0.0052967  | https://www.openstreetmap.org/changeset/44222992  | nyuriks          | 2016-12-07T00:02:22Z  |

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