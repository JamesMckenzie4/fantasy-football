import os

import pandas as pd
from unidecode import unidecode

from config import db_config
from query_database import QueryDatabase

DATA_PATH = "/home/james/Fantasy-Premier-League/data"
QUERY_PATH = "../sql/insert_vaastav.sql"
COLS = [
    "round",
    "kickoff_time",
    "name",
    "element",
    "value",
    "minutes",
    "total_points",
    "bonus",
    "bps",
    "goals_scored",
    "assists",
    "penalties_missed",
    "red_cards",
    "yellow_cards",
    "goals_conceded",
    "own_goals",
    "saves",
    "penalties_saved",
    "creativity",
    "influence",
    "threat",
    "ict_index",
    "transfers_in",
    "transfers_out",
    "transfers_balance",
    "selected",
    "fixture",
    "team_h_score",
    "team_a_score",
    "was_home",
    "opponent_team",
]


def remove_accents(a):
    return unidecode(a)


def parse_vaastav():
    """Parse vaastav data directory and populate database"""
    data = []
    query_db = QueryDatabase(db_config)
    for year in sorted(os.listdir(DATA_PATH), reverse=True):
        for game_week in os.listdir(os.path.join(DATA_PATH, year, "gws")):
            if not game_week.endswith("cleaned.csv"):
                continue
            print(
                "Processing file - {}".format(
                    os.path.join(DATA_PATH, year, "gws", game_week)
                )
            )
            df = pd.read_csv(
                os.path.join(DATA_PATH, year, "gws", game_week), encoding="utf8"
            )
            df.dropna(inplace=True)
            # Remove accents from players names
            df["name"] = df.apply(lambda x: remove_accents(x["name"]), axis=1)
            # Remove player_id / element from the end players name
            if year in ["2018-19", "2019-20"]:
                df["name"] = df.name.str.split("_").str[:-1].str.join(" ")
            game_week_data = list(df[COLS].itertuples(index=False, name=None))
            data.extend(game_week_data)

    query_db.db_insert(QUERY_PATH, data)


if __name__ == "__main__":
    parse_vaastav()
