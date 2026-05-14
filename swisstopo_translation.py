import ogr2osm


class SwisstopoTranslation(ogr2osm.TranslationBase):
    """Translation file for ogr2osm to convert swissBOUNDARIES3D to OSM format.

    Handles the tlm_hoheitsgebiet layer from the swissBOUNDARIES3D GeoPackage
    file (or equivalent SHP layer).  Maps swisstopo attributes to the
    appropriate OSM tags used for Swiss administrative boundaries.

    Usage example (command line):
        ogr2osm \\
            --sql "SELECT * FROM tlm_hoheitsgebiet
                   WHERE objektart='Gemeindegebiet' AND icc='CH'" \\
            -t swisstopo_translation.py \\
            -f \\
            -o output/swissBOUNDARIES3D.osm \\
            swissBOUNDARIES3D_1_5_LV95_LN02.gpkg
    """

    def filter_tags(self, attrs):
        if not attrs:
            return None

        tags = {}

        # Municipality name — GPKG uses lowercase, SHP uses uppercase
        name = attrs.get("name") or attrs.get("NAME")
        if name:
            tags["name"] = str(name)

        # BFS municipality number — matched in OSM as swisstopo:BFS_NUMMER
        bfs_num = attrs.get("bfs_nummer") or attrs.get("BFS_NUMMER")
        if bfs_num is not None:
            try:
                # OGR may return integer fields as floats (e.g. 355.0), so
                # convert via float first to handle both int and float inputs.
                tags["swisstopo:BFS_NUMMER"] = str(int(float(bfs_num)))
            except (ValueError, TypeError):
                pass

        # Administrative boundary tags
        tags["boundary"] = "administrative"
        tags["admin_level"] = "8"  # Municipalities in Switzerland are admin_level 8

        return tags
