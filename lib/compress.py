"""_summary_
作者：xinyu3ru 
代码部分参考https://www.jianshu.com/p/649cf285b21b，代码备份./test.py
"""

import logging
import os
import subprocess
import threading
from typing import List

from PIL import Image

from lib.util import convert_mb_kb, is_jpg_file, is_png_file


def compress_jpg(path: str, width: int = 720, quality: int = 85) -> None:
    byteSizeBefore = os.path.getsize(path)
    img: Image.Image = Image.open(path)
    w, h = img.size
    if w > width:
        h = int(h * width / w)
        w = width
        logging.info(f"图片宽度超过 {width} px,调整为{w}x{h} px。")
    img = img.resize((w, h), Image.LANCZOS)
    img.save(path, quality=quality, optimize=True)
    byteSizeAfter = os.path.getsize(path)
    logging.info(f"{path} , 压缩前：{convert_mb_kb(byteSizeBefore)}, 压缩后：{convert_mb_kb(byteSizeAfter)}。")


def compress_png(path: str) -> None:
    try:
        result = subprocess.run(
            ["pngquant", "256", "--quality=65-80", "--skip-if-larger", "--force", "--ext", ".png", path],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        logging.error("未检测到pngquant命令行环境，请参照pngquant官网搭建命令行环境：https://pngquant.org/")
    except subprocess.CalledProcessError as e:
        logging.error(f"压缩PNG失败 {path}: {e.stderr}")


def _compress_image(path: str) -> None:
    logging.info(f"开始压缩图片路径：{path}")
    if is_jpg_file(path):
        compress_jpg(path)
    elif is_png_file(path):
        compress_png(path)
    logging.info(f"结束压缩图片路径：{path}")


def compress_pic(path_list: List[str]) -> None:
    threads = []
    for filepath in path_list:
        thread = threading.Thread(target=_compress_image, args=(filepath,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()




