"""@package DB
This module manages access to the sqllite databases, these provide better performance than CSV files.

More details.
"""

import sqlite3
from datetime import datetime, timezone

import requests
import csv

class DB:
    def __init__(self):
        self.conn_lexicon = sqlite3.connect('db/lexicon.db')
        self.conn_data = sqlite3.connect('db/train_data.db')
        self.token = None
        self.expires = None

    def refresh_token(self):
        response = requests.post('https://api.hatebase.org/4-4/authenticate',
                                 dict(api_key='sQmKeVgLQwrWJmyNvCUaziuDbsEVypnt'))
        self.token = response.json()["result"]["token"]
        self.expires = datetime.strptime(response.json()["result"]["expires_on"], '%Y-%m-%d %H:%M:%S')
        self.expires = self.expires.replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(self.expires)

    def expired(self):
        return datetime.now(tz=None) >= self.expires

    @staticmethod
    def insert_term(i, cursor):
        cursor.execute('insert or ignore into lexicon values (?,?)', (i["term"],
                                                                                                    i["average_offensiveness"]))

    def create_lexicon_db(self):
        sql_file = open("./db/create_lexicon_db.sql")
        sql_as_string = sql_file.read()
        self.conn_lexicon.executescript(sql_as_string)
        self.conn_lexicon.commit()
        # get token from hatebase
        if (self.token is None) or self.expired():
            self.refresh_token()
        # create cursor
        cursor = self.conn_lexicon.cursor()

        # Save (commit) the changes

        res = requests.post('https://api.hatebase.org/4-4/get_vocabulary',
                            dict(token=self.token, page=1))
        for i in res.json()["result"]:
            self.insert_term(i, cursor)
        pages = res.json()["number_of_pages"]
        print(f"1/{pages}")
        for j in range(2, pages):
            res = requests.post('https://api.hatebase.org/4-4/get_vocabulary',
                                dict(token=self.token, page=j))
            print(f"{j}/{pages}")
            for i in res.json()["result"]:
                self.insert_term(i, cursor)

        self.conn_lexicon.commit()
        print("done")

    def show_lexicon_db(self):
        c = self.conn_lexicon.execute("select * from lexicon")
        for i in c:
            print(i)

    def create_data_db(self):
        sql_file = open("./db/create_data_db.sql")
        self.conn_data.executescript(sql_file.read())
        self.conn_data.commit()

        # create cursor
        cursor = self.conn_data.cursor()

        # Read csv
        with open("../gekregen github repo/data/labeled_data.csv") as file:
            reader = csv.reader(file,delimiter=',')
            next(reader)
            for row in reader:
                self.insert_data(row,cursor)
        self.conn_data.commit()
        print("done")

    @staticmethod
    def insert_data(i, cursor):
        total = int(i[1])/2
        cursor.execute('insert or ignore into data values (?,?,?,?)', (int(i[0]), int(i[2])>=total,int(i[3])>=total,i[-1]))

    def show_data_db(self):
        c = self.conn_data.execute("select * from data")
        for i in c:
            print(i)
