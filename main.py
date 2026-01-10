# 请先阅读README.md

from CodemaoEDUTools import *  # noqa: F403
import requests
import json
import os
import time


def save_workid(workid, path="workid.json"):
    if not os.path.exists(path):
        data = {"workids": []}
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    data["workids"].append(workid)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


print("欢迎使用，请先阅读README.md!")
print("=========================")

user = input("请输入编程猫账号：")
password = input("请输入编程猫账号密码：")
tokenfile = input("请输入Token文件存放路径：")

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

# 开始创建作品

for i in range(1, 26):
    print(f"请稍后，创建作品，编号：{i}")
    # 获取 WorkID
    workid = json.loads(
        requests.post(
            url="https://api-creation.codemao.cn/kitten/r2/work",
            json={
                "name": "临时作品-" + str(i),
                "work_url": "https://creation.bcmcdn.com/445/kitten/d2ViXzIwMDJfMTQ1ODIyNzEwM18xXzE3Njc5NzAyMDU5MjNfY2U2NGFhYmM=.bcm4",
                "preview": "https://creation.bcmcdn.com/445/kitten/d2ViXzIwMDFfMTQ1ODIyNzEwM18xXzE3Njc5NzAyMDU2MTRfY2RhNTQ1MzM=",
                "orientation": 1,
                "sample_id": "",
                "version": "4.11.18",
                "work_source_label": 1,
                "save_type": 2,
            },
            headers=headers,
        ).text
    ).get("id")

    # 发布作品
    req = requests.put(
        url=f"https://api-creation.codemao.cn/kitten/r2/work/{workid}/publish",
        json={
            "work_id": workid,
            "name": "临时作品-" + str(i),
            "description": "文件由CodemaoLV5自动创建，为临时作品",
            "operation": "请在统计结束后删除这些作品，在README中有说明",
            "labels": [],
            "cover_url": "https://creation.bcmcdn.com/445/kitten/d2ViXzIwMDFfMTQ1ODIyNzEwM18zMDAzNzI1MjFfMTc2Nzk3MDU3ODY4Ml83ZGI0YjA0MA==.png",
            "fork_enable": 1,
            "cover_type": 1,
            "version": "4.11.18",
            "user_labels": [],
            "bcmc_url": "https://creation.bcmcdn.com/445/kitten/d2ViXzIwMDJfMTQ1ODIyNzEwM18zMDAzNzI1MjFfMTc2Nzk3MDU3OTQ2Ml9iNDAzZWUxMA==.json",
            "work_url": "https://creation.bcmcdn.com/445/kitten/d2ViXzIwMDJfMTQ1ODIyNzEwM18zMDAzNzI1MjFfMTc2Nzk3MDU3OTE3MF82NTY4MGY0MQ==.bcm4",
            "if_default_cover": 1,
        },
        headers=headers,
    )

    if req.status_code == 200:
        # 请求成功
        save_workid(workid)
        time.sleep(5)  # 防止操作过于频繁
        print("等待一会，防止Autoban发力...")
    else:
        # 请求失败
        exit(f"请求失败：{req.text}")

# 开始刷数据

count = 0

with open("workid.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i in data["workids"]:
    count = count + 1
    print(f"=====开始作品ID：{i} | 第{count}个=====")
    # 点赞作品
    if LikeWork(tokenfile, i):  # noqa: F405
        print("点赞完毕")
    if CollectionWork(tokenfile, i):  # noqa: F405
        print("收藏完毕")
    if ForkWork(tokenfile, i):  # noqa: F405
        print("再创作完毕")
    print(f"=====结束作品ID：{i}| 余{25 - count}个=====")

# 结束

print("脚本运行完成，请在数据更新后执行 delete.py~")