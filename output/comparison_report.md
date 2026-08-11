Generated: 2026-08-11 03:45:18 UTC

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
| Mean symmetric difference | 0.039% |
| Mean Hausdorff distance   | 1.8806 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-08-10)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.009% |
| Current mean area difference     |   0.009% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   1.897 |
| Current mean Hausdorff distance  |   1.881 |
| Hausdorff change                 |  -0.016 |

## Worst 10 Matches (by IoU)

| name            |   bfs_nummer |      iou |   area_diff_pct |
|:----------------|-------------:|---------:|----------------:|
| Eschenz         |         4806 | 0.981348 |       1.54249   |
| Regensberg      |           95 | 0.996494 |       0.0141785 |
| Dozwil          |         4406 | 0.996898 |       0.103515  |
| Dättlikon       |          215 | 0.997101 |       0.0819724 |
| Borex           |         5706 | 0.997201 |       0.0270045 |
| Prévonloup      |         5683 | 0.997366 |       0.0700191 |
| Lovatens        |         5674 | 0.997373 |       0.0372413 |
| Masein          |         3663 | 0.997455 |       0.0107846 |
| Obergerlafingen |         2528 | 0.997484 |       0.0485894 |
| Jaberg          |          868 | 0.997524 |       0.0534641 |

## Most Improved (if historical data available)

| name          |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:--------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Noble-Contrée |         6254 |   0.998837 |   0.999995 |    0.00115817 |    1685395 |
| Yvorne        |         5415 |   0.998839 |   0.999996 |    0.00115721 |    1685208 |
| Aigle         |         5401 |   0.998905 |   0.999996 |    0.00109096 |    1684831 |
| Gerzensee     |          866 |   0.998972 |   0.999996 |    0.00102487 |    1682451 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name       |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                    | changeset_user   | changeset_timestamp   |
|:-----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:-------------------------------------------------|:-----------------|:----------------------|
| Regensberg |           95 |    1682191 | https://www.openstreetmap.org/relation/1682191 | https://www.openstreetmap.org/?mlat=47.481393&mlon=8.409009#map=16/47.481393/8.409009 |              3.487 |             21.004 |       17.517 | https://www.openstreetmap.org/changeset/44224658 | nyuriks          | 2016-12-07T02:43:55Z  |
| Steinmaur  |          101 |    1682212 | https://www.openstreetmap.org/relation/1682212 | https://www.openstreetmap.org/?mlat=47.511950&mlon=8.452797#map=16/47.511950/8.452797 |              6.118 |             21.004 |       14.886 | https://www.openstreetmap.org/changeset/44224875 | nyuriks          | 2016-12-07T03:13:19Z  |

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