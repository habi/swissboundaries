Generated: 2026-07-29 05:23:37 UTC

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
| Mean symmetric difference | 0.050% |
| Mean Hausdorff distance   | 2.3607 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-28)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.401 |
| Current mean Hausdorff distance  |   2.361 |
| Hausdorff change                 |  -0.040 |

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

| name                 |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:---------------------|-------------:|-----------:|-----------:|--------------:|
| Valeyres-sous-Rances |         5763 |   0.998076 |   0.999994 |    0.00191785 |
| Lengwil              |         4683 |   0.998288 |   0.999995 |    0.00170697 |
| Berg (TG)            |         4891 |   0.998434 |   0.999996 |    0.00156124 |
| Bottighofen          |         4643 |   0.997138 |   0.998677 |    0.00153906 |
| Märstetten           |         4941 |   0.998591 |   0.999996 |    0.00140469 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name            |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:----------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Wigoltingen     |         4951 |    1684570 | https://www.openstreetmap.org/relation/1684570 | https://www.openstreetmap.org/?mlat=47.588031&mlon=9.013464#map=16/47.588031/9.013464 |           0.0162088  |            0.042237  |            0.0260282  | https://www.openstreetmap.org/changeset/17840790  | mstock           | 2013-09-14T21:41:10Z  |
| Langrickenbach  |         4681 |    1684538 | https://www.openstreetmap.org/relation/1684538 | https://www.openstreetmap.org/?mlat=47.575678&mlon=9.272409#map=16/47.575678/9.272409 |           0.0112238  |            0.029347  |            0.0181233  | https://www.openstreetmap.org/changeset/186501822 | SimonPoole       | 2026-07-28T07:18:47Z  |
| Ependes (VD)    |         5914 |    1684960 | https://www.openstreetmap.org/relation/1684960 | https://www.openstreetmap.org/?mlat=46.739550&mlon=6.614911#map=16/46.739550/6.614911 |           0.00710667 |            0.0218676 |            0.014761   | https://www.openstreetmap.org/changeset/179138618 | SimonPoole       | 2026-02-27T16:09:40Z  |
| Rothenthurm     |         1370 |    1683098 | https://www.openstreetmap.org/relation/1683098 | https://www.openstreetmap.org/?mlat=47.090494&mlon=8.697903#map=16/47.090494/8.697903 |           0.00042981 |            0.0125198 |            0.01209    | https://www.openstreetmap.org/changeset/44195583  | nyuriks          | 2016-12-05T23:52:02Z  |
| Weinfelden      |         4946 |    1684569 | https://www.openstreetmap.org/relation/1684569 | https://www.openstreetmap.org/?mlat=47.560819&mlon=9.135503#map=16/47.560819/9.135503 |           0.00312301 |            0.0117558 |            0.00863275 | https://www.openstreetmap.org/changeset/44222992  | nyuriks          | 2016-12-07T00:03:04Z  |
| Sattel          |         1371 |    1683101 | https://www.openstreetmap.org/relation/1683101 | https://www.openstreetmap.org/?mlat=47.083846&mlon=8.662088#map=16/47.083846/8.662088 |           0.00712616 |            0.0153761 |            0.00824997 | https://www.openstreetmap.org/changeset/183510502 | KeyTV            | 2026-06-01T17:18:46Z  |
| Feusisberg      |         1321 |    1683071 | https://www.openstreetmap.org/relation/1683071 | https://www.openstreetmap.org/?mlat=47.166560&mlon=8.749521#map=16/47.166560/8.749521 |           0.00436647 |            0.0112203 |            0.00685387 | https://www.openstreetmap.org/changeset/44195583  | nyuriks          | 2016-12-05T23:51:55Z  |
| Amlikon-Bissegg |         4881 |    1684498 | https://www.openstreetmap.org/relation/1684498 | https://www.openstreetmap.org/?mlat=47.560053&mlon=9.069083#map=16/47.560053/9.069083 |           0.0346837  |            0.0402552 |            0.00557151 | https://www.openstreetmap.org/changeset/44212692  | nyuriks          | 2016-12-06T15:37:31Z  |
| Unterägeri      |         1709 |    1683149 | https://www.openstreetmap.org/relation/1683149 | https://www.openstreetmap.org/?mlat=47.116930&mlon=8.554560#map=16/47.116930/8.554560 |           0.00568844 |            0.0101232 |            0.0044348  | https://www.openstreetmap.org/changeset/186561808 | SimonPoole       | 2026-07-29T05:09:56Z  |
| Münsterlingen   |         4691 |    1684546 | https://www.openstreetmap.org/relation/1684546 | https://www.openstreetmap.org/?mlat=47.623563&mlon=9.213860#map=16/47.623563/9.213860 |           0.0562323  |            0.0592884 |            0.00305607 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |

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