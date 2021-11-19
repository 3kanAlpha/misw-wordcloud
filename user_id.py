import requests
import os
import json

from dotenv import load_dotenv

load_dotenv('.env')

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

USER_IDS_PATH = "user_ids.json"

def create_url(user_name):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=" + user_name
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def try_to_insert(user_ids, user_id):
    fl = True

    for user in user_ids["ids"]:
        if user["id"] == user_id:
            fl = False
            break

    return fl

def main():
    user_names = input().split(",")

    user_ids_json = open(USER_IDS_PATH, 'r', encoding="utf-8")
    user_ids = json.load(user_ids_json)
    user_ids_json.close()

    new_user_ids = []

    for user_name in user_names:
        url = create_url(user_name)
        json_response = connect_to_endpoint(url)

        print("{}'s user ID: {}".format(user_name, json_response["data"][0]["id"]))

        if try_to_insert(user_ids, json_response["data"][0]["id"]) is True:
            new_user_ids.append({"id": json_response["data"][0]["id"], "name": user_name})
    
    if len(new_user_ids) > 0:
        for new_user_id in new_user_ids:
            user_ids["ids"].append(new_user_id)
        
        with open(USER_IDS_PATH, 'w', encoding="utf-8") as f:
            json.dump(user_ids, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()