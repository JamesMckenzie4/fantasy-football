import os
import pandas as pd


DATA_DIR = "/home/james/Fantasy-Premier-League/data"
POSITION_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
COLS = ["first_name", "second_name", "element_type"]


def get_positions():
    for file in os.listdir(DATA_DIR):
        df = pd.read_csv(os.path.join(DATA_DIR, file, "players_raw.csv"))
        df = df[COLS]
        print(df.head())


if __name__ == "__main__":
    get_positions()
