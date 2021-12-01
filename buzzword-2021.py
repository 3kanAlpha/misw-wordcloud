import os
import numpy as np

import MeCab
from wordcloud import WordCloud
import re

import json
import time
import collections

from dotenv import load_dotenv

load_dotenv('.env')

# SourceHanSans
FONT_PATH = os.environ.get("FONT_PATH")

TWEETS_DIR = "tweets/"
TWEETS_JSON_PATH = TWEETS_DIR + "tweets.json"

USER_IDS_PATH = "user_ids.json"

WORDCLOUD_TITLE = "misw-buzzword"

def generate_wordcloud(text):
    wc = WordCloud(background_color="white", font_path=FONT_PATH, max_words=1000, max_font_size=300, width=800, height=600)
    wc.generate(text)

    wc.to_file("{}.png".format(WORDCLOUD_TITLE))

def list_to_string(l):
    return ' '.join(l)

def get_words_from_text(text):
    mecab = MeCab.Tagger("-d D:\Documents\MeCabDic")
    text_dst = mecab.parse(text)

    lines = text_dst.split('\n')
    lines = lines[0:-2]

    words = []

    for line in lines:
        # tabかカンマでsplitする
        col = re.split('\t|,', line)
        
        if col[1] in ["形容詞", "動詞","名詞", "副詞"]:
            words.append(col[0])
    
    return words

# 本質的でない単語を除く
def remove_words(list):
    for s in list:
        if s.startswith("https://") or s.startswith("http://"):
            list.remove(s)
        
        if s == "前日比":
            list.remove(s)
        elif s == "https":
            list.remove(s)
        elif s == "t":
            list.remove(s)
        elif s == "co":
            list.remove(s)
        elif s == "t":
            list.remove(s)
        elif s == "ー":
            list.remove(s)
        elif s == "てる":
            list.remove(s)
        elif s == "自分":
            list.remove(s)
        elif s == "て":
            list.remove(s)
        elif s == "の":
            list.remove(s)
        elif s == "それ":
            list.remove(s)
        elif s == "気":
            list.remove(s)
        elif s == "ん":
            list.remove(s)

def remove_words_by_counter(list, counter):
    max_val = 330

    for s in list:
        if counter[s] > max_val:
            list.remove(s)

def print_counter(counter):
    threshold = 80

    for x in counter:
        if counter[x] > threshold:
            print("{}: {}".format(x, counter[x]))

def main():
    user_ids_json = open(USER_IDS_PATH, 'r', encoding="utf-8")
    user_ids = json.load(user_ids_json)
    user_ids_json.close()

    tweets_json = open(TWEETS_JSON_PATH, 'r', encoding="utf-8")
    tweets = json.load(tweets_json)
    tweets_json.close()

    all_tweets = tweets["tweets"]

    words_to_wc = []

    start_time = time.perf_counter()

    for user in user_ids["ids"]:
        if user["name"] in all_tweets:
            print("Loading {}'s tweets ... ({})".format(user["name"], len(all_tweets[user["name"]])))
            for tweet in all_tweets[user["name"]]:
                words_to_wc.extend(get_words_from_text(tweet["tweet"]))

    # time_1 = time.perf_counter()

    print("Removing unrelated words ...")
    remove_words(words_to_wc)

    counter = collections.Counter(words_to_wc)
    remove_words_by_counter(words_to_wc, counter)

    # time_2 = time.perf_counter()

    print("Words to string ...")
    words_str = list_to_string(words_to_wc)

    # time_3 = time.perf_counter()

    print("Generating wordcoud ...")
    generate_wordcloud(words_str)

    time_end = time.perf_counter()

    print("Done! ({} [sec])".format(time_end - start_time))

if __name__ == '__main__':
    main()