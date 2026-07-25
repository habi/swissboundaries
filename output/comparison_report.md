Generated: 2026-07-25 05:16:29 UTC

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
| Mean Hausdorff distance   | 2.4991 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-24)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.518 |
| Current mean Hausdorff distance  |   2.499 |
| Hausdorff change                 |  -0.019 |

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

| name       |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:-----------|-------------:|-----------:|-----------:|--------------:|
| Langendorf |         2550 |   0.997438 |   0.999992 |    0.00255409 |
| Bellach    |         2542 |   0.998467 |   0.999995 |    0.00152822 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name                   |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-----------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Schattdorf             |         1213 |    1683102 | https://www.openstreetmap.org/relation/1683102 | https://www.openstreetmap.org/?mlat=46.859269&mlon=8.682190#map=16/46.859269/8.682190 |           0.0055442  |           0.0139064  |            0.00836223 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:20Z  |
| Lüsslingen-Nennigkofen |         2464 |    2742593 | https://www.openstreetmap.org/relation/2742593 | https://www.openstreetmap.org/?mlat=47.173104&mlon=7.500568#map=16/47.173104/7.500568 |           0.0152467  |           0.0214428  |            0.00619607 | https://www.openstreetmap.org/changeset/46233679  | iWowik           | 2017-02-20T06:20:50Z  |
| Biberist               |         2513 |    1683482 | https://www.openstreetmap.org/relation/1683482 | https://www.openstreetmap.org/?mlat=47.183295&mlon=7.530571#map=16/47.183295/7.530571 |           0.0105262  |           0.0124823  |            0.00195604 | https://www.openstreetmap.org/changeset/159962086 | mottiger         | 2024-12-05T15:30:42Z  |
| Glarus Süd             |         1631 |    1683141 | https://www.openstreetmap.org/relation/1683141 | https://www.openstreetmap.org/?mlat=47.035754&mlon=9.208148#map=16/47.035754/9.208148 |           0.00164645 |           0.00333195 |            0.0016855  | https://www.openstreetmap.org/changeset/185247444 | SimonPoole       | 2026-07-07T07:02:50Z  |

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