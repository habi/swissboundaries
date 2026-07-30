Generated: 2026-07-30 05:00:23 UTC

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
| Mean Hausdorff distance   | 2.3297 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-07-29)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   0.999 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.010% |
| Current mean area difference     |   0.010% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   2.361 |
| Current mean Hausdorff distance  |   2.330 |
| Hausdorff change                 |  -0.031 |

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

| name         |   bfs_nummer |   prev_iou |   curr_iou |   improvement |
|:-------------|-------------:|-----------:|-----------:|--------------:|
| Frenkendorf  |         2824 |   0.998595 |   0.999993 |    0.00139825 |
| Collex-Bossy |         6615 |   0.998848 |   0.999994 |    0.00114619 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Area Difference (if historical data available)

| name                 |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_area_diff_pct |   curr_area_diff_pct |   increase_pct_points | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:---------------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|---------------------:|---------------------:|----------------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Nuglar-St. Pantaleon |         2478 |    1683558 | https://www.openstreetmap.org/relation/1683558 | https://www.openstreetmap.org/?mlat=47.454816&mlon=7.694611#map=16/47.454816/7.694611 |           0.00285328 |           0.0312564  |            0.0284032  | https://www.openstreetmap.org/changeset/44224658  | nyuriks          | 2016-12-07T02:44:11Z  |
| Füllinsdorf          |         2825 |    1683648 | https://www.openstreetmap.org/relation/1683648 | https://www.openstreetmap.org/?mlat=47.517982&mlon=7.743488#map=16/47.517982/7.743488 |           0.0148843  |           0.0419753  |            0.027091   | https://www.openstreetmap.org/changeset/44222265  | nyuriks          | 2016-12-06T22:59:51Z  |
| Bellevue             |         6606 |    1685450 | https://www.openstreetmap.org/relation/1685450 | https://www.openstreetmap.org/?mlat=46.246326&mlon=6.151057#map=16/46.246326/6.151057 |           0.00432069 |           0.0193802  |            0.0150595  | https://www.openstreetmap.org/changeset/182293639 | 9_tab            | 2026-05-06T12:45:15Z  |
| Hersberg             |         2827 |    1683657 | https://www.openstreetmap.org/relation/1683657 | https://www.openstreetmap.org/?mlat=47.501977&mlon=7.790956#map=16/47.501977/7.790956 |           0.0446979  |           0.0583234  |            0.0136255  | https://www.openstreetmap.org/changeset/44222265  | nyuriks          | 2016-12-06T22:59:53Z  |
| Sattel               |         1371 |    1683101 | https://www.openstreetmap.org/relation/1683101 | https://www.openstreetmap.org/?mlat=47.083846&mlon=8.662088#map=16/47.083846/8.662088 |           0.0153761  |           0.0187395  |            0.00336338 | https://www.openstreetmap.org/changeset/183510502 | KeyTV            | 2026-06-01T17:18:46Z  |
| Lausen               |         2828 |    1683666 | https://www.openstreetmap.org/relation/1683666 | https://www.openstreetmap.org/?mlat=47.455806&mlon=7.772416#map=16/47.455806/7.772416 |           0.00060287 |           0.00250643 |            0.00190356 | https://www.openstreetmap.org/changeset/44222265  | nyuriks          | 2016-12-06T22:59:55Z  |
| Seltisberg           |         2833 |    1683706 | https://www.openstreetmap.org/relation/1683706 | https://www.openstreetmap.org/?mlat=47.467688&mlon=7.705963#map=16/47.467688/7.705963 |           0.0227533  |           0.0242981  |            0.00154483 | https://www.openstreetmap.org/changeset/44224875  | nyuriks          | 2016-12-07T03:13:55Z  |

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