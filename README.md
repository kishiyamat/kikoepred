# README

![](https://docs.google.com/drawings/d/1dvrN2Thqb2PAi_fQFFx0x4VEPq_vVYBM8zB1ES2SlZ4/pub?w=960&amp;h=720)

HerokuでStreamlitアプリを
30分でデプロイするテンプレート
各ステップの詳細は後述します。

| Task                         | Duration  |
|------------------------------|-----------|
| リポジトリをクローン            | 1 min     |
| Herokuにデプロイ               | 5 min     |
| ドメイン取得                   | 5 min     |
| HerokuでPointDNSを設定         | 5 min     |
| ドメインでネームサーバーの設定| 5 min     |
| HerokuでConfigure SSL         | 1 min     |
| 待つ                          | 5--8 mins |

- 環境変数: `.streamlit/secrets.toml`
- Pythonのバージョン: `runtime.txt`
- 起動するアプリ: `Procfile`
- ライブラリ: `requirements.txt` (以下はデフォルト)
    - streamlit
    - pytest

# カスタムドメイン

1. リポジトリをクローン
1. Herokuにデプロイ
1. ドメイン取得
1. HerokuでPointDNSを設定
1. ドメインの設定（ネームサーバー）
1. HerokuでConfigure SSL

# Local

- pyenvで特定のバージョンのPythonを入れる

```sh
$ python -m venv venv
```

# Test

- `./tests/`配下に記述

# 開発手順

- GitHub flowなど
- CIでmainを自動でデプロイする

