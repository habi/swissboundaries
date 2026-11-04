Generated: 2026-11-04 08:43:16 UTC

## Dataset Overview

| Metric                         | Value |
|--------------------------------|------:|
| Total Swisstopo municipalities |  2123 |
| Matched in OSM                 |  2123 |
| Missing in OSM                 |     0 |
| Only in OSM (not in Swisstopo) |     9 |

## Accuracy Metrics (for matched municipalities)

| Metric                    | Value  |
|---------------------------|--------|
| Mean IoU                  | 1.0000 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.001% |
| Mean symmetric difference | 0.001% |
| Mean Hausdorff distance   | 0.1540 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-11-03)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  -0.000 |
| Previous mean area difference    |   0.001% |
| Current mean area difference     |   0.001% |
| Area difference change           |  +0.000% |
| Previous mean Hausdorff distance |   0.152 |
| Current mean Hausdorff distance  |   0.154 |
| Hausdorff change                 |  +0.002 |

## Worst 10 Matches (by IoU)

| name            |   bfs_nummer |      iou |   area_diff_pct |
|:----------------|-------------:|---------:|----------------:|
| Eschenz         |         4806 | 0.982138 |     1.54071     |
| Gottlieben      |         4651 | 0.999961 |     0.000269056 |
| Mauraz          |         5488 | 0.999977 |     0.000113529 |
| Concise         |         5554 | 0.999979 |     0.00180662  |
| Cheyres-Châbles |         2055 | 0.99998  |     0.00175751  |
| Grancia         |         5186 | 0.99998  |     0.000372478 |
| Neggio          |         5206 | 0.999981 |     0.000231974 |
| Vich            |         5732 | 0.999984 |     5.29437e-05 |
| Sorengo         |         5225 | 0.999984 |     0.00020662  |
| Savosa          |         5221 | 0.999984 |     7.79363e-05 |

## Most Improved (if historical data available)

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name    |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                       |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:--------|-------------:|-----------:|:-----------------------------------------------|:----------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Zuoz    |         3791 |    1684213 | https://www.openstreetmap.org/relation/1684213 | https://www.openstreetmap.org/?mlat=46.548125&mlon=10.043108#map=16/46.548125/10.043108 |              0.016 |              1.916 |          1.9 | https://www.openstreetmap.org/changeset/185546025 | SimonPoole       | 2026-07-11T16:13:34Z  |
| S-chanf |         3788 |    1684145 | https://www.openstreetmap.org/relation/1684145 | https://www.openstreetmap.org/?mlat=46.548125&mlon=10.043108#map=16/46.548125/10.043108 |              0.016 |              1.916 |          1.9 | https://www.openstreetmap.org/changeset/185759183 | SimonPoole       | 2026-07-15T04:22:21Z  |

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