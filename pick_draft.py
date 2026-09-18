"""
毎日の投稿「候補」を1件選んで表示するスクリプト。
Xには投稿しない。posts.txt のローテーションだけ進めて state.json に保存する。

実行方法:
    python pick_draft.py
"""

import sys

from poster import load_posts, load_state, save_state, next_post


def main():
    posts = load_posts()
    if not posts:
        print("エラー: posts.txt に投稿がありません。", file=sys.stderr)
        sys.exit(1)

    state = load_state(len(posts))
    text = next_post(posts, state)
    save_state(state)

    print(text)


if __name__ == "__main__":
    main()
