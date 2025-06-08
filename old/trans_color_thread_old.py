from PIL import Image
import os
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
from colorsys import rgb_to_hsv

# 設定
save = False            # 変換画像を保存するか
save_sample = True      # サンプルサムネイルを保存するか
compact = True          # サムネイルを詰めて配置するか
num_images = 11         # 画像枚数
cols = 6                # プレビュー1行あたりの画像数
thumb_size = (150, 150) # サムネイル最大サイズ

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
    "#FFD700": "ゴールド",
    "#00FFFF": "シアン",
    "#8B4513": "ダークブラウン",
    "#A0522D": "セピア",
    "#B22222": "ファイアレッド",
    "#4682B4": "スチールブルー",
    "#046E04": "フォレストグリーン",
    "#F5DEB3": "ウィート",
    "#E6E6FA": "ラベンダー",
    "#DC143C": "クリムゾン",
    "#00CED1": "ダークターコイズ",
    "#FFDAB9": "ピーチパフ",
    "#ADFF2F": "グリーンイエロー",
    "#FF69B4": "ホットピンク",
    "#8A2BE2": "ブルーバイオレット",
    "#A9A9A9": "ダークグレー",
    "#F08080": "ライトコーラル",
    "#20B2AA": "ライトシーグリーン",
    "#B0E0E6": "パウダーブルー",
    "#000000": "黒",
    "#F4A460": "サンドブラウン",
    "#7FFF00": "チャートリューズ",
    "#FF6347": "トマト",
    "#40E0D0": "ターコイズ",
    "#6A5ACD": "スレートブルー",
    "#D2691E": "チョコレート",
    "#00FF7F": "スプリンググリーン",
    "#FF4500": "オレンジレッド",
    "#2E8B57": "シーグリーン",
    "#1E90FF": "ドジャーブルー",
    "#FFE4E1": "ミスティローズ",
    "#C0C0C0": "シルバー",
    "#BDB76B": "ダークカーキ",
    "#8FBC8F": "ダークシーグリーン",
    "#9932CC": "ダークオーキッド",
    "#FFB6C1": "ライトピンク",
    "#5F9EA0": "キャドブルー",
    "#F5F5DC": "ベージュ",
    "#D8BFD8": "シスル",
    "#DEB887": "バーレイウッド",
    "#00FA9A": "ミディアムスプリンググリーン",
    "#FF7F50": "コーラル",
    "#B8860B": "ダークゴールド",
    "#00FF00": "ライム",
    "#191970": "ミッドナイトブルー",
    "#FF1493": "ディープピンク",
    "#7B68EE": "ミディアムスレートブルー",
    "#228B22": "フォレスト",
    "#FFD700": "ゴールド",
    "#DA70D6": "オーキッド",
    "#00BFFF": "ディープスカイブルー",
    "#CD5C5C": "インディアンレッド",
    "#FFDEAD": "ネバダ",
    "#8B0000": "ダークレッド",
    "#00FFEF": "エレクトリックシアン",
    "#FF8C00": "ダークオレンジ",
    "#B0C4DE": "ライトスチールブルー",
    "#32CD32": "ライムグリーン",
    "#F0E68C": "カーキ",
    "#BC8F8F": "ロージーブラウン",
    "#4169E1": "ロイヤルブルー",
    "#FFFAFA": "スノー",
    "#8A3324": "バーントアンバー",
    "#00C957": "シャムロックグリーン",
    "#C71585": "ミディアムバイオレットレッド",
    "#FFEFD5": "パパイヤホイップ",
    "#A0522D": "セピア",
    "#DDA0DD": "プラム",
    "#F0FFF0": "ハニーデュー",
    "#E9967A": "ダークサーモン",
    "#7CFC00": "ローングリーン",
    "#F5FFFA": "ミントクリーム",
    "#483D8B": "ダークスレートブルー",
    "#00BFFF": "ディープスカイブルー",
    "#DC143C": "クリムゾン",
    "#FDF5E6": "オールドレース",
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def replace_color_fast(input_path, output_folder, from_color, to_color, threshold=30, save=True):
    if isinstance(from_color, str):
        from_rgb = np.array(hex_to_rgb(from_color))
    else:
        from_rgb = np.array(from_color)
    if isinstance(to_color, str):
        to_rgb = np.array(hex_to_rgb(to_color))
    else:
        to_rgb = np.array(to_color)
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img)
    rgb = arr[..., :3]
    mask = np.linalg.norm(rgb - from_rgb, axis=-1) < threshold
    arr[mask, :3] = to_rgb
    img2 = Image.fromarray(arr)
    if save:
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.basename(input_path)
        img2.save(os.path.join(output_folder, base_name))
    return img2

