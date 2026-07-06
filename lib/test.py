"""测试文件 - 用于测试 lib 模块功能"""

import os
import platform
import subprocess
import threading


def test_compress_png(path: str) -> None:
    """测试 PNG 压缩功能"""
    try:
        result = subprocess.run(
            ["pngquant", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"pngquant 版本: {result.stdout.strip()}")
    except FileNotFoundError:
        print("警告: 未检测到 pngquant 命令行环境")


if __name__ == '__main__':
    print("运行 lib 模块测试...")
    test_compress_png("test.png")
    print("测试完成")
