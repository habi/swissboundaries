Generated: 2026-07-24 05:23:14 UTC

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
| Mean Hausdorff distance   | 2.5177 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-23)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.544 |
| Current mean Hausdorff distance  |   2.518 |
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

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name          |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:--------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Buseno        |         3804 |    1684053 | https://www.openstreetmap.org/relation/1684053 | https://www.openstreetmap.org/?mlat=46.287134&mlon=9.120613#map=16/46.287134/9.120613 |          0.0293372   |           0.0350303  |            0.00569311 | https://www.openstreetmap.org/changeset/29338809  | ydrgbjo          | 2015-03-08T20:54:22Z  |
| Breil/Brigels |         3981 |    1684050 | https://www.openstreetmap.org/relation/1684050 | https://www.openstreetmap.org/?mlat=46.767866&mlon=9.018175#map=16/46.767866/9.018175 |          0.000810475 |           0.0028135  |            0.00200303 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Lungern       |         1405 |    1683090 | https://www.openstreetmap.org/relation/1683090 | https://www.openstreetmap.org/?mlat=46.763929&mlon=8.165924#map=16/46.763929/8.165924 |          0.000491452 |           0.00246729 |            0.00197584 | https://www.openstreetmap.org/changeset/119388272 | FischersFritz    | 2022-04-06T13:41:39Z  |
| Ilanz/Glion   |         3619 |    3411942 | https://www.openstreetmap.org/relation/3411942 | https://www.openstreetmap.org/?mlat=46.872244&mlon=9.084861#map=16/46.872244/9.084861 |          0.00163169  |           0.00303138 |            0.00139969 | https://www.openstreetmap.org/changeset/186218626 | SimonPoole       | 2026-07-23T07:57:43Z  |

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