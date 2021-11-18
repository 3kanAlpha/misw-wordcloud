import os
import numpy as np

import MeCab
from wordcloud import WordCloud
import re

FONT_PATH = r"C:/Users/あるふぁ/AppData/Local/Microsoft/Windows/Fonts/SourceHanSans-Regular.otf"
TEXT_NAME = "rashomon"

def generate_wordcloud(text):
    wc = WordCloud(background_color="white", font_path=FONT_PATH, max_words=1000, max_font_size=300, width=800, height=600)
    wc.generate(text)

    wc.to_file("{}.png".format(TEXT_NAME))

def list_to_string(l):
    return ' '.join(l)

def get_words_from_text(text):
    mecab = MeCab.Tagger("-d D:\Documents\MeCabDic")
    text_dst = mecab.parse(text)

    lines = text_dst.split('\n')
    lines = lines[0:-2]

    words = []

    for line in lines:
        col = re.split('\t|,', line)
        
        if col[1] in ["形容詞", "動詞","名詞", "副詞"]:
            words.append(col[0])
    
    return words

def main():
    txt = open("127_ruby_150/{}.txt".format(TEXT_NAME), encoding="utf8").read()
    words = get_words_from_text(txt)
    words_str = list_to_string(words)
    generate_wordcloud(words_str)

if __name__ == '__main__':
    main()