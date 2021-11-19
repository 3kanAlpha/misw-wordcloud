# みす流行語大賞2021
PythonでWordCloud作ってみる

# Docs
## buzzword-2021.py
このアプリの本体。与えられたテキストを形態素解析してWordCloudを生成する。  
WordCloudには名詞、動詞、形容詞、副詞を利用している。  
(Progress: 90%)

## user_id.py
ユーザー名（Twitterで@の後ろに付いている文字列）から固有のユーザーIDを取得する。  
(Progress: 100%)

## tweet_collector.py
上で取得したユーザーIDを利用して、特定のユーザーのツイート（リツイート、リプライなど含む）を取得する。  
(WIP)

## user_ids.json
ユーザー名とユーザーIDの対応表。  
自分のアカウント(@luigi_0829_2)をフォローしてくれている人から適当に選んでいる。