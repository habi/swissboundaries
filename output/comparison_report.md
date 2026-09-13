Generated: 2026-09-13 07:14:03 UTC

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
| Mean IoU                  | 0.9999 |
| Median IoU                | 1.0000 |
| Mean area difference      | 0.004% |
| Mean symmetric difference | 0.014% |
| Mean Hausdorff distance   | 0.8815 |

## Quality Distribution

| Quality    | Count | Percentage |
|------------|-------|-----------:|
| IoU ≥ 0.98 |  2121 |    100.000 |
| IoU ≥ 0.95 |     0 |      0.000 |
| IoU ≥ 0.90 |     0 |      0.000 |
| IoU < 0.90 |     0 |      0.000 |

## Historical Comparison (vs 2026-09-12)

| Metric                           | Value   |
|----------------------------------|---------|
| Previous mean IoU                |   1.000 |
| Current mean IoU                 |   1.000 |
| Change                           |  +0.000 |
| Previous mean area difference    |   0.004% |
| Current mean area difference     |   0.004% |
| Area difference change           |  -0.000% |
| Previous mean Hausdorff distance |   0.882 |
| Current mean Hausdorff distance  |   0.881 |
| Hausdorff change                 |  -0.001 |

## Worst 10 Matches (by IoU)

| name          |   bfs_nummer |      iou |   area_diff_pct |
|:--------------|-------------:|---------:|----------------:|
| Eschenz       |         4806 | 0.982101 |      1.5445     |
| Prévonloup    |         5683 | 0.997366 |      0.0700191  |
| Lovatens      |         5674 | 0.997373 |      0.0372413  |
| Chêne-Pâquier |         5908 | 0.99773  |      0.0210398  |
| Henniez       |         5819 | 0.997866 |      0.168654   |
| Willadingen   |          423 | 0.997933 |      0.0548498  |
| Giebenach     |         2826 | 0.998    |      0.00184768 |
| Hellsau       |          408 | 0.998087 |      0.0493622  |
| Rümlingen     |         2859 | 0.998115 |      0.0180965  |
| Bettingen     |         2702 | 0.998261 |      0.0699435  |

## Most Improved (if historical data available)

| name         |   bfs_nummer |   prev_iou |   curr_iou |   improvement |   relation |
|:-------------|-------------:|-----------:|-----------:|--------------:|-----------:|
| Gy           |         6624 |   0.997952 |   0.99999  |    0.00203785 |    1685490 |
| Unterramsern |         2463 |   0.998296 |   0.999992 |    0.00169632 |    1683584 |
| Kernenried   |          411 |   0.998675 |   0.999994 |    0.00131862 |    1682506 |

## Most Deteriorated (if historical data available)

| name    |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_iou |   curr_iou |   deterioration | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:--------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-----------:|-----------:|----------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Henniez |         5819 |    1685001 | https://www.openstreetmap.org/relation/1685001 | https://www.openstreetmap.org/?mlat=46.745541&mlon=6.877775#map=16/46.745541/6.877775 |   0.999554 |   0.997866 |      0.00168873 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |

## Most Deteriorated in Hausdorff Distance (if historical data available)

| name      |   bfs_nummer |   relation | osm_url                                        | boundary_diff_url                                                                     |   prev_hausdorff_m |   curr_hausdorff_m |   increase_m | changeset_url                                     | changeset_user   | changeset_timestamp   |
|:----------|-------------:|-----------:|:-----------------------------------------------|:--------------------------------------------------------------------------------------|-------------------:|-------------------:|-------------:|:--------------------------------------------------|:-----------------|:----------------------|
| Henniez   |         5819 |    1685001 | https://www.openstreetmap.org/relation/1685001 | https://www.openstreetmap.org/?mlat=46.745541&mlon=6.877775#map=16/46.745541/6.877775 |              3.043 |             31.412 |       28.369 | https://www.openstreetmap.org/changeset/153414606 | woodpeck_repair  | 2024-07-01T14:10:13Z  |
| Surpierre |         2044 |    1683406 | https://www.openstreetmap.org/relation/1683406 | https://www.openstreetmap.org/?mlat=46.745541&mlon=6.877775#map=16/46.745541/6.877775 |              3.073 |             31.412 |       28.339 | https://www.openstreetmap.org/changeset/179329999 | Tseodoric        | 2026-03-04T03:00:21Z  |

## BFS numbers only in Swisstopo (missing in OSM) (showing first 20):
| name            |   bfs_nummer |
|:----------------|-------------:|
| Isenthal        |         1211 |
| Wolfenschiessen |         1511 |

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

## Municipalities whose swisstopo:BFS_NUMMER tag was removed from OSM (2):
  • Isenthal (BFS 1211)  — OSM relation: https://www.openstreetmap.org/relation/1683085  — tag removed in changeset https://www.openstreetmap.org/changeset/188945634 by SimonPoole at 2026-09-13T06:42:00Z
  • Wolfenschiessen (BFS 1511)  — OSM relation: https://www.openstreetmap.org/relation/1683122  — tag removed in changeset https://www.openstreetmap.org/changeset/188945843 by SimonPoole at 2026-09-13T06:50:52Z