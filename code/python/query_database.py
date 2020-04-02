import psycopg2
from psycopg2 import ProgrammingError


class QueryDatabase:
    """A class to support database queries. Pass a config dictionary containing database login
    details. """

    def __init__(self, config):
        self.config = config
        self.conn = self.db_connect()
        self.cur = self.get_cursor()
        self.query = None
        self.query_results = None

    def db_connect(self):
        config = self.config
        connection_string = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(
            config["dbname"],
            config["user"],
            config["host"],
            config["password"],
            config["port"],
        )

        conn = psycopg2.connect(connection_string)
        return conn

    def get_cursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            print("No connection object detected")

    def build_query_from_file(self, query_file, *args):
        """Build a query from an sql file containing python string formaters and arguments to populate them."""
        with open(query_file) as open_file:
            query = open_file.read()
            self.query = query.format(*args)

    def set_query(self, query):
        self.query = query

    def close_connection(self):
        self.conn.close()

    def execute_query(self, close_after_execution=False):
        if self.query:
            cur = self.get_cursor()
            cur.execute(self.query)
            data = cur.fetchall()
            self.query_results = data
            if close_after_execution:
                self.close_connection()
        else:
            print("No query specified - database connection still live")
            return

    def db_insert(self, query, insert_data, close_after_execution=False):
        with open(query) as query_file:
            query_file = query_file.read()

        # Convert insert data into massive string
        template = ",".join(["%s"] * len(insert_data))
        insert_query = query_file.format(template)
        # Insert logs into db
        try:
            self.cur.execute(insert_query, insert_data)
            self.conn.commit()
        except ProgrammingError as e:
            print(e)

        if close_after_execution:
            self.close_connection()
