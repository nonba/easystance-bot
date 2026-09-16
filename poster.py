"""
easystanceapp 用の定時自動投稿スクリプト。

1回実行するたびに posts.txt から1件を選んでXに投稿し、
state.json に「次はどれを投稿するか」を保存する。
posts.txt を全部使い切ったら、順番をシャッフルして最初からまた回す。

実行方法:
    python poster.py            通常実行（Xに投稿する）
    python poster.py --dry-run  投稿はせず、次に投稿される文面を表示するだけ
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "posts.txt"
STATE_FILE = BASE_DIR / "state.json"
LOG_FILE = BASE_DIR / "post_log.txt"

DELIMITER = "----------"


def load_posts():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 先頭の説明書き（最初の区切り線より前の部分）は投稿として扱わない
    chunks = content.split(DELIMITER)[1:]
    posts = [chunk.strip() for chunk in chunks]
    return [p for p in posts if p]


def load_state(num_posts):
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("order") and len(state["order"]) == num_posts:
            return state
    order = list(range(num_posts))
    random.shuffle(order)
    return {"order": order, "position": 0}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def next_post(posts, state):
    if state["position"] >= len(state["order"]):
        order = list(range(len(posts)))
        random.shuffle(order)
        state["order"] = order
        state["position"] = 0

    idx = state["order"][state["position"]]
    state["position"] += 1
    return posts[idx]


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_client():
    import tweepy

    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    missing = [
        name
        for name, val in [
            ("X_API_KEY", api_key),
            ("X_API_SECRET", api_secret),
            ("X_ACCESS_TOKEN", access_token),
            ("X_ACCESS_TOKEN_SECRET", access_token_secret),
        ]
        if not val
    ]
    if missing:
        log(f"エラー: .env に未設定の項目があります: {', '.join(missing)}")
        sys.exit(1)

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="投稿せずに次の投稿文を表示するだけ",
    )
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")

    posts = load_posts()
    if not posts:
        log("エラー: posts.txt に投稿がありません。")
        sys.exit(1)

    state = load_state(len(posts))
    text = next_post(posts, state)

    if args.dry_run:
        print("---- 次に投稿される文面 (dry-run) ----")
        print(text)
        print(f"文字数: {len(text)}")
        return

    client = get_client()
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data.get("id")
        log(f"投稿成功 (id={tweet_id}): {text}")
        save_state(state)
    except Exception as e:
        log(f"投稿失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
