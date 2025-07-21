import geopandas as gpd
import mercantile
import csv
from shapely.geometry import box

# GeoJSONポリゴンの読み込み
gdf = gpd.read_file("japan.geojson").to_crs("EPSG:4326")
geom_union = gdf.union_all()

# 出力先CSVファイルを用意
with open("intersecting_tiles.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["z", "x", "y"])

    for zoom in range(1, 15):
        print(f"🔍 z={zoom} のタイルを調査中…")
        minx, miny, maxx, maxy = geom_union.bounds
        tile_candidates = mercantile.tiles(minx, miny, maxx, maxy, zoom)

        tile_ids = set()

        for tile in tile_candidates:
            bounds = mercantile.bounds(tile)
            tile_geom = box(bounds.west, bounds.south, bounds.east, bounds.north)
            if geom_union.intersects(tile_geom):
                tile_ids.add((tile.z, tile.x, tile.y))

        for tile_id in sorted(tile_ids):
            writer.writerow(tile_id)

        print(f"✅ z={zoom} 完了。交差タイル数: {len(tile_ids)}")

print("🎉 全ズーム完了！")
