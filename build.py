#!/usr/bin/env python3
"""
打包脚本 - 使用 PyInstaller 将 Python 应用打包成可执行程序
"""
import os
import sys
import subprocess
import platform

def build_executable():
    """构建可执行程序"""
    print("开始打包应用程序...")
    
    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个可执行文件
        "--windowed",  # Windows 应用（无命令行窗口）
        "--name", "AccountManager",  # 应用名称
        "--icon", "icon.ico" if os.path.exists("icon.ico") else None,  # 图标（如果存在）
        "--collect-all", "bcrypt",  # 包含 bcrypt
        "app.py"
    ]
    
    # 移除 None 值
    cmd = [x for x in cmd if x is not None]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ 打包成功！")
        
        # 输出路径信息
        if platform.system() == "Windows":
            exe_path = os.path.join("dist", "AccountManager.exe")
            print(f"可执行文件位置: {exe_path}")
        else:
            exe_path = os.path.join("dist", "AccountManager")
            print(f"可执行文件位置: {exe_path}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失败: {e}")
        return False
    except FileNotFoundError:
        print("\n✗ 错误：未找到 PyInstaller")
        print("请先运行: pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
