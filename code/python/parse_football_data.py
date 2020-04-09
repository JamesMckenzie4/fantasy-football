import pandas as pd
import os

from query_database import QueryDatabase
from config import db_config


PATH = "../../data/football_data_co_uk.csv"
QUERY_PATH = "../sql/insert_football_data.sql"
COLS = [
    "Div",
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "HTHG",
    "HTAG",
    "FTR",
    "Referee",
    "HS",
    "AS",
    "HST",
    "AST",
    "HC",
    "AC",
    "HF",
    "AF",
    "HY",
    "AY",
    "HR",
    "AR",
    "PSH",
    "PSA",
    "PSD",
]


def ship_football_data_to_db():
    """Parse footbal-data.co.uk data and ship to local db"""
    data = []
    query_db = QueryDatabase(db_config)
    for year in os.listdir(PATH):
        print(PATH, year)
        df = pd.read_csv(os.path.join(PATH, year))
        df_data = list(df[COLS].itertuples(index=False, name=None))
        data.extend(df_data)

    query_db.db_insert(QUERY_PATH, data)


if __name__ == "__main__":
    ship_football_data_to_db()
