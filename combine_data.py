import json
import os
import myloaddata
import datetime
import pandas as pd
import numpy as np

def parse_genres(s):
    if isinstance(s, list):
        return s
    genres = s.replace("[", "")
    genres = genres.replace("]", "")
    return genres.split(", ")

def add_genre_dummy(lst, genre):
    return 1 if genre in lst else 0

def get_all_genres(df):
    all_genres = set()
    for genres in df["genres_list"]:
        all_genres |= set(genres)
    return list(all_genres)

def add_columns_for_genres(all_genres, df):
    for genre in all_genres:
        df[genre] = 0
    for genre in all_genres:
        df[genre] = df["genres_list"].apply(lambda lst: add_genre_dummy(lst, genre))

def main():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.abspath(os.path.join(cur_dir, "data"))

    mojo_data = myloaddata.load_data(os.path.join(data_dir, "boxofficemojo"))
    metacritic_data = myloaddata.load_data(os.path.join(data_dir, "metacritic"))

    # filter empty data
    metacritic_data = [d for d in metacritic_data if len(d) == 15]

    mojo_df = pd.DataFrame(mojo_data)
    metacritic_df = pd.DataFrame(metacritic_data)

    combined_df = pd.merge(mojo_df, metacritic_df, how="inner", on=["title", "year", "director"])
    combined_df["month"] = combined_df["release_date_wide"].apply(lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').strftime("%b") if s is not None else None)
    combined_df["release_date_wide"] = pd.to_datetime(combined_df["release_date_wide"], format='%Y-%m-%d')
    combined_df["weekday"] = combined_df["release_date_wide"].dt.weekday_name
#    combined_df["month"] = combined_df["release_date_wide"].dt.month
    combined_df["year_release"] = combined_df["release_date_wide"].dt.year
    combined_df["log_domestic_gross"] = combined_df["domestic_gross"].apply(np.log)
    combined_df["log_opening_weekend_take"] = combined_df["opening_weekend_take"].apply(np.log)

    print combined_df["genre"].head(3)
    print type(combined_df["genre"][0])
    combined_df["genres_list"] = combined_df["genre"].apply(parse_genres)
    combined_df["number_of_genres"] = combined_df["genres_list"].apply(lambda x: len(x))
    all_genres = get_all_genres(combined_df)

    add_columns_for_genres(all_genres, combined_df)

    print combined_df.head(3)
    combined_df.to_csv("data/combined_movie_data.csv", encoding="utf-8")



if __name__ == "__main__":
    main()
