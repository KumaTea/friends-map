import json
from tools import *
from random import choice

try:
    from debugDB import *
except ImportError:
    from db import *


def generate_map(u_data: dict):
    # Generate a dict, key is the lowercase of username, value is a list of mentioned username
    new_map = {}
    for u in u_data:
        raw_users = find_twitter_username(u_data[u].description)
        lower_users = lower_list(raw_users)
        users = list(set(remove_leading_at(lower_users)))
        new_map[u_data[u].screen_name.lower()] = users.copy()
    return new_map


def slim_map(map_to_slim: dict):
    # Slim the dict, remove single-mentioned relationship
    # Removes: self-mentioning (A -> A), one-step-mentioning (A -> B)
    # Keeps: mention-mentioning (A -> B -> A), two-step-mentioning (A -> B -> C) and more

    mentioning = []
    mentioned = []

    # First find all the users that are mentioned
    for u in map_to_slim:
        for t in map_to_slim[u]:
            mentioning.append(u)
            mentioned.append(t)
    # Do not remove duplicates

    map_copy = map_to_slim.copy()
    for u in map_copy:
        if len(map_copy[u]) == 0:  # Does not mention anyone in bio
            del map_to_slim[u]
        elif len(map_copy[u]) == 1:  # Only mentions one person
            t = map_copy[u][0]
            if u == t:  # Self-mentioning
                mentioned_times = mentioned.count(t)
                if mentioned_times < 2:
                    del map_to_slim[u]
            else:
                if t not in mentioning:  # Else: chain
                    mentioned_times = mentioned.count(t)
                    if mentioned_times < 2:
                        del map_to_slim[u]
    del map_copy
    return map_to_slim


def generate_content(relation, u_index, u_data, h_code):
    # Generate the nodes and edges
    n_html = ''
    e_html = ''
    u_index_list = list(u_index.keys())
    for u in u_index:
        label = f'\'@\' + users[{u_index_list.index(u)}]'
        for i in u_data:
            if u == u_data[i].screen_name.lower():
                # label = json.dumps(u_data[i].name)
                label = f'\'{u_data[i].name}\'' if '\'' not in u_data[i].name else f'\"{u_data[i].name}\"'
                break
        n_html += f'{blank_space}{{id: {u_index[u]}, ' \
                  f'label: {label}, ' \
                  f'url: twi + users[{u_index_list.index(u)}], ' \
                  f'color: colors[{colors.index(choice(colors))}]}},\n'

    for u in relation:
        for target in relation[u]:
            e_html += f'{blank_space}{{from: {u_index[u]}, to: {u_index[target]}}},\n'

    h_code = h_code.replace('TITLE_PLACEHOLDER', 'KumaTea Friends Map ' + datetime.now().strftime('%m/%d'))
    h_code = h_code.replace('USERS_PLACEHOLDER', f'const users = {json.dumps(u_index_list)};')
    h_code = h_code.replace('NODES_PLACEHOLDER', n_html)
    h_code = h_code.replace('EDGES_PLACEHOLDER', e_html)

    return h_code


def index_user(r_map: dict):
    u_index = {}
    # Generate a dict, key is the lowercase of username, value is the index of the node
    index = 1
    for u in r_map:
        if u not in u_index:
            u_index[u] = index
            index += 1
        for t in r_map[u]:
            if t not in u_index:
                u_index[t] = index
                index += 1
    return u_index
