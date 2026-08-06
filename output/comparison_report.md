Generated: 2026-08-06 05:18:50 UTC

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
| Mean IoU                  | 0.9996 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.009% |
| Mean symmetric difference | 0.043% |
| Mean Hausdorff distance   | 2.0460 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-05)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.009% |
| Current mean area difference     |   0.009% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.073 |
| Current mean Hausdorff distance  |   2.046 |
| Hausdorff change                 |  -0.027 |

## Worst 10 Matches (by IoU)

| name        |   bfs_nummer |      iou |   area_diff_pct |
|:------------|-------------:|---------:|----------------:|
| Eschenz     |         4806 | 0.981348 |       1.54249   |
| Regensberg  |           95 | 0.996637 |       0.03134   |
| Dozwil      |         4406 | 0.996898 |       0.103515  |
| Kammersrohr |         2549 | 0.996999 |       0.0526844 |
| Dättlikon   |          215 | 0.997101 |       0.0819724 |
| Borex       |         5706 | 0.997201 |       0.0270045 |
| Henggart    |           31 | 0.997285 |       0.0153214 |
| Prévonloup  |         5683 | 0.997366 |       0.0700191 |
| Lovatens    |         5674 | 0.997373 |       0.0372413 |
| Birsfelden  |         2766 | 0.997411 |       0.0594732 |

## Most Improved (if historical data available)

| name                 |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:---------------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Känerkinden          |         2850 |   0.996793 |   0.999994 |    0.00320039 |    1683662 |
| Oberweningen         |           93 |   0.997125 |   0.999992 |    0.0028673  |    1682180 |
| Niederglatt          |           89 |   0.997333 |   0.999994 |    0.00266052 |    1682171 |
| Mattstetten          |          543 |   0.997901 |   0.999992 |    0.0020906  |    1682548 |
| Hilterfingen         |          929 |   0.998567 |   0.999992 |    0.00142527 |    1682480 |
| Bäriswil             |          403 |   0.998597 |   0.999993 |    0.00139612 |    1682400 |
| Schöfflisdorf        |           99 |   0.997437 |   0.998667 |    0.00122994 |    1682206 |
| Nuglar-St. Pantaleon |         2478 |   0.998803 |   0.999995 |    0.001192   |    1683558 |
| Schleinikon          |           98 |   0.997551 |   0.998688 |    0.0011371  |    1682203 |
| Seltisberg           |         2833 |   0.998889 |   0.999995 |    0.00110637 |    1683706 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name    |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:--------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Hagneck |          736 |    1682468 | https://www.openstreetmap.org/relation/1682468 | https://www.openstreetmap.org/?mlat=47.061378&mlon=7.191817#map=16/47.061378/7.191817 |              0.007 |              2.336 |        2.329 | https://www.openstreetmap.org/changeset/186928760 | habi             | 2026-08-04T14:34:59Z  |

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