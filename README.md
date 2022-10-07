# 使い方
本アプリは、バックエンドにPythonのFastAPI、フロントエンドにViteをつかったVue.js3で開発を行っておりまふ。

# 環境設定
## Gitからダウンロード

`gh repo clone supplepentan/penta_subject_extraction`

`cd penta_subject_extraction` 

## バックエンド(Python)の設定

`cd app`

`python -m venv venv`

`venv/scripts/activate`

`python -m pip install -r requirements.txt`

## フロントエンド（Vite、Vue.js3、TailwindCSS）の設定（テストだけ行いたければ必要ありまふぇん）

`cd front_vite`

`npm install`

### Vue.jsの起動（開発時）

`npm run dev`

# テスト

`cd app`

`venv/scripts/activate`

`uvicorn main:app --reload`

http://127.0.0.1:8000にアクセス