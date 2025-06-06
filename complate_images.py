from PIL import Image, ImageDraw, ImageFont
import os

# samplesディレクトリ内の画像ファイル名を取得（拡張子pngのみ、ソート）
samples_dir = 'samples'
output_path = 'complate.png'

image_files = [f for f in os.listdir(samples_dir) if f.endswith('.png') and f != 'complate.png']
image_files.sort()  # ファイル名順

# 画像を開く
images = [Image.open(os.path.join(samples_dir, fname)) for fname in image_files]

# 3列で折り返し
cols = 3
rows = (len(images) + cols - 1) // cols

# 各画像のサイズを取得
widths, heights = zip(*(img.size for img in images))
img_w = max(widths)
img_h = max(heights)

# フォント設定
try:
    # Windowsのメイリオ（なければデフォルト）
    font = ImageFont.truetype('meiryo.ttc', 28)
except:
    font = ImageFont.load_default()

# ラベル高さ
label_h = 36

# 新しい画像サイズ
canvas_w = cols * img_w
canvas_h = rows * (img_h + label_h)

# 背景を白に変更
new_img = Image.new('RGBA', (canvas_w, canvas_h), (255,255,255,255))
draw = ImageDraw.Draw(new_img)

for idx, (img, fname) in enumerate(zip(images, image_files)):
    row = idx // cols
    col = idx % cols
    x = col * img_w
    y = row * (img_h + label_h)
    # 画像を白背景で合成
    bg = Image.new('RGBA', (img_w, img_h), (255,255,255,255))
    bg.paste(img, (0, 0), img if img.mode == 'RGBA' else None)
    new_img.paste(bg, (x, y))
    # ファイル名（拡張子除去）
    label = os.path.splitext(fname)[0]
    # テキストの中央揃え（Pillow>=8.0.0ならtextbbox推奨）
    try:
        bbox = draw.textbbox((0,0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(label)
    text_x = x + (img_w - text_w) // 2
    text_y = y + img_h + (label_h - text_h) // 2
    draw.text((text_x, text_y), label, fill=(0,0,0,255), font=font)

# 保存
new_img.save(output_path)
print(f'結合画像を保存しました: {output_path}')
