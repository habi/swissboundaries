Generated: 2026-07-26 05:34:35 UTC

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
| Mean symmetric difference | 0.053% |
| Mean Hausdorff distance   | 2.4717 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-25)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  +0.000% |
| Previous mean Hausdorff distance |   2.499 |
| Current mean Hausdorff distance  |   2.472 |
| Hausdorff change                 |  -0.027 |

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

| name                |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:--------------------|-------------:|-----------:|-----------:|--------------:|
| Kradolf-Schönenberg |         4501 |   0.998523 |   0.999995 |    0.00147172 |
| Niederhelfenschwil  |         3423 |   0.998694 |   0.999996 |    0.00130128 |
| Bischofszell        |         4471 |   0.998859 |   0.999995 |    0.00113554 |
| Baar                |         1701 |   0.998935 |   0.999997 |    0.00106179 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name              |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Steinhausen       |         1708 |    1683148 | https://www.openstreetmap.org/relation/1683148 | https://www.openstreetmap.org/?mlat=47.211918&mlon=8.495102#map=16/47.211918/8.495102 |           0.00955806 |           0.0614415  |            0.0518834  | https://www.openstreetmap.org/changeset/44224875  | nyuriks          | 2016-12-07T03:13:43Z  |
| Zuzwil (SG)       |         3426 |    1683969 | https://www.openstreetmap.org/relation/1683969 | https://www.openstreetmap.org/?mlat=47.471811&mlon=9.075143#map=16/47.471811/9.075143 |           0.0175259  |           0.0418291  |            0.0243031  | https://www.openstreetmap.org/changeset/186336506 | SimonPoole       | 2026-07-25T09:37:03Z  |
| Schönholzerswilen |         4756 |    1684556 | https://www.openstreetmap.org/relation/1684556 | https://www.openstreetmap.org/?mlat=47.526933&mlon=9.109947#map=16/47.526933/9.109947 |           0.00496865 |           0.0207874  |            0.0158187  | https://www.openstreetmap.org/changeset/44224875  | nyuriks          | 2016-12-07T03:14:24Z  |
| Wuppenau          |         4791 |    1684572 | https://www.openstreetmap.org/relation/1684572 | https://www.openstreetmap.org/?mlat=47.503937&mlon=9.130737#map=16/47.503937/9.130737 |           0.00326222 |           0.0155651  |            0.0123029  | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:20Z  |
| Neuheim           |         1705 |    1683145 | https://www.openstreetmap.org/relation/1683145 | https://www.openstreetmap.org/?mlat=47.191835&mlon=8.580209#map=16/47.191835/8.580209 |           0.0140014  |           0.0254954  |            0.011494   | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Menzingen         |         1704 |    1683144 | https://www.openstreetmap.org/relation/1683144 | https://www.openstreetmap.org/?mlat=47.153579&mlon=8.604462#map=16/47.153579/8.604462 |           0.0141616  |           0.021071   |            0.00690938 | https://www.openstreetmap.org/changeset/151242030 | signina          | 2024-05-12T20:53:17Z  |
| Walchwil          |         1710 |    1683150 | https://www.openstreetmap.org/relation/1683150 | https://www.openstreetmap.org/?mlat=47.091629&mlon=8.527549#map=16/47.091629/8.527549 |           0.0148777  |           0.0216845  |            0.00680687 | https://www.openstreetmap.org/changeset/177721697 | habi             | 2026-01-26T14:06:13Z  |
| Bürglen (TG)      |         4911 |    1684512 | https://www.openstreetmap.org/relation/1684512 | https://www.openstreetmap.org/?mlat=47.562084&mlon=9.171055#map=16/47.562084/9.171055 |           0.0222126  |           0.0278526  |            0.00564003 | https://www.openstreetmap.org/changeset/44212692  | nyuriks          | 2016-12-06T15:37:36Z  |
| Cham              |         1702 |    1683139 | https://www.openstreetmap.org/relation/1683139 | https://www.openstreetmap.org/?mlat=47.213610&mlon=8.461723#map=16/47.213610/8.461723 |           0.00538489 |           0.0104111  |            0.00502623 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:20Z  |
| Arth              |         1362 |    1683058 | https://www.openstreetmap.org/relation/1683058 | https://www.openstreetmap.org/?mlat=47.054958&mlon=8.477358#map=16/47.054958/8.477358 |           0.00085995 |           0.00273736 |            0.00187741 | https://www.openstreetmap.org/changeset/183510502 | KeyTV            | 2026-06-01T17:18:46Z  |

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