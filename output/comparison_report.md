Generated: 2026-10-02 08:00:16 UTC

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
| Mean IoU                  | 0.9999 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.002% |
| Mean symmetric difference | 0.005% |
| Mean Hausdorff distance   | 0.4401 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-10-01)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.002% |
| Current mean area difference     |   0.002% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.450 |
| Current mean Hausdorff distance  |   0.440 |
| Hausdorff change                 |  -0.010 |

## Worst 10 Matches (by IoU)

| name               |   bfs_nummer |      iou |   area_diff_pct |
|:-------------------|-------------:|---------:|----------------:|
| Eschenz            |         4806 | 0.982101 |       1.5445    |
| Prévonloup         |         5683 | 0.997366 |       0.0700191 |
| Bettingen          |         2702 | 0.998261 |       0.0699435 |
| Lovatens           |         5674 | 0.998371 |       0.0597391 |
| Romanel-sur-Morges |         5645 | 0.998662 |       0.0979852 |
| Finsterhennen      |          493 | 0.9987   |       0.0147253 |
| Wiggiswil          |          553 | 0.998797 |       0.0462724 |
| Brenzikofen        |          606 | 0.998841 |       0.0626268 |
| Herbligen          |          610 | 0.998906 |       0.066823  |
| La Praz            |         5758 | 0.998925 |       0.0763002 |

## Most Improved (if historical data available)

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name       |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Gurtnellen |         1209 |    1683078 | https://www.openstreetmap.org/relation/1683078 | https://www.openstreetmap.org/?mlat=46.717617&mlon=8.608803#map=16/46.717617/8.608803 |              1.452 |              8.489 |        7.037 | https://www.openstreetmap.org/changeset/185854607 | SimonPoole       | 2026-07-16T16:11:54Z  |
| Wassen     |         1220 |    1683121 | https://www.openstreetmap.org/relation/1683121 | https://www.openstreetmap.org/?mlat=46.717617&mlon=8.608803#map=16/46.717617/8.608803 |              3.21  |              8.489 |        5.279 | https://www.openstreetmap.org/changeset/189827321 | SimonPoole       | 2026-10-01T14:14:46Z  |

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