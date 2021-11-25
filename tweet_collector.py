import json
import os
from datetime import datetime, timedelta
import time

import twint

from dotenv import load_dotenv

load_dotenv('.env')

USER_IDS_PATH = "user_ids.json"

TWEETS_DIR = "tweets/"
DATE_SINCE = datetime(2021, 1, 1)

def make_user_dir(user_name):
    try:
        os.makedirs(TWEETS_DIR + user_name)
    except FileExistsError:
        pass

# sinceからuntilまでのツイートを取得してJSONに保存
def get_tweets(user_name, since, until):
    c = twint.Config()

    c.Username = user_name
    c.Store_object = True
    c.Hide_output = True
    c.Store_json = True
    c.Output = TWEETS_DIR + user_name + "/" + since + "_to_" + until + ".jsonl"
    c.Since = since
    c.Until = until
    c.Limit = 1000

    twint.run.Search(c)

# 今年のツイートを取得（できるはずだった）
def get_tweets_this_year(user_name, delta=1):
    make_user_dir(user_name)
    start_date = DATE_SINCE
    now = datetime.now()

    day_delta = timedelta(days=delta)

    while start_date < now:
        get_tweets(user_name, start_date.strftime("%Y-%m-%d"), (start_date + day_delta).strftime("%Y-%m-%d"))
        start_date += day_delta
        time.sleep(1)

def main():
    user_ids_json = open(USER_IDS_PATH, 'r', encoding="utf-8")
    user_ids = json.load(user_ids_json)
    user_ids_json.close()

    left = 0

    for user in user_ids["ids"]:
        if left > 0:
            left -= 1
            continue

        if user["protected"]:
            continue

        get_tweets_this_year(user["name"], delta=3)
        print("Progress {}/{} ...".format(user_ids["ids"].index(user)+1, len(user_ids["ids"])))
        time.sleep(15)
    
    print("Done!")

if __name__ == "__main__":
    main()