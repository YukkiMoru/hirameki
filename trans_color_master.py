from PIL import Image
import os

# 設定
from_color = '#FFFF00'  # 置換元の色（例：黄色）
threshold = 100          # 色のしきい値
save = True            # 変換画像を保存するか
save_sample = True      # サンプルサムネイルを保存するか
num_images = 11         # 画像枚数
cols = 6                # プレビュー1行あたりの画像数
thumb_size = (150, 150) # サムネイル最大サイズ
over_ride = False  # 既存の画像をスキップするか

# 変換先カラーリスト（辞書型: カラーコード: 色名）
color_dict = {
    "#FFFF00": "黄",
    "#00B3FF": "青",
    "#FF0000": "赤",
    "#00A500": "緑",
    "#FF00FF": "マゼンタ",
    "#FFA500": "オレンジ",
    "#FFFFFF": "白",
    "#777777": "グレー",
    "#C529C5": "紫",
    "#EB8A9A": "ピンク",
    "#9BF415": "黄緑",
    "#D16212": "茶色",
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def replace_color(input_path, output_folder, from_color, to_color, threshold=30, save=True):
    if isinstance(from_color, str):
        from_rgb = hex_to_rgb(from_color)
    else:
        from_rgb = from_color
    if isinstance(to_color, str):
        to_rgb = hex_to_rgb(to_color)
    else:
        to_rgb = to_color
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if color_distance((r, g, b), from_rgb) < threshold:
                pixels[x, y] = (*to_rgb, a)
    if save:
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.basename(input_path)
        img.save(os.path.join(output_folder, base_name))
    return img

# 変換＆サンプル保存＆プレビュー
for to_color, color_name in color_dict.items():
    output_folder = os.path.join("hirameki_trans", f"hirameki_{to_color.lstrip('#')}_{color_name}")
    image_files = []
    thumbs = []
    for i in range(1, num_images + 1):
        fname = os.path.join('hirameki_original', f'ひらめき{i}.png')
        img = replace_color(fname, output_folder, from_color, to_color, threshold=threshold, save=save)
        # サムネイル作成
        img_thumb = img.copy()
        img_thumb.thumbnail(thumb_size, Image.LANCZOS)
        thumbs.append(img_thumb)
        image_files.append(os.path.join(output_folder, f'ひらめき{i}.png'))
    # プレビュー用画像の圧縮配置（余白なしで詰めて1枚に）
    img_w = max(t.size[0] for t in thumbs) if thumbs else thumb_size[0]
    img_h = max(t.size[1] for t in thumbs) if thumbs else thumb_size[1]
    n_thumbs = len(thumbs)
    n_cols = min(cols, n_thumbs)
    n_rows = (n_thumbs + n_cols - 1) // n_cols
    preview_img = Image.new('RGBA', (n_cols * img_w, n_rows * img_h), (255,255,255,0))
    for idx, img_thumb in enumerate(thumbs):
        row = idx // n_cols
        col = idx % n_cols
        # サムネイルを中央揃えで貼り付け
        x = col * img_w + (img_w - img_thumb.size[0]) // 2
        y = row * img_h + (img_h - img_thumb.size[1]) // 2
        preview_img.paste(img_thumb, (x, y))
    if save_sample:
        os.makedirs("samples", exist_ok=True)
        preview_img.save(os.path.join("samples", f"{to_color.lstrip('#')}_{color_name}.png"))
