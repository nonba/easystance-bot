# easystanceapp 自動投稿ツール

posts.txt に登録した文面を、1回実行するたびに1件ずつ順番に（使い切ったらシャッフルして再スタート）Xへ投稿するツールです。

## セットアップ

1. Python 3.9以上がインストールされていること
2. 依存パッケージをインストール

   ```bash
   pip install -r requirements.txt
   ```

3. `.env.example` をコピーして `.env` を作成し、X Developer Portal で取得した4つの値を入力

   ```bash
   cp .env.example .env
   ```

   `.env` は絶対にGitや他人と共有しないでください。

4. 動作確認（実際には投稿されません）

   ```bash
   python poster.py --dry-run
   ```

5. 本番投稿

   ```bash
   python poster.py
   ```

## 投稿内容を編集する

`posts.txt` をメモ帳などで開いて自由に編集してください。「----------」の区切り線までが1つの投稿（1ツイート）です。
文章の書き換え・追加・削除、いずれも区切り線を保ったまま自由にどうぞ。
280字（日本語は目安140字前後）を超えないよう注意してください。
全件投稿し終えると自動的にシャッフルされて最初からまた回ります。

## 毎日自動実行する（Windows タスクスケジューラ）

PowerShellを管理者として開き、以下を実行（時刻は9:00の例。パスは環境に合わせて書き換えてください）:

```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "poster.py" -WorkingDirectory "C:\path\to\easystance-bot"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00am
Register-ScheduledTask -TaskName "EasyStanceAutoPost" -Action $action -Trigger $trigger -Description "easystanceapp 毎日自動投稿"
```

タスクの確認・削除:

```powershell
Get-ScheduledTask -TaskName "EasyStanceAutoPost"
Unregister-ScheduledTask -TaskName "EasyStanceAutoPost" -Confirm:$false
```

## ログ

投稿の成功・失敗は `post_log.txt` に記録されます。失敗した場合はまずここを確認してください
（キーの権限がRead and Writeになっているか、.envの値が正しいか、など）。
