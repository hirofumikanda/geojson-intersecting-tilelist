# geojson-intersecting-tilelist

このスクリプトは、指定した GeoJSON（ポリゴン地物）と交差する XYZ タイル（z, x, y）の一覧を出力します。  
Shapely の空間インデックス `STRtree` を使って高速に交差判定を行います。

## 主な機能

- GeoJSON形式のポリゴンデータを入力として読み込み
- 指定ズームレベル範囲のXYZタイルと交差するものを抽出
- 出力はCSV形式（z,x,y）
- 空間インデックスによる高速処理
- CRS（座標系）は自動で EPSG:4326（WGS84）に変換

## 必要な環境

- Python 3.8 以上
- 以下のPythonライブラリ：

```bash
pip install geopandas shapely mercantile
````

※ `shapely` は **バージョン2.0以上** が必要です（STRtree対応のため）

## 使い方

```bash
python main.py
```

実行すると以下の処理が行われます：

1. `japan_land.geojson` を読み込み
2. 全ポリゴンを Shapely ジオメトリとして取得
3. 空間インデックスを作成
4. ズームレベル1〜14の範囲で全タイルをチェック
5. 交差しているタイルID（z, x, y）を `intersecting_tiles.csv` に書き出し

## 出力例

```csv
z,x,y
10,915,402
10,916,402
...
```

## 備考

* GeoJSONがWGS84以外の座標系でも、自動でEPSG:4326に変換されます。
* 日本全域など、ある程度広いポリゴンを対象とした利用を想定しています。
* ズームレベル1〜4は精度が粗く正しく交差を検出できない場合があります。
