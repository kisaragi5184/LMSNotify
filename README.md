# LMSNotify

1.通知を送りたいDiscordサーバーでWebhookを作成
サーバー設定 → 「連携サービス」→「Webhook」→「新規作成」
Webhook URLをコピー（後で使う）

2.LMSのカレンダーを開く→ カレンダをエクスポート
エクスポートするイベントは「コースに関連したイベント」
期間は「カスタム範囲」を推奨 

1,2で取得したURLをLMS_assignment_notify.pyの該当箇所に入力
実行すれば締め切り24時間以内の課題を取得してdiscordで通知してくれる
