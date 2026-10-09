Generated: 2026-10-09 08:33:33 UTC

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
| Mean area difference      | 0.002% |
| Mean symmetric difference | 0.004% |
| Mean Hausdorff distance   | 0.3576 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-10-08)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.002% |
| Current mean area difference     |   0.002% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.375 |
| Current mean Hausdorff distance  |   0.358 |
| Hausdorff change                 |  -0.018 |

## Worst 10 Matches (by IoU)

| name               |   bfs_nummer |      iou |   area_diff_pct |
|:-------------------|-------------:|---------:|----------------:|
| Eschenz            |         4806 | 0.982101 |       1.5445    |
| Prévonloup         |         5683 | 0.997366 |       0.0700191 |
| Lovatens           |         5674 | 0.998371 |       0.0597391 |
| Romanel-sur-Morges |         5645 | 0.998662 |       0.0979852 |
| Wiggiswil          |          553 | 0.998797 |       0.0462724 |
| Brenzikofen        |          606 | 0.998841 |       0.0626268 |
| Herbligen          |          610 | 0.998906 |       0.066823  |
| Zielebach          |          556 | 0.999013 |       0.0251335 |
| Lalden             |         6286 | 0.999085 |       0.0372583 |
| Oppligen           |          622 | 0.999128 |       0.011958  |

## Most Improved (if historical data available)

No significant improvements detected.

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

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

## Resolved: swisstopo:BFS_NUMMER tag restored in OSM (1):
  • Bettingen (BFS 2702)  — first detected: 2026-10-08  — OSM relation: https://www.openstreetmap.org/relation/1683623