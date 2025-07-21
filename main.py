import geopandas as gpd
import mercantile
import csv
from shapely.geometry import box
from shapely.strtree import STRtree

gdf = gpd.read_file("japan.geojson")
if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs("EPSG:4326")
geoms = [geom for geom in gdf.geometry.values if geom is not None and not geom.is_empty]
strtree = STRtree(geoms)
geom_by_index = {i: geom for i, geom in enumerate(geoms)}

with open("intersecting_tiles.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["z", "x", "y"])

    for zoom in range(1, 15):
        print(f"🔍 z={zoom} のタイル処理中...")

        minx, miny, maxx, maxy = gdf.total_bounds
        tile_candidates = mercantile.tiles(minx, miny, maxx, maxy, zoom)

        tile_ids = set()

        for tile in tile_candidates:
            b = mercantile.bounds(tile)
            tile_geom = box(b.west, b.south, b.east, b.north)

            match_indices = strtree.query(tile_geom)

            for idx in match_indices:
                geom = geom_by_index[idx]
                if geom.intersects(tile_geom):
                    tile_ids.add((tile.z, tile.x, tile.y))
                    break

        for tid in sorted(tile_ids):
            writer.writerow(tid)

        print(f"✅ z={zoom} 完了！交差タイル数: {len(tile_ids)} ")

print("🎉 全ズーム完了！")
