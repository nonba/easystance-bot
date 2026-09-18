"""
posts.txt に登録されている投稿候補を全件、番号付きで表示するスクリプト。
ローテーション状態(state.json)は変更しない。

実行方法:
    python list_drafts.py
"""

from poster import load_posts


def main():
    posts = load_posts()
    lines = []
    for i, text in enumerate(posts, start=1):
        lines.append(f"{i}. {text}")
    print("\n\n".join(lines))


if __name__ == "__main__":
    main()
