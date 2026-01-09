#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub リポジトリの QRコード生成スクリプト
"""

import qrcode
from pathlib import Path
from PIL import Image

def generate_qr_code(url, output_path, logo_path=None, box_size=10, border=4):
    """
    QRコードを生成して PNG ファイルとして保存
    
    Args:
        url (str): QRコード化する URL
        output_path (str): 出力ファイルのパス
        logo_path (str): ロゴ画像のパス（オプション）
        box_size (int): 1ボックスのピクセルサイズ
        border (int): 枠線のボーダーサイズ
    """
    try:
        # QRコード生成
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 最高レベルの誤り訂正
            box_size=box_size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 画像生成
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # ロゴを埋め込む場合
        if logo_path and Path(logo_path).exists():
            try:
                logo = Image.open(logo_path).convert('RGBA')
                # ロゴサイズを QRコードの 1/5 に縮小
                logo_size = img.size[0] // 5
                logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # ロゴの背景を白にして中央に配置
                logo_bg = Image.new('RGB', img.size, 'white')
                logo_pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                # ロゴの透明部分を考慮して合成
                logo_bg.paste(img, (0, 0))
                logo_bg.paste(logo, logo_pos, logo)
                img = logo_bg
            except Exception as e:
                print(f"⚠️  ロゴ埋め込み失敗: {e}")
        
        # RGB に変換（PNG 保存用）
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # 保存
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        
        print(f"✅ QRコード生成完了！")
        print(f"📁 保存先: {output_path.resolve()}")
        print(f"📏 サイズ: {img.size[0]}x{img.size[1]} px")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == "__main__":
    # GitHub リポジトリ URL
    GITHUB_URL = "https://fuku86.github.io/exhibit-nubuck/"
    
    # 出力ファイルパス
    OUTPUT_PATH = Path(__file__).parent / "qr_code.png"
    
    # ロゴパス
    LOGO_PATH = Path(__file__).parent / "logo.png"
    
    # QRコード生成実行（ロゴ埋め込み）
    generate_qr_code(GITHUB_URL, OUTPUT_PATH, LOGO_PATH)

