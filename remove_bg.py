#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像の白背景を透明に変換するスクリプト
"""

from PIL import Image
import os


def remove_white_background(input_path, output_path, threshold=200):
    """
    白色背景を透明に変換
    
    Args:
        input_path (str): 入力画像パス
        output_path (str): 出力画像パス (PNG推奨)
        threshold (int): 白判定の閾値 (0-255)。高いほど白に近い色を透明化
    """
    try:
        # 画像を RGBA モードで開く
        img = Image.open(input_path).convert('RGBA')
        
        # ピクセルデータ取得
        data = img.getdata()
        
        # 白色（またはそれに近い色）を透明に変換
        new_data = []
        for item in data:
            # R, G, B が全て threshold 以上なら白と判定して透明に
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0))  # 透明
            else:
                new_data.append(item)
        
        # 新しいデータをセット
        img.putdata(new_data)
        
        # 保存
        img.save(output_path)
        print(f"✅ 背景透明化完了！")
        print(f"📁 入力: {input_path}")
        print(f"📁 出力: {output_path}")
        print(f"📏 サイズ: {img.size[0]}x{img.size[1]} px")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == "__main__":
    # 使用例：
    remove_white_background('logo_white.png', 'logo.png')