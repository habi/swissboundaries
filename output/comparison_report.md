Generated: 2026-09-11 19:34:09 UTC

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
| Mean area difference      | 0.005% |
| Mean symmetric difference | 0.014% |
| Mean Hausdorff distance   | 0.9100 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2123 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-11)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.005% |
| Current mean area difference     |   0.005% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.917 |
| Current mean Hausdorff distance  |   0.910 |
| Hausdorff change                 |  -0.007 |

## Worst 10 Matches (by IoU)

| name          |   bfs_nummer |      iou |   area_diff_pct |
|:--------------|-------------:|---------:|----------------:|
| Eschenz       |         4806 | 0.982101 |      1.5445     |
| Prévonloup    |         5683 | 0.997366 |      0.0700191  |
| Lovatens      |         5674 | 0.997373 |      0.0372413  |
| Chêne-Pâquier |         5908 | 0.99773  |      0.0210398  |
| Willadingen   |          423 | 0.997933 |      0.0548498  |
| Gy            |         6624 | 0.997952 |      0.0613426  |
| Giebenach     |         2826 | 0.998    |      0.00184768 |
| Hellsau       |          408 | 0.998087 |      0.0493622  |
| Rümlingen     |         2859 | 0.998115 |      0.0180965  |
| Bettingen     |         2702 | 0.998261 |      0.0699435  |

## Most Improved (if historical data available)

| name        |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Dänikon     |           85 |   0.998175 |   0.999992 |    0.00181629 |    1682109 |
| Hüttikon    |           87 |   0.99844  |   0.999988 |    0.001548   |    1682149 |
| Schleinikon |           98 |   0.998695 |   0.999994 |    0.0012996  |    1682203 |
| Boppelsen   |           82 |   0.998971 |   0.999994 |    0.00102227 |    1682093 |

## Most Deteriorated (if historical data available)

No significant deteriorations detected.

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name         |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:-------------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Saignelégier |         6757 |    1685626 | https://www.openstreetmap.org/relation/1685626 | https://www.openstreetmap.org/?mlat=47.296422&mlon=6.977669#map=16/47.296422/6.977669 |              0.015 |             17.444 |       17.429 | https://www.openstreetmap.org/changeset/188869449 | SimonPoole       | 2026-09-11T12:18:09Z  |
| Les Breuleux |         6743 |    1685610 | https://www.openstreetmap.org/relation/1685610 | https://www.openstreetmap.org/?mlat=47.219689&mlon=7.007361#map=16/47.219689/7.007361 |              3.668 |             17.444 |       13.776 | https://www.openstreetmap.org/changeset/188869449 | SimonPoole       | 2026-09-11T12:18:09Z  |

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