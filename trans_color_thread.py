from PIL import Image
import os
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
from colorsys import rgb_to_hsv
# from color_major import color_dict
from color import color_dict

# 設定
save = True            # 変換画像を保存するか
save_sample = True      # サンプルサムネイルを保存するか
skip_sample_exists = True  # サンプルが既にあればスキップするか
compact = True          # サムネイルを詰めて配置するか
num_images = 11         # 画像枚数
cols = 6                # プレビュー1行あたりの画像数
thumb_size = (150, 150) # サムネイル最大サイズ

# 出力先ディレクトリ
os.makedirs("hirameki_files", exist_ok=True)

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
    output_folder = os.path.join("hirameki_files", f"hirameki_{to_color.lstrip('#')}_{color_name}")
    img = replace_color_with_binary(fname, binary_fname, output_folder, to_color, save=save)
    img_thumb = img.copy()
    img_thumb.thumbnail(thumb_size, Image.LANCZOS)
    return img_thumb

# 変換＆サンプル保存＆プレビュー（並列処理）
total_start = time.time()
for to_color, color_name in color_dict.items():
    start = time.time()
    thumbs = []
    sample_path = os.path.join("samples", f"{to_color.lstrip('#')}_{color_name}.png")
    if save_sample and skip_sample_exists and os.path.exists(sample_path):
        print(f"既にサンプルが存在するためスキップ: {sample_path}")
        continue
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
        preview_img.save(sample_path)
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
    return (h, -s)  # 色相昇順、彩度降順

# 色相昇順、彩度降順でソート
image_files.sort(key=get_color_info)

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
