import os
import pickle
from map import *
from toolsAPI import *


if __name__ == '__main__':
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
    with open(os.path.join(data_path, info_file), 'rb') as f:
        data = pickle.load(f)

    extended_data = get_extended_users_data(*get_extended_users(data))

    try:  # Python 3.9 and newer
        combined_data = data | extended_data
    except:
        combined_data = {**data, **extended_data}
        # combined_data = extended_data.update(data)

    # Generate a dict, key is the lowercase of username, value is a list of mentioned username
    relation_map = generate_map(combined_data)

    # Slim the map
    relation_map = slim_map(relation_map)

    # Index the users
    user_index = index_user(relation_map)

    # Generate the html code
    new_html_code = generate_content(relation_map, user_index, data, html_code)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html_code)
