import requests
import json

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

if __name__ == "__main__":
    games = fetch_steam_games()
    with open("games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
