# 此脚本用于删除已发布的作品
import os
import requests
import json
import time
from CodemaoEDUTools import *  # noqa: F403

print("欢迎使用，这个脚本用于删除已发布的作品")
print("=========================")

# 登录
user = input("请输入编程猫账号：")
password = input("请输入编程猫账号密码：")

print("尝试登录...")

token = GetUserToken(user, password)  # noqa: F405

if not token:
    exit("登录失败")

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "authorization": token,
}

# 确认文件

if not os.path.exists("workid.json"):
    exit("找不到生成的作品ID文件")

# 开始运行

count = 0

with open("workid.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i in data["workids"]:
    count = count + 1
    print(f"=====开始作品ID：{i} | 第{count}个=====")
    # 解除作品的发布状态
    if (
        requests.put(
            url=f"https://api.codemao.cn/web/works/r2/unpublish/{i}", headers=headers
        ).status_code
        == 200
    ):
        print("解除发布状态成功")
    else:
        print("解除发布状态失败")
    time.sleep(1)
    # 删除作品
    if (
        requests.delete(
            url=f"https://api-creation.codemao.cn/kitten/common/work/{i}/temporarily",
            headers=headers,
        ).status_code
        == 200
    ):
        print("删除作品成功")
    else:
        print("删除作品失败")
    time.sleep(4)
    print("等待一会，防止Autoban发力...")

    print(f"=====结束作品ID：{i}| 余{25 - count}个=====")

os.remove("workid.json")

print("运行完毕，尽情享用吧~")