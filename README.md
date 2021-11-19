# みす流行語大賞2021
PythonでWordCloud作ってみる

# Requirements
* Python 3.8.x or later
* MeCab + [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)
* [wordcloud](https://github.com/amueller/word_cloud)

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
