import json
import os
import myloaddata
import pandas as pd

def main():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.abspath(os.path.join(cur_dir, "data"))

    mojo_data = myloaddata.load_data(os.path.join(data_dir, "boxofficemojo"))
    metacritic_data = myloaddata.load_data(os.path.join(data_dir, "metacritic"))

    # filter empty data
    metacritic_data = [d for d in metacritic_data if len(d) == 15]

    mojo_df = pd.DataFrame(mojo_data)
    metacritic_df = pd.DataFrame(metacritic_data)

    combined_df = pd.merge(mojo_df, metacritic_df, how="inner", on="title")
    print combined_df.head(3)
    combined_df.to_csv("combined_movie_data.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
