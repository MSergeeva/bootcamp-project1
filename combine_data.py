import json
import os
import myloaddata
import datetime
import pandas as pd
import numpy as np

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
    print combined_df.head(3)
    combined_df.to_csv("data/combined_movie_data.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
