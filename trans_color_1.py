from PIL import Image
import os
import tkinter as tk
from PIL import ImageTk

# HEXカラーをRGBに変換
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# 2つの色の距離を計算
def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

# 任意の色を他の色に置換する関数
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

# 変換元・変換先カラーコード
from_color = '#FFFF00'  # 置換元の色（例：黄色）
to_color = "#00B3FF"  # 置換先の色（例：緑）
threshold = 30          # 色のしきい値
save = False  # 保存するかどうか
num_images = 11 # 画像枚数を変数で指定

# 一括処理
for i in range(1, num_images + 1):
    fname = os.path.join('hirameki_original', f'ひらめき{i}.png')
    output_folder = f"hirameki_{to_color.lstrip('#')}"
    replace_color(fname, output_folder, from_color, to_color, threshold=threshold, save=save)

# 変換後画像のパス一覧を取得
output_folder = f"hirameki_{to_color.lstrip('#')}"
image_files = [os.path.join(output_folder, f"ひらめき{i}.png") for i in range(1, num_images + 1)]

root = tk.Tk()
root.title("変換後画像のプレビュー")

# 画像をグリッド（例：1行5列）で表示し、縦横比を維持して縮小
cols = 5  # 1行あたりの画像数
thumb_size = (150, 150)  # サムネイル最大サイズ
frames = []
for idx, img_path in enumerate(image_files):
    img = Image.open(img_path)
    img.thumbnail(thumb_size, Image.LANCZOS)  # 縦横比維持で縮小
    tk_img = ImageTk.PhotoImage(img)
    frame = tk.Label(root, image=tk_img)
    frame.image = tk_img  # 参照保持
    row = idx // cols
    col = idx % cols
    frame.grid(row=row, column=col, padx=5, pady=5)
    frames.append(frame)

root.mainloop()
