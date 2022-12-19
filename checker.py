import requests
import argparse
from dateutil import parser
import re

TOKEN = "REPLACE_THIS"
INACTIVE_THRESHOLD = 2018


def read_usernames(file):
    try:
        usernames = set([l.strip() for l in open(file).readlines()])
    except FileNotFoundError:
        print(f"Error: No such file '{file}'")
        exit(1)

    # Remove invalid usernames
    pattern = "^[A-Za-z0-9_]{5,15}$"
    valid_usernames = []
    for username in usernames:
        if re.match(pattern, username):
            valid_usernames.append(username)
        else:
            print(f"\033[1;31mINVALID\033[0m\t\t{username}")
    return valid_usernames


def search_users(usernames):
    available_users = []
    username_chunks = [usernames[i : i + 100] for i in range(0, len(usernames), 100)]
    for username_chunk in username_chunks:
        response = requests.get(
            url="https://api.twitter.com/2/users/by",
            headers={
                "Authorization": f"Bearer {TOKEN}",
            },
            params={
                "usernames": ",".join(username_chunk),
                "user.fields": "id,created_at,name,username,verified,pinned_tweet_id",
                "tweet.fields": "created_at",
            },
        )

        data = response.json()

        if response.status_code != 200:
            print(f"Error: {data['detail']}")
            exit()

        if "errors" in data:
            for error in data["errors"]:
                assert "resource_id" in error
                username = error["resource_id"]
                if "suspended" in error["detail"]:
                    print(f"\033[1;31mSUSPENDED\033[0m\t{username}")
                elif "Could not find user" in error["detail"]:
                    available_users.append(username)
                else:
                    print(error)

        if "data" in data:
            for user in data["data"]:
                username = user["username"]

                user_created = parser.parse(user["created_at"].split("T")[0])
                threshold = parser.parse(f"{INACTIVE_THRESHOLD}-01-01")

                if (
                    user_created > threshold
                    or "pinned_tweet_id" in user
                    or user["verified"]
                ):
                    print(f"\033[1;31mACTIVE\033[0m\t\t{username}")
                    continue

                response = requests.get(
                    f"https://api.twitter.com/2/users/{user['id']}/tweets",
                    params={"tweet.fields": "created_at"},
                    headers={"Authorization": f"Bearer {TOKEN}"},
                )

                tweet_data = response.json()

                if response.status_code != 200:
                    print(f"Error: {tweet_data['detail']}")
                    exit()

                if "meta" not in tweet_data:
                    print(f"\033[1;31mPRIVATE\033[0m\t\t{username}")
                    continue

                if tweet_data["meta"]["result_count"] > 0:
                    print(f"\033[1;31mACTIVE\033[0m\t\t{username}")
                else:
                    print(f"\033[1;33mINACTIVE\033[0m\t{username}")
    return available_users


def check_usernames(usernames):
    for username in usernames:
        response = requests.get(
            f"https://twitter.com/i/api/i/users/username_available.json?username={username}",
            headers={
                "authorization": f"Bearer {TOKEN}",
                "x-guest-token": "1337",
                "x-twitter-active-user": "yes",
                "x-twitter-client-language": "en",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
            },
        )
        data = response.json()
        if response.status_code != 200:
            print(f"Error: {data['detail']}")
            exit()
        print(
            f"\033[1;{'32' if data['valid'] else '31'}m{data['reason'].upper()}\033[0m\t{username}"
        )


# Read usernames
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "username_file",
        help="Name of a text file that contains a list of usernames",
    )
    args = arg_parser.parse_args()
    usernames = read_usernames(args.username_file)

    available_users = search_users(usernames)
    check_usernames = check_usernames(available_users)
