# みす流行語大賞2021
PythonでWordCloud作ってみる

# Requirements
* Python 3.8.x or later
* MeCab + [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)
* [wordcloud](https://github.com/amueller/word_cloud)
* twint

# Docs
## buzzword-2021.py
このアプリの本体。与えられたテキストを形態素解析してWordCloudを生成する。  
WordCloudには名詞、動詞、形容詞、副詞を利用している。  
(Progress: 90%)

## user_id.py (Unused)
ユーザー名（Twitterで@の後ろに付いている文字列）から固有のユーザーIDを取得する。  
(Progress: 100%)

## tweet_collector.py
twintを利用して、特定のユーザーのツイート（リツイート、リプライなど含む）を取得する。  
取得したツイートはJSON Lines形式で保存される。

## database_builder.py
tweet_collector.pyで取得したツイートを整形してJSONに構成し直す。