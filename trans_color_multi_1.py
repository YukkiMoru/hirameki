from PIL import Image
import os
import tkinter as tk
from PIL import ImageTk
import yaml  # 追加

# HEXカラーをRGBに変換
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# 2つの色の距離を計算
def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

# 任意の色を他の色に置換する関数
def replace_color(input_path, output_folder, from_color, to_color, threshold=30):
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
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.basename(input_path)
    img.save(os.path.join(output_folder, base_name))

# 設定ファイル(config.yml)から値を読み込む
with open('config.yml', encoding='utf-8') as f:
    config = yaml.safe_load(f)

from_color = config['from_color']
to_color = config['to_color']
threshold = config.get('threshold', 30)

# 以下はコード内で直接指定
num_images = 11  # 画像枚数
cols = 5         # 1行あたりの画像数
thumb_size = (120, 120)  # サムネイルサイズ

# 一括処理
for i in range(1, num_images + 1):
    fname = os.path.join('hirameki_original', f'ひらめき{i}.png')
    output_folder = f"hirameki_{to_color.lstrip('#')}"
    replace_color(fname, output_folder, from_color, to_color, threshold=threshold)

# 変換後画像のパス一覧を取得
output_folder = f"hirameki_{to_color.lstrip('#')}"
image_files = [os.path.join(output_folder, f"ひらめき{i}.png") for i in range(1, num_images + 1)]

root = tk.Tk()
root.title("変換後画像のプレビュー")

# 画像をグリッド（例：1行5列）で表示
# cols, thumb_sizeはYAMLから取得済み
frames = []
for idx, img_path in enumerate(image_files):
    img = Image.open(img_path)
    img.thumbnail(thumb_size, Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    frame = tk.Label(root, image=tk_img)
    frame.image = tk_img
    row = idx // cols
    col = idx % cols
    frame.grid(row=row, column=col, padx=5, pady=5)
    frames.append(frame)

root.mainloop()
