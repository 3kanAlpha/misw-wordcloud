import json
import subprocess
import os
import datetime
import arrow

from subprocess import PIPE

import stweet as st

from dotenv import load_dotenv

load_dotenv('.env')

USER_IDS_PATH = "user_ids.json"

TWEETS_DIR = "tweets/"
DATE_SINCE = datetime.datetime(2021, 1, 1)
DATE_SINCE_ARR = arrow.get(DATE_SINCE)

def try_search(user):
    search_tweets_task = st.SearchTweetsTask(from_username=user["name"], since=DATE_SINCE_ARR, tweets_limit=10000)
    output_jl_tweets = st.JsonLineFileRawOutput(TWEETS_DIR + user["name"] + '_tweets.jsonl')
    output_jl_users = st.JsonLineFileRawOutput(TWEETS_DIR + user["name"] + '_users.jsonl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_jl_tweets],
                         user_raw_data_outputs=[output_jl_users]).run()

def try_user_scrap(user):
    user_task = st.GetUsersTask([user["name"]])
    output_json = st.JsonLineFileRawOutput('output_raw_user.jsonl')
    output_print = st.PrintRawOutput()
    st.GetUsersRunner(get_user_task=user_task, raw_data_outputs=[output_print, output_json]).run()

def main():
    user_ids_json = open(USER_IDS_PATH, 'r', encoding="utf-8")
    user_ids = json.load(user_ids_json)
    user_ids_json.close()

    for user in user_ids["ids"]:
        if user["protected"]:
            continue

        # try_search(user)
        break

if __name__ == "__main__":
    main()