from tools import *
from tqdm import tqdm
from session import kuma


def get_extended_users(data: dict):
    friend_ids = kuma.get_friend_ids()
    follower_ids = kuma.get_follower_ids()
    one_way_user_ids = list(set(follower_ids) - set(friend_ids))

    mentioned_users = []
    for u in data:
        raw_users = find_twitter_username(data[u].description)
        lower_users = lower_list(raw_users)
        users = list(set(remove_leading_at(lower_users)))
        mentioned_users.extend(users)
    mentioned_users = list(set(mentioned_users))
    return mentioned_users, one_way_user_ids


def get_extended_users_data(user_names: list, user_ids: list):
    # Get the data of users
    user_data = {}
    print('Getting user data (1/2)')
    for u in tqdm(user_names):
        user = kuma.get_user(screen_name=u)
        user_data[user.id] = user
    print('Getting user data (2/2)')
    for u in tqdm(user_ids):
        user_data[u] = kuma.get_user(user_id=u)
    return user_data
