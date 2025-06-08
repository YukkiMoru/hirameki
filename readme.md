# ひらめき画像 色変換・分類・可視化ツール
githubでソースコードが管理されています。
https://github.com/YukkiMoru/hirameki
## 概要
このプロジェクトは、ひらめき画像（`hirameki_original`）を指定色で二値化し、カラーパレット（`color.py`）の各色に変換・分類・サムネイル化・可視化・PowerPoint資料化までを自動化するPythonスクリプト群です。

## 主な機能
- 画像の色変換・二値化・分類（`trans_color_thread.py`, `tools/binarize_images.py`）
- 色名・カラーコード管理とチェック（`color.py`, `tools/check_color.py`）
- 色分布の可視化（`tools/color_graph.py`）
- 変換画像のサムネイル生成・サンプル結合（`samples`, `complete.png`）
- PowerPoint資料自動生成（`make_hirameki_ppt.py`）

## ディレクトリ構成
```
hirameki_original/   ... 元画像
hirameki_binary/     ... 二値化画像
hirameki_files/      ... 色ごとに分類された変換画像
samples/             ... サンプルサムネイル
tools/               ... 補助スクリプト
old/                 ... 旧バージョン
color.py             ... カラーパレット定義
color_major.py       ... 主要色パレット
trans_color_thread.py... メイン処理スクリプト
make_hirameki_ppt.py ... PowerPoint生成
complete.png         ... サンプル結合画像
```

## セットアップ
1. Python 3.8以降推奨
2. 仮想環境作成（`python-env.txt`参照）
3. 必要なパッケージをインストール:
   ```
   pip install numpy pillow matplotlib python-pptx
   ```

## 使い方
1. 元画像を `hirameki_original` に配置
2. 二値化（例: 黄色部分を抽出）
   ```
   python tools/binarize_images.py
   ```
3. 色変換・分類・サムネイル生成
   ```
   python trans_color_thread.py
   ```
   - `samples` にサムネイル、`hirameki_files` に色ごとの画像が生成されます
   - `complete.png` にサンプル結合画像が生成されます
4. PowerPoint資料作成
   ```
   python make_hirameki_ppt.py
   ```
5. 色分布の可視化
   ```
   python tools/color_graph.py
   ```

## カスタマイズ
- カラーパレットは `color.py` を編集してください。
- 主要色のみで処理したい場合は `color_major.py` を利用し、`trans_color_thread.py` の該当行を切り替えてください。