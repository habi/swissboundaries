# swissboundaries
Matching boundaries from swissBOUNDARIES3D to OpenStreetMap

This repository used the ideas presented in https://github.com/stalker314314/osm-admin-boundary-conflation and Claude.ai to produce a report on the matching.

The intital prompt to Claude.ai was

> I have the boundaries of the swiss municipalities in https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2025-04/swissboundaries3d_2025-04_2056_5728.gpkg.zip.
> Help me produce a report on how well these match geographically with the boundaries mapped in OpenStreetMap, preferrably via Overpass Turbo.
> The boundaries in the geopackage have `bfs_nummer=355`, the boundaries in OSM have `swisstopo:BFS_NUMMER=355` as a matching ID.

> Can you query Overpass in Python, too?

> Can you make this all work in a GitHub action?
