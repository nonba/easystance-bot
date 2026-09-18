# easystanceapp 投稿案ツール

毎日20:07（JST）に、`posts.txt` から1件を選んでGitHub Issueとして通知するツールです。
Xへは自動投稿せず、内容を確認・修正してから自分でXに投稿する運用です。

GitHub Actions（GitHubのクラウド機能）で動くので、PCの電源が入っていなくても毎日実行されます。

## 使い方

1. 毎日20:07になると、このリポジトリに「YYYY-MM-DD の投稿案」というIssueが自動で作成されます
2. GitHubの通知（メール等）が届くので、内容を確認します
3. 気になる部分を直して、Xアプリ／サイトから自分で投稿します
4. Issueはそのままでも、確認済みとして閉じてもどちらでも構いません

## 投稿の候補（ネタ）を編集する

`posts.txt` をGitHubのサイト上で直接編集するのが簡単です。

1. https://github.com/nonba/easystance-bot/blob/master/posts.txt を開く
2. 右上の鉛筆マーク（編集アイコン）をクリック
3. 文章を書き換えて、下の方にある緑の「Commit changes」ボタンを押す

「----------」の区切り線までが1つの候補です。区切り線を保ったまま、文章の書き換え・追加・削除は自由にどうぞ。
280字（日本語は目安140字前後）を超えないよう注意してください。
全件使い終えると自動的にシャッフルされて最初からまた回ります。

## 手動で今すぐ候補を出したいとき

リポジトリの Actions タブ → 「Daily draft notification」→ 「Run workflow」で、いつでも手動実行できます。
https://github.com/nonba/easystance-bot/actions

## ローカルで動作確認したいとき

```bash
pip install -r requirements.txt
python pick_draft.py
```

を実行すると、次の候補文がその場に表示されます（GitHub Issueは作られません）。

## 参考：以前のXへの自動投稿機能について

`poster.py` にはXへ直接投稿する機能も残していますが、現在の自動実行では使っていません
（`.env` にX APIキーを設定すれば `python poster.py` で手動投稿は可能です）。
再び完全自動投稿に戻したくなったら、いつでも相談してください。
