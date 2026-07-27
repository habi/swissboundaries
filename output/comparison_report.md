Generated: 2026-07-27 05:52:12 UTC

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
| Mean symmetric difference | 0.052% |
| Mean Hausdorff distance   | 2.4293 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-26)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   0.999 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.472 |
| Current mean Hausdorff distance  |   2.429 |
| Hausdorff change                 |  -0.042 |

## Worst 10 Matches (by IoU)

| name           |   bfs_nummer |      iou |   area_diff_pct |
|:---------------|-------------:|---------:|----------------:|
| Eschenz        |         4806 | 0.981348 |      1.54249    |
| Hagneck        |          736 | 0.995824 |      0.00469874 |
| Regensberg     |           95 | 0.996442 |      0.0295773  |
| Kilchberg (BL) |         2851 | 0.9965   |      0.0323861  |
| Känerkinden    |         2850 | 0.996793 |      0.0345198  |
| Fürstenau      |         3633 | 0.996862 |      0.00192794 |
| Dozwil         |         4406 | 0.996898 |      0.103515   |
| Tecknau        |         2862 | 0.996983 |      0.036558   |
| Kammersrohr    |         2549 | 0.996999 |      0.0526844  |
| Lichtensteig   |         3374 | 0.997039 |      0.015559   |

## Most Improved (if historical data available)

| name                 |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:---------------------|-------------:|-----------:|-----------:|--------------:|
| Rueyres              |         5534 |   0.995282 |   0.99999  |    0.00470784 |
| Bercher              |         5512 |   0.9975   |   0.999994 |    0.00249356 |
| Bretigny-sur-Morrens |         5515 |   0.997889 |   0.999992 |    0.00210281 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name                  |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:----------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Saint-Barthélemy (VD) |         5535 |    1685133 | https://www.openstreetmap.org/relation/1685133 | https://www.openstreetmap.org/?mlat=46.628539&mlon=6.583696#map=16/46.628539/6.583696 |           0.0189108  |           0.0442063  |            0.0252955  | https://www.openstreetmap.org/changeset/186398566 | SimonPoole       | 2026-07-26T13:09:23Z  |
| Cugy (VD)             |         5516 |    1684937 | https://www.openstreetmap.org/relation/1684937 | https://www.openstreetmap.org/?mlat=46.576626&mlon=6.652565#map=16/46.576626/6.652565 |           0.0232891  |           0.0462907  |            0.0230016  | https://www.openstreetmap.org/changeset/183415618 | SimonPoole       | 2026-05-30T19:38:04Z  |
| Oppens                |         5923 |    1685079 | https://www.openstreetmap.org/relation/1685079 | https://www.openstreetmap.org/?mlat=46.707651&mlon=6.687422#map=16/46.707651/6.687422 |           0.0040119  |           0.0254354  |            0.0214235  | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Furna                 |         3862 |    1684083 | https://www.openstreetmap.org/relation/1684083 | https://www.openstreetmap.org/?mlat=46.919690&mlon=9.684315#map=16/46.919690/9.684315 |           0.00814404 |           0.0220435  |            0.0138995  | https://www.openstreetmap.org/changeset/44195583  | nyuriks          | 2016-12-05T23:52:31Z  |
| Bettens               |         5471 |    1684851 | https://www.openstreetmap.org/relation/1684851 | https://www.openstreetmap.org/?mlat=46.628539&mlon=6.583696#map=16/46.628539/6.583696 |           0.0201316  |           0.0314954  |            0.0113637  | https://www.openstreetmap.org/changeset/155734695 | kartler175       | 2024-08-25T12:24:27Z  |
| Bottens               |         5514 |    1684861 | https://www.openstreetmap.org/relation/1684861 | https://www.openstreetmap.org/?mlat=46.624342&mlon=6.675447#map=16/46.624342/6.675447 |           0.0138789  |           0.0242944  |            0.0104154  | https://www.openstreetmap.org/changeset/186398066 | SimonPoole       | 2026-07-26T12:59:28Z  |
| Untervaz              |         3946 |    1684198 | https://www.openstreetmap.org/relation/1684198 | https://www.openstreetmap.org/?mlat=46.915685&mlon=9.478754#map=16/46.915685/9.478754 |           0.00210777 |           0.0115753  |            0.0094675  | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Ogens                 |         5680 |    1685075 | https://www.openstreetmap.org/relation/1685075 | https://www.openstreetmap.org/?mlat=46.716585&mlon=6.713517#map=16/46.716585/6.713517 |           0.0144972  |           0.0226701  |            0.00817284 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Felsberg              |         3731 |    1684075 | https://www.openstreetmap.org/relation/1684075 | https://www.openstreetmap.org/?mlat=46.838174&mlon=9.448875#map=16/46.838174/9.448875 |           0.0089191  |           0.0170091  |            0.00809003 | https://www.openstreetmap.org/changeset/186389892 | SimonPoole       | 2026-07-26T10:05:39Z  |
| Zizers                |         3947 |    1684212 | https://www.openstreetmap.org/relation/1684212 | https://www.openstreetmap.org/?mlat=46.938553&mlon=9.547832#map=16/46.938553/9.547832 |           0.00480356 |           0.00867264 |            0.00386909 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |

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