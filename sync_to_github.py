import requests
import json
import time

STEAM_API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

def fetch_steam_games():
    print("正在拉取Steam全部游戏列表...")
    
    for attempt in range(3):
        try:
            print(f"第{attempt+1}次尝试...")
            resp = requests.get(
                STEAM_API_URL,
                timeout=120,
                headers={"Accept-Encoding": "gzip"}
            )
            resp.raise_for_status()
            
            if not resp.content:
                raise ValueError("响应内容为空")
            
            data = resp.json()
            games = [
                {"appid": app["appid"], "name": app["name"]}
                for app in data["applist"]["apps"]
                if app["name"].strip()
            ]
            print(f"共获取到 {len(games)} 个游戏")
            return games
            
        except (requests.exceptions.JSONDecodeError, ValueError) as e:
            print(f"第{attempt+1}次失败 (JSON解析错误): {e}")
            if attempt < 2:
                print("等待10秒后重试...")
                time.sleep(10)
        except requests.exceptions.Timeout:
            print(f"第{attempt+1}次失败 (超时)")
            if attempt < 2:
                print("等待10秒后重试...")
                time.sleep(10)
        except requests.exceptions.HTTPError as e:
            print(f"第{attempt+1}次失败 (HTTP错误): {e}")
            if attempt < 2:
                time.sleep(10)
        except Exception as e:
            print(f"第{attempt+1}次失败 (未知错误): {e}")
            if attempt < 2:
                time.sleep(10)
    
    raise RuntimeError("3次重试均失败，无法获取Steam游戏列表")

if __name__ == "__main__":
    games = fetch_steam_games()
    with open("games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    print("games.json 已保存")
