from bs4 import BeautifulSoup
import io
import pandas as pd
from pandas.errors import EmptyDataError, ParserError
import requests


from config import db_config
from query_database import QueryDatabase

URL = "https://fantasyoverlord.com/FPL/History"
SQL_DIR = "../../"
COLUMNS = [
    "game_week",
    "FirstName",
    "Surname",
    "PositionsList",
    "Team",
    "Cost",
    "PointsLastRound",
    "TotalPoints",
    "AveragePoints",
    "AveragePointsPerDollar",
    "TotalPointsPerDollar",
    "GameweekWeighting",
    "TransfersOut",
    "YellowCards",
    "GoalsConceded",
    "GoalsConcededPoints",
    "Saves",
    "SavesPoints",
    "GoalsScored",
    "GoalsScoredPoints",
    "ValueSeason",
    "TransfersOutRound",
    "PriceRise",
    "PriceFallRound",
    "LastSeasonPoints",
    "PriceFall",
    "ValueForm",
    "PenaltiesMissed",
    "Form",
    "Bonus",
    "FanRating",
    "CleanSheets",
    "CleanSheetPoints",
    "Assists",
    "SelectedByPercent",
    "TransfersIn",
    "OwnGoals",
    "EAIndex",
    "PenaltiesSaved",
    "DreamteamCount",
    "MinutesPlayed",
    "TransfersInRound",
    "PriceRiseRound",
    "RedCards",
    "BPS",
    "NextFixture1",
    "NextFixture2",
    "NextFixture3",
    "NextFixture4",
    "NextFixture5",
]


def scrape_fantasy_overlord(to_exclude=None):
    """Scrape fantasyoverlord.com for historic weekly player points returns.

    Parameters
    ----------
    to_exclude : list
    optional list of games weeks to exclude from scraping

    Returns
    -------
    list
    A list of csv file rows
    """

    data = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    url_start = URL.replace("/FPL/History", "")
    for link in soup.findAll("a"):
        if "file" in link["href"]:
            # Get game week id from file name
            file_id = link["href"].replace("/FPL/History?file=", ",").replace(",", "")
            if to_exclude and file_id in to_exclude:
                continue
            print("Processing game week - {}".format(file_id))
            r = requests.get(url_start + link["href"]).content
            try:
                df = pd.read_csv(io.StringIO(r.decode("utf-8")))
            except (EmptyDataError, ParserError):
                continue
            df["game_week"] = file_id
            game_week_data = list(df[COLUMNS].itertuples(index=False, name=None))
            data.extend(game_week_data)

    return data


def insert_into_db(data, sql_file_path="../sql/insert_fantasy_lord.sql"):
    print("Shipping data to db")
    query_db = QueryDatabase(db_config)
    query_db.db_insert(sql_file_path, data)


def main():
    data = scrape_fantasy_overlord()
    insert_into_db(data)


if __name__ == "__main__":
    main()
