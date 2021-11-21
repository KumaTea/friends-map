import re


def find_twitter_username(text):
    return re.findall(r'@[a-zA-Z0-9_]{1,15}', text)


def lower_list(original_list: list):
    return [x.lower() for x in original_list]


def remove_leading_at(original_list: list):
    return [x[1:] for x in original_list]
