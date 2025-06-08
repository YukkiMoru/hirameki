import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from color import color_dict

change_color = True

try:
    import webcolors
except ImportError:
    print('webcolorsパッケージが必要です。pip install webcolors でインストールしてください。')
    sys.exit(1)

def get_en_name(hex_code):
    try:
        return webcolors.hex_to_name(hex_code), hex_code, False
    except ValueError:
        # 近い色名とそのカラーコードを取得
        try:
            rgb = webcolors.hex_to_rgb(hex_code)
            min_colors = {}
            for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - rgb[0]) ** 2
                gd = (g_c - rgb[1]) ** 2
                bd = (b_c - rgb[2]) ** 2
                min_colors[(rd + gd + bd)] = (name, key)
            closest = min_colors[min(min_colors.keys())]
            return closest[0] + ' (近似)', closest[1], True
        except Exception:
            return '不明', hex_code, False

def get_hex_from_en_name(en_name):
    try:
        return webcolors.name_to_hex(en_name)
    except Exception:
        return None

# 日本語名→英語名の簡易辞書
jp_to_en = {
    '青': 'blue',
    '緑': 'green',
    'グレー': 'gray',
    '紫': 'purple',
    'ピンク': 'pink',
    '黄緑': 'yellowgreen',
    '茶色': 'brown',
    'フォレストグリーン': 'forestgreen',
    'エレクトリックシアン': 'cyan',
    'バーントアンバー': 'saddlebrown',  # 近い色
    'シャムロックグリーン': 'mediumspringgreen',  # 近い色
}

unknown_colors = []
print(f'{"カラーコード":<20}{"日本語名":<30}{"英語標準色名":<24}{"書換"}')
for code, jp_name in color_dict.items():
    en_name, new_code, changed = get_en_name(code)
    flag = '◯' if changed else ''
    if changed:
        code_display = f'{code}->{new_code}'
    else:
        code_display = code
    print(f'{code_display:<20}{jp_name:<30}{en_name:<24}{flag}')
    if en_name == '不明':
        # 日本語名から英語名を引いてカラーコードを取得
        if jp_name in jp_to_en:
            en = jp_to_en[jp_name]
            hex_code = get_hex_from_en_name(en)
            if hex_code:
                print(f'  → {jp_name} → {en} → {hex_code}')
        unknown_colors.append((jp_name, code))

if unknown_colors:
    print('\n不明な色名リスト:')
    for jp_name, code in unknown_colors:
        # 推奨カラーコードを探す
        if jp_name in jp_to_en:
            en = jp_to_en[jp_name]
            hex_code = get_hex_from_en_name(en)
            if hex_code:
                print(f'{jp_name} ({code}) → 推奨: {hex_code} ({en})')
            else:
                print(f'{jp_name} ({code}) → 推奨なし')
        else:
            print(f'{jp_name} ({code}) → 推奨なし')
