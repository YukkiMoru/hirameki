from PIL import Image
import os

# 設定
from_color_hex = '#FFFF00'  # 置換元の色（例：黄色）
threshold = 100          # 色のしきい値

# 入力フォルダと出力フォルダの設定
input_folder = 'hirameki_original'
output_folder = 'hirameki_binary'

# 出力フォルダがなければ作成
os.makedirs(output_folder, exist_ok=True)

# 入力フォルダ内の画像ファイルを取得
try:
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
except FileNotFoundError:
    print(f"エラー: 入力フォルダ '{input_folder}' が見つかりません。")
    exit()

if not image_files:
    print(f"入力フォルダ '{input_folder}' に画像ファイルが見つかりません。")
    exit()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

from_color_rgb = hex_to_rgb(from_color_hex)

print(f"'{input_folder}' から画像を読み込み、色 '{from_color_hex}' (しきい値: {threshold}) に基づいて二値化処理を開始します...")

for filename in image_files:
    try:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 画像を開く
        img = Image.open(input_path).convert('RGB')
        pixels = img.load()

        # 新しい二値化画像を作成 (白黒)
        binary_img = Image.new('1', img.size) # '1' モードで1ビットピクセル、白黒
        binary_pixels = binary_img.load()

        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                if color_distance((r, g, b), from_color_rgb) < threshold:
                    binary_pixels[x, y] = 255  # 白
                else:
                    binary_pixels[x, y] = 0    # 黒

        # 二値化画像を保存
        binary_img.save(output_path)
        print(f"'{filename}' を二値化し、'{output_path}' に保存しました。")

    except Exception as e:
        print(f"ファイル '{filename}' の処理中にエラーが発生しました: {e}")

print("すべての画像の二値化処理が完了しました。")
