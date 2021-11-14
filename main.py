import os
import re
import pickle
from db import *
from random import choice


def get_twitter_username(text):
    return re.findall(r'@[a-zA-Z0-9_]{1,15}', text)


if __name__ == '__main__':
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
    with open(os.path.join(data_path, info_file), 'rb') as f:
        data = pickle.load(f)

    relation_map = {}
    user_index = {}
    nodes_html = ''
    edges_html = ''

    for user in data:
        lower_user = []
        users = []
        raw_users = get_twitter_username(data[user].description)
        for i in raw_users:
            if not i.lower() in lower_user:
                users.append(i)
                lower_user.append(i.lower())
        relation_map[data[user].screen_name] = users.copy()

    index = 1
    for user in relation_map:
        for target in relation_map[user]:
            if (u := f'@{user}'.lower()) not in user_index:
                user_index[u] = index
                index += 1
            if (t := target.lower()) not in user_index:
                user_index[t] = index
                index += 1

    for user in user_index:
        nodes_html += f'{blank_space}{{id: {user_index[user]}, ' \
                      f'label: \'{user}\', ' \
                      f'url: \'https://twitter.com/{user[1:]}\', ' \
                      f'color: \'{choice(colors)}\'}},\n'

    for user in relation_map:
        for target in relation_map[user]:
            u = f'@{user}'.lower()
            t = target.lower()
            edges_html += f'{blank_space}{{from: {user_index[u]}, to: {user_index[t]}}},\n'

    html_code = html_code.replace('TITLE_PLACEHOLDER', 'KumaTea Friends Map ' + datetime.now().strftime('%m/%d'))
    html_code = html_code.replace('NODES_PLACEHOLDER', nodes_html)
    html_code = html_code.replace('EDGES_PLACEHOLDER', edges_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_code)
