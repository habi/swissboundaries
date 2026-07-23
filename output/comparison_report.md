Generated: 2026-07-23 05:26:49 UTC

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
| Mean Hausdorff distance   | 2.5445 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-22)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.581 |
| Current mean Hausdorff distance  |   2.544 |
| Hausdorff change                 |  -0.037 |

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

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name      |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Dallenwil |         1503 |    1683064 | https://www.openstreetmap.org/relation/1683064 | https://www.openstreetmap.org/?mlat=46.937484&mlon=8.378187#map=16/46.937484/8.378187 |          0.000587686 |           0.0136031  |            0.0130155  | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Kaufdorf  |          869 |    1682504 | https://www.openstreetmap.org/relation/1682504 | https://www.openstreetmap.org/?mlat=46.836641&mlon=7.486885#map=16/46.836641/7.486885 |          0.00419869  |           0.0128307  |            0.00863196 | https://www.openstreetmap.org/changeset/44195583  | nyuriks          | 2016-12-05T23:51:21Z  |
| Uebeschi  |          943 |    1682697 | https://www.openstreetmap.org/relation/1682697 | https://www.openstreetmap.org/?mlat=46.741768&mlon=7.561543#map=16/46.741768/7.561543 |          0.00166081  |           0.00540542 |            0.00374461 | https://www.openstreetmap.org/changeset/21351369  | Schnupfix        | 2014-03-27T19:33:30Z  |
| Ennetmoos |         1506 |    1683069 | https://www.openstreetmap.org/relation/1683069 | https://www.openstreetmap.org/?mlat=46.930347&mlon=8.342888#map=16/46.930347/8.342888 |          0.0156191   |           0.0173731  |            0.00175396 | https://www.openstreetmap.org/changeset/63658080  | user_177389      | 2018-10-18T19:17:08Z  |

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