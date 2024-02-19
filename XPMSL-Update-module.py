import requests
import json
import os
import subprocess
import time

# 读取本地releases.json文件，并容错处理
def read_local_build():
    try:
        with open(os.path.join('XPMSL', 'releases.json'), 'r') as file:
            data = json.load(file)
        return data.get('Build')  # 使用get避免KeyError
    except FileNotFoundError:
        print("本地releases.json文件未找到。")
        return None

# 从远程获取releases.json并返回build值和releases值
def fetch_remote_build_and_releases():
    url = 'https://xpmsl.pages.dev/releases.json'
    response = requests.get(url)
    data = response.json()
    return data.get('build', 0), data.get('releases')  # 对build使用默认值0，对releases没有默认值

# 关闭XPMSL.exe程序
def close_xpmsl():
    try:
        subprocess.run("taskkill /f /im XPMSL.exe", shell=True, check=True)
        print("XPMSL.exe已关闭")
    except subprocess.CalledProcessError as e:
        print("关闭XPMSL.exe时出错:", e)

# 下载新版本的XPMSL.exe
def download_new_version(releases):
    download_url = f"https://slink.ltd/https://github.com/ymh0000123/XPMSL/releases/download/V{releases}/XPMSL.exe"
    response = requests.get(download_url)
    with open('XPMSL.exe.new', 'wb') as file:
        file.write(response.content)
    print("新版本下载完成")

    # 替换原来的XPMSL.exe
    try:
        os.replace('XPMSL.exe.new', 'XPMSL.exe')
        print("XPMSL.exe替换完成")
    except FileNotFoundError:
        print("替换XPMSL.exe时出错：找不到文件")
    except PermissionError:
        print("替换XPMSL.exe时出错：权限不足")

def main():
    local_build = read_local_build()
    if local_build is None:
        return  # 如果本地build读取失败，则终止程序

    remote_build, releases = fetch_remote_build_and_releases()

    if remote_build is not None and remote_build > local_build:
        print("发现新版本，开始下载...")
        close_xpmsl()  # 关闭XPMSL.exe
        time.sleep(2)  # 等待2秒确保程序关闭
        download_new_version(releases)
    else:
        print("当前已是最新版本。")

if __name__ == "__main__":
    main()
