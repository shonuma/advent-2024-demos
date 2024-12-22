# Google Cloud Advent Calendar 通常版 12/23 デモ用

## ローカルでの動作
依存ライブラリをインストールします。
```
pip install -r requirements.txt
```

.env ファイルを作成します。
```
.env
```

以下の環境変数を `.env` に設定します。
```
export PROJECT_ID=<%PROJECT_ID%>
export GRADIO_SERVER_PORT=8080
```

サーバーを実行します。
```
bash run.sh
```

## Cloud Run での動作

事前準備
- 必要な API を有効化してください。
- Cloud Run を動作させるサービスアカウントに `Vertex AI ユーザー` を設定してください。
- Dockerfile 内の PROJECT_ID を動作させる Google Cloud プロジェクトのIDに設定してください。

デプロイを実行します。
```
gcloud run deploy service_name --source . --region us-central1 --allow-unauthenticated
```