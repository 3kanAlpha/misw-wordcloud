import os
import json
import jsonlines
import glob

TWEETS_DIR = "tweets\\"
TWEETS_JSON_PATH = TWEETS_DIR + "tweets.json"
USER_IDS_PATH = "user_ids.json"

def find_tweet(old_tweets, screen_name, tweet_id):
    all_tweets = old_tweets.get("tweets")
    if all_tweets is None:
        return False

    user_tweets = all_tweets.get(screen_name)
    if user_tweets is None:
        return False

    fl = False

    for tweet in user_tweets:
        if tweet["id"] == tweet_id:
            fl = True
            break

    return fl

def combine_user_tweets(old_tweets, screen_name):
    dir_path = TWEETS_DIR + screen_name + "\\"
    files = glob.glob(dir_path + "*.jsonl")
    
    tweets = []

    for file in files:
        with jsonlines.open(file) as reader:
            for tweet in reader:
                if not find_tweet(old_tweets, screen_name, tweet["id"]):
                    tweets.append(tweet)

    return tweets

def main():
    user_ids_json = open(USER_IDS_PATH, 'r', encoding="utf-8")
    user_ids = json.load(user_ids_json)
    user_ids_json.close()

    tweets_json = open(TWEETS_JSON_PATH, 'r', encoding="utf-8")
    tweets = json.load(tweets_json)
    tweets_json.close()

    for user in user_ids["ids"]:
        if os.path.isdir(TWEETS_DIR + user["name"]):
            user_tweets = combine_user_tweets(tweets, user["name"])
            tweets["tweets"][user["name"]] = user_tweets

            print("{}'s tweets combined successfully.".format(user["name"]))
    
    with open(TWEETS_JSON_PATH, 'w', encoding="utf-8") as outfile:
        json.dump(tweets, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()