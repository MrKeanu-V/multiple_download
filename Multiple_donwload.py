import os

import requests
import time
from tqdm import tqdm

# 模拟浏览器检测头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# 读取文本文件
with open('download_list.txt', 'r') as file:
    links = file.readlines()
with open('rename.txt', 'r', encoding='utf-8') as file:
    names = file.readlines()

# 指定保存路径
save_dir = os.path.join(os.getcwd(), "DownloadFiles")
os.makedirs(save_dir, exist_ok=True)

# 去除每个链接开头和结尾的空白符
# links = [link.strip() for link in links]

# 下载失败链接
failed_links = []

# 遍历链接并下载文件
for name, link in tqdm(zip(names, links), total=len(names), desc="正在下载"):
    # 提取文件名，需要用strip去掉换行符
    filename = name.split('+')[-1].strip() + ".mp4"
    # 发送请求
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        save_path = os.path.join(save_dir, filename)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"已下载文件: {filename}")
    else:
        failed_links.append((filename, link))
        print(f"无法下载链接: {link}")

# 失效链接
error_links = []
for filename, link in tqdm(failed_links, desc="尝试重新下载失败链接"):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"已下载文件: {filename}")
    else:
        error_links.append((filename, link))
        print(f"无法下载链接: {link}")

if len(error_links) > 0:
    with open('failed_list.txt', 'w', encoding='utf-8') as file:
        for filename, link in failed_links:
            file.write(f'{filename}\t{link}\n')

print("失败链接已保存在failed_list.txt文件中，请尝试手动下载")

response.close()
