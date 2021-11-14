import os
import re
import pickle
from random import choice

try:
    from debugDB import *
except ImportError:
    from db import *


def find_twitter_username(text):
    return re.findall(r'@[a-zA-Z0-9_]{1,15}', text)


def lower_list(original_list: list):
    return [x.lower() for x in original_list]


def remove_leading_at(original_list: list):
    return [x[1:] for x in original_list]


if __name__ == '__main__':
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
    with open(os.path.join(data_path, info_file), 'rb') as f:
        data = pickle.load(f)

    relation_map = {}
    user_index = {}
    nodes_html = ''
    edges_html = ''

    # Generate a dict, key is the lowercase of username, value is a list of mentioned username
    for user in data:
        raw_users = find_twitter_username(data[user].description)
        lower_users = lower_list(raw_users)
        users = list(set(remove_leading_at(lower_users)))
        relation_map[data[user].screen_name.lower()] = users.copy()

    # Slim the dict, remove single-mentioned relationship
    # Removes: self-mentioning (A -> A), one-step-mentioning (A -> B)
    # Keeps: mention-mentioning (A -> B -> A), two-step-mentioning (A -> B -> C) and more

    mentioning = []
    mentioned = []

    # First find all the users that are mentioned
    for user in relation_map:
        for target in relation_map[user]:
            mentioning.append(user)
            mentioned.append(target)
    # Do not remove duplicates

    map_copy = relation_map.copy()
    for user in map_copy:
        if len(map_copy[user]) == 0:  # Does not mention anyone in bio
            del relation_map[user]
        elif len(map_copy[user]) == 1:  # Only mentions one person
            target = map_copy[user][0]
            if user == target:  # Self-mentioning
                mentioned_times = mentioned.count(target)
                if mentioned_times < 2:
                    del relation_map[user]
            else:
                if target not in mentioning:  # Else: chain
                    mentioned_times = mentioned.count(target)
                    if mentioned_times < 2:
                        del relation_map[user]
    del map_copy

    # Generate a dict, key is the lowercase of username, value is the index of the node
    index = 1
    for user in relation_map:
        if user not in user_index:
            user_index[user] = index
            index += 1
        for target in relation_map[user]:
            if target not in user_index:
                user_index[target] = index
                index += 1

    # Generate the nodes and edges
    for user in user_index:
        label = f'@{user}'
        for i in data:
            if user == data[i].screen_name.lower():
                label = data[i].name
                break
        nodes_html += f'{blank_space}{{id: {user_index[user]}, ' \
                      f'label: \'{label}\', ' \
                      f'url: \'https://twitter.com/{user}\', ' \
                      f'color: \'{choice(colors)}\'}},\n'

    for user in relation_map:
        for target in relation_map[user]:
            edges_html += f'{blank_space}{{from: {user_index[user]}, to: {user_index[target]}}},\n'

    html_code = html_code.replace('TITLE_PLACEHOLDER', 'KumaTea Friends Map ' + datetime.now().strftime('%m/%d'))
    html_code = html_code.replace('NODES_PLACEHOLDER', nodes_html)
    html_code = html_code.replace('EDGES_PLACEHOLDER', edges_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_code)