def replace_color_with_binary(input_path, binary_path, output_folder, to_color, save=True):
    to_rgb = np.array(hex_to_rgb(to_color))
    # 元画像とバイナリ画像を開く
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img)
    binary_img = Image.open(binary_path).convert('L')
    binary_arr = np.array(binary_img)
    # 白ピクセル（255）が変換対象
    mask = binary_arr == 255
    arr[mask, :3] = to_rgb
    img2 = Image.fromarray(arr)
    if save:
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.basename(input_path)
        img2.save(os.path.join(output_folder, base_name))
    return img2

def process_image(i, to_color, color_name, save, thumb_size):
    fname = os.path.join('hirameki_original', f'ひらめき{i}.png')
    binary_fname = os.path.join('hirameki_binary', f'ひらめき{i}.png')
    output_folder = os.path.join("hirameki_trans", f"hirameki_{to_color.lstrip('#')}_{color_name}")
    img = replace_color_with_binary(fname, binary_fname, output_folder, to_color, save=save)
    img_thumb = img.copy()
    img_thumb.thumbnail(thumb_size, Image.LANCZOS)
    return img_thumb

# 変換＆サンプル保存＆プレビュー（並列処理）
total_start = time.time()
for to_color, color_name in color_dict.items():
    start = time.time()
    thumbs = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda i: process_image(i, to_color, color_name, save, thumb_size), range(1, num_images + 1)))
        thumbs.extend(results)
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
        x = col * img_w + (img_w - img_thumb.size[0]) // 2
        y = row * img_h + (img_h - img_thumb.size[1]) // 2
        preview_img.paste(img_thumb, (x, y))
    if save_sample:
        os.makedirs("samples", exist_ok=True)
        preview_img.save(os.path.join("samples", f"{to_color.lstrip('#')}_{color_name}.png"))
    end = time.time()
    elapsed = end - start
    remain = len(color_dict) - list(color_dict.keys()).index(to_color) - 1
    est_total = elapsed * (remain + 1)
    print(f"{elapsed:.2f}秒 | 残り推定:{est_total:.1f}秒 | {to_color} | {color_name}")
total_end = time.time()
print(f"全色合計処理時間: {total_end - total_start:.2f}秒")

start_time = time.time()

# --- samplesディレクトリ内の画像を3列でラベル付き結合 ---
from PIL import Image, ImageDraw, ImageFont
import os

samples_dir = 'samples'
output_path = 'complate.png'

image_files = [f for f in os.listdir(samples_dir) if f.endswith('.png') and f != 'complate.png']

# 彩度・明度で並べるための関数
def hex_to_rgb_tuple(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_color_info(fname):
    # ファイル名例: '00B3FF_青.png' → '00B3FF'
    code = fname.split('_', 1)[0]
    rgb = hex_to_rgb_tuple(code)
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = rgb_to_hsv(r, g, b)
    return (s, v, h)  # 彩度, 明度, 色相

# 彩度（s）降順、明度（v）降順、色相（h）昇順でソート
image_files.sort(key=get_color_info, reverse=True)

images = [Image.open(os.path.join(samples_dir, fname)) for fname in image_files]

cols = 4
rows = (len(images) + cols - 1) // cols
widths, heights = zip(*(img.size for img in images))
img_w = max(widths)
img_h = max(heights)

try:
    font = ImageFont.truetype('meiryo.ttc', 28)
except:
    font = ImageFont.load_default()
label_h = 36
canvas_w = cols * img_w
canvas_h = rows * (img_h + label_h)

new_img = Image.new('RGBA', (canvas_w, canvas_h), (255,255,255,255))
draw = ImageDraw.Draw(new_img)

for idx, (img, fname) in enumerate(zip(images, image_files)):
    row = idx // cols
    col = idx % cols
    x = col * img_w
    y = row * (img_h + label_h)
    # 白背景で合成
    bg = Image.new('RGBA', (img_w, img_h), (255,255,255,255))
    bg.paste(img, (0, 0), img if img.mode == 'RGBA' else None)
    new_img.paste(bg, (x, y))
    label = os.path.splitext(fname)[0]
    try:
        bbox = draw.textbbox((0,0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(label)
    text_x = x + (img_w - text_w) // 2
    text_y = y + img_h + (label_h - text_h) // 2
    draw.text((text_x, text_y), label, fill=(0,0,0,255), font=font)

new_img.save(output_path)
end_time = time.time()
print(f'結合画像を保存しました: {output_path}')
print(f'結合画像生成時間: {end_time - start_time:.2f}秒')
