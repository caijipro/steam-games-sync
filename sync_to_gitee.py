import requests
import base64
import json
import datetime
import os

# 
GITEE_OWNER = "Steam-Games-gitee"  # 
GITEE_REPO = "steam-games-public"  # 
GITEE_TOKEN = os.environ.get("GITEE_TOKEN")
GITEE_FILE = "games.json"
GITEE_API = f"https://gitee.com/api/v5/repos/{GITEE_OWNER}/{GITEE_REPO}/contents/{GITEE_FILE}"
STEAM_API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

def fetch_steam_games():
    print("正在拉取Steam全部游戏列表...")
    resp = requests.get(STEAM_API_URL, timeout=60)
    data = resp.json()
    games = [
        {"appid": app["appid"], "name": app["name"]}
        for app in data["applist"]["apps"] if app["name"]
    ]
    print(f"共获取到{len(games)}个游戏")
    return games

def get_gitee_file_sha():
    url = f"{GITEE_API}?access_token={GITEE_TOKEN}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()["sha"]
    return None

def upload_to_gitee(games):
    content = base64.b64encode(json.dumps(games, ensure_ascii=False, indent=2).encode("utf-8")).decode()
    sha = get_gitee_file_sha()
    data = {
        "access_token": GITEE_TOKEN,
        "content": content,
        "message": f"update games.json {datetime.datetime.now()}",
    }
    if sha:
        data["sha"] = sha
    resp = requests.put(GITEE_API, json=data)
    if resp.status_code in (200, 201):
        print("上传到Gitee成功！")
    else:
        print("上传失败：", resp.text)

if __name__ == "__main__":
    games = fetch_steam_games()
    upload_to_gitee(games)
