import os

from config import db_config
from query_database import QueryDatabase


DATA_PATH = "../../data/positions"
INSERT_QUERY = "../sql/insert_positions.sql"


def insert_positions():
    insert_data = []
    for year in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, year)) as open_file:
            for line in open_file:
                insert_data.append(tuple(line.split(",")))

    query_db = QueryDatabase(db_config)
    query_db.db_insert(INSERT_QUERY, insert_data)


if __name__ == "__main__":
    insert_positions()
