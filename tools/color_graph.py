# 色分布のグラフを作成するスクリプト
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3Dプロット用
import os
import sys
import colorsys
# 日本語フォントを指定
plt.rcParams['font.family'] = 'MS Gothic'  # または 'Meiryo' など
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from color import color_dict

# HEXカラーをRGBに変換
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# 色リスト
hex_colors = list(color_dict.keys())
color_names = list(color_dict.values())
rgb_colors = [hex_to_rgb(h) for h in hex_colors]

# RGB値を0-1に正規化
rgb_colors_norm = [(r/255, g/255, b/255) for r, g, b in rgb_colors]

# 表示フラグ（Trueで表示、Falseで非表示）
show_rgb = True   # 3Dグラフ（RGB空間）を表示する場合はTrue
show_hsv = False   # 色相-彩度グラフ（HSV平面）を表示する場合はTrue

# ハイライトする色（HEXで指定）
highlight_hex = '#FF0000'  # 例: 赤色をハイライト
highlight_rgb = hex_to_rgb(highlight_hex)
highlight_rgb_norm = tuple([v/255 for v in highlight_rgb])

if show_rgb:
    # 3Dプロット
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        [r for r, g, b in rgb_colors_norm],
        [g for r, g, b in rgb_colors_norm],
        [b for r, g, b in rgb_colors_norm],
        c=rgb_colors_norm,
        s=100,
        edgecolors='black',
        label='通常色'
    )
    # ハイライト色を強調表示
    if highlight_rgb_norm in rgb_colors_norm:
        idx = rgb_colors_norm.index(highlight_rgb_norm)
        ax.scatter(
            [highlight_rgb_norm[0]],
            [highlight_rgb_norm[1]],
            [highlight_rgb_norm[2]],
            c=[highlight_rgb_norm],
            s=400,
            edgecolors='gold',
            marker='*',
            label=f'ハイライト: {color_names[idx]}'
        )
        # ラベルも表示
        ax.text(
            highlight_rgb_norm[0],
            highlight_rgb_norm[1],
            highlight_rgb_norm[2],
            color_names[idx],
            fontsize=14,
            color='red',
            fontname='MS Gothic',
            weight='bold'
        )
    ax.set_xlabel('Red (正規化)')
    ax.set_ylabel('Green (正規化)')
    ax.set_zlabel('Blue (正規化)')
    ax.set_title('color.pyに含まれる色の分布 (R-G-B空間)')
    ax.legend()
    plt.tight_layout()
    plt.show()

if show_hsv:
    # HEXカラーをHSVに変換
    hsv_colors = [colorsys.rgb_to_hsv(r/255, g/255, b/255) for r, g, b in rgb_colors]
    hues = [h for h, s, v in hsv_colors]
    sats = [s for h, s, v in hsv_colors]

    plt.figure(figsize=(10, 8))
    plt.scatter(hues, sats, c=rgb_colors_norm, s=100, edgecolors='black')
    for i, name in enumerate(color_names):
        # オフセットを交互に加えて重なりを軽減
        offset = 0.05 if i % 2 == 0 else -0.05
        plt.text(hues[i], sats[i] + offset, name, fontsize=9, fontname='MS Gothic', ha='center', va='bottom')
    plt.xlabel('色相 (Hue)')
    plt.ylabel('彩度 (Saturation)')
    plt.title('color.pyに含まれる色の分布 (色相-彩度 平面)')
    plt.xlim(-0.05, 1.05)  # 端に余白を追加
    plt.ylim(-0.05, 1.05)  # 端に余白を追加
    plt.tight_layout()
    plt.show()