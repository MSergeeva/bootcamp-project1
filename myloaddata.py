"""bootcamp eda challenge"""

import os
import json

# constants
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
MOJO_DIR = os.path.join(DATA_DIR, 'boxofficemojo')

def load_data(dir_name=MOJO_DIR):
    movie_dict = []
    for file_name in os.listdir(dir_name):
        with open(os.path.join(dir_name, file_name), "r") as f:
            data = json.load(f)
            movie_dict.append(data)
    return movie_dict

if __name__ == "__main__":
    load_data(MOJO_DIR)
