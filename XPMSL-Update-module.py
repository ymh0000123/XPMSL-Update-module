import subprocess
import requests
import tkinter as tk
from tkinter import messagebox
import os
import argparse
import sys

Build = "20240210"
def open_announcement():
    # 创建解析器
    parser = argparse.ArgumentParser(description='处理命令行参数的示例。')
    
    # 添加 '-v' 或 '--verbose' 选项
    parser.add_argument('-b', '--Build', action='store_true', help='查看版本号')
    
    # 解析命令行参数
    args = parser.parse_args()

    # 根据 '-v' 或 '--verbose' 选项是否存在来决定程序行为
    if args.Build:
        print(Build)
        # 执行一些操作后，退出程序
        sys.exit()
open_announcement()

def check_for_update():
    try:
        output = subprocess.check_output(["XPMSL.exe", "-b"], text=True).strip()
        current_build = int(output)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", "无法执行 XPMSL.exe -b 命令")
        return

    try:
        response = requests.get("https://xpmsl.pages.dev/releases.json")
        response.raise_for_status()
        latest_build = int(response.json()['build'])
        download_url = f"https://slink.ltd/https://github.com/ymh0000123/XPMSL/releases/download/V{response.json()['releases']}/XPMSL.exe"
    except (requests.RequestException, KeyError) as e:
        messagebox.showerror("错误", "获取最新版本信息失败")
        return

    if current_build < latest_build:
        answer = messagebox.askyesno("更新提示", "有新版本可用！是否要更新？")
        if answer:
            download_update(download_url)
    else:
        if current_build > latest_build:
            messagebox.showinfo("提示", "注意！你正在使用的可能是测试版。")
        else:
            messagebox.showinfo("提示", "您的版本是最新的。")

def download_update(download_url):
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        with open("XPMSL_update.exe", "wb") as f:
            f.write(response.content)
        
        # 替换原来的XPMSL.exe
        os.replace("XPMSL_update.exe", "XPMSL.exe")

        messagebox.showinfo("提示", "更新已下载完成。")
    except requests.RequestException as e:
        messagebox.showerror("错误", "下载更新失败")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    check_for_update()
