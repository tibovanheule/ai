"""@package DB
This module manages access to the sqllite databases, these provide better performance than CSV files.

More details.
"""
import random
import string
from csv import reader
from datetime import datetime, timezone
from sqlite3 import connect

from requests import post


class DB:
    """  collection of all db connections


    """
    def __init__(self):

        self.conn_lexicon = connect('db/lexicon.db', isolation_level=None)
        self.conn_data = connect('db/train_data.db', isolation_level=None)
        self.conn_model = connect('db/model_data.db', isolation_level=None)
        self.conn_ad = connect('db/ad_data.db', isolation_level=None)
        self.conn_extra_data = connect('db/extra_data.db', isolation_level=None)
        self.token = None
        self.expires = None

    def refresh_token(self):
        """  refresh hatebase token
        """
        response = post('https://api.hatebase.org/4-4/authenticate',
                        dict(api_key='sQmKeVgLQwrWJmyNvCUaziuDbsEVypnt'))
        self.token = response.json()["result"]["token"]
        self.expires = datetime.strptime(response.json()["result"]["expires_on"], '%Y-%m-%d %H:%M:%S')
        self.expires = self.expires.replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(self.expires)

    def expired(self):
        """  check if hatebase token is expired
        """
        return datetime.now(tz=None) >= self.expires

    @staticmethod
    def insert_term(i, cursor):
        """  insert a term in the lexicon database
        """
        cursor.execute('insert or ignore into lexicon values (?,?)', (i["term"],
                                                                      i["average_offensiveness"]))

    def create_lexicon_db(self):
        """  create and populate the lexicon database
        """
        with open("./db/create_lexicon_db.sql") as sql_file:
            sql_as_string = sql_file.read()
            self.conn_lexicon.executescript(sql_as_string)
            self.conn_lexicon.commit()
        # get token from hatebase
        if (self.token is None) or self.expired():
            self.refresh_token()
        # create cursor
        cursor = self.conn_lexicon.cursor()

        # Save (commit) the changes

        res = post('https://api.hatebase.org/4-4/get_vocabulary',
                   dict(token=self.token, page=1))
        for i in res.json()["result"]:
            self.insert_term(i, cursor)
        pages = res.json()["number_of_pages"]
        print(f"1/{pages}")
        for j in range(2, pages):
            res = post('https://api.hatebase.org/4-4/get_vocabulary',
                       dict(token=self.token, page=j))
            print(f"{j}/{pages}")
            for i in res.json()["result"]:
                self.insert_term(i, cursor)

        self.conn_lexicon.commit()
        print("done")

    def show_lexicon_db(self):
        """ print the lexicon database
        """
        c = self.conn_lexicon.execute("select * from lexicon")
        for i in c:
            print(i)

    def create_data_db(self):
        """  Read the csv and create the data database
        """
        with open("./db/create_data_db.sql") as sql_file:
            self.conn_data.executescript(sql_file.read())
            self.conn_data.commit()

        # create cursor
        cursor = self.conn_data.cursor()

        # Read csv
        with open("../gekregen github repo/data/labeled_data.csv") as file:
            read = reader(file, delimiter=',')
            next(read)
            for row in read:
                self.insert_data(row, cursor)
        self.conn_data.commit()
        print("done")

    def create_adversarial_db(self):
        """  Create the adversarial database

        Used to create adversarials totally random
        """
        with open("./db/create_adversarial_db.sql") as sql_file:
            self.conn_ad.executescript(sql_file.read())
            self.conn_ad.commit()

        # create cursor
        cursor = self.conn_ad.cursor()
        l = [i[0] for i in self.db_load_lexicon()]
        # Read csv
        with open("./db/Ethos_Dataset_Binary.csv", encoding='utf-8') as file:
            read = reader(file, delimiter=';')
            next(read)
            for i in read:
                # don't wont every non-hate, but some to test
                if float(i[-1]) <= 0.5:
                    i[-1] = "0"
                    print("insert")
                    self.insert_ad(i, cursor)
                # hate speech do something
                else:
                    i[-1] = "1"
                    tweet = i[0]
                    print(tweet)
                    hate_in_tweet = [word for word in l if word in tweet.split()]
                    if len(hate_in_tweet) > 0:
                        print("HATEBASE")
                        print(hate_in_tweet)
                        for k in hate_in_tweet:
                            if random.random() < 0.25:
                                print("CHAR BOUNDARY")
                                left = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in
                                               range(random.randint(2, (len(tweet) % 4) + 2)))
                                right = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in
                                                range(random.randint(2, (len(tweet) % 4) + 2)))
                                new = left + k + right
                                tweet = tweet.replace(k, new, 1)
                    for _ in [0, 1]:
                        if random.random() < 0.5:
                            r = random.randint(1, len(tweet) // 2)
                            tweet = tweet[:r] + tweet[r:].replace(' ', "", 1)
                        if random.random() > 0.5:
                            r = random.randint(1, len(tweet) - 1)
                            tweet = tweet[:r] + ' ' + tweet[r:]
                    i[0] = tweet
                    print(i[0])
                    self.insert_ad(i, cursor)
        self.conn_ad.commit()
        print("done")

    def create_extra_db(self):
        """ create a data database using a new diffrent dataset
        """
        with open("./db/create_extra_db.sql") as sql_file:
            self.conn_extra_data.executescript(sql_file.read())
            self.conn_extra_data.commit()

        # create cursor
        cursor = self.conn_extra_data.cursor()
        # Read csv
        with open("./db/Ethos_Dataset_Binary.csv", encoding='utf-8') as file:
            read = reader(file, delimiter=';')
            next(read)
            for i in read:
                # don't wont every non-hate, but some to test
                if float(i[-1]) <= 0.5:
                    i[-1] = "0"
                    self.insert_extra(i, cursor)
                # hate speech do something
                else:
                    i[-1] = "1"
                    self.insert_extra(i, cursor)
        self.conn_extra_data.commit()
        print("done")

    @staticmethod
    def insert_ad(i, cursor):
        """  insert an adversarial into the adversarial database
        """
        cursor.execute('insert or ignore into adversarial (hate_speech,offensive_language,tweet) values (?,?,?)',
                       (int(i[-1]), 0, i[0]))

    @staticmethod
    def insert_extra(i, cursor):
        """  insert a tweet into the extra data database
        """
        cursor.execute('insert or ignore into extra (hate_speech,offensive_language,tweet) values (?,?,?)',
                       (int(i[-1]), 0, i[0]))

    @staticmethod
    def insert_data(i, cursor):
        """  insert an term into the data database
        """
        total = int(i[1]) / 2
        cursor.execute('insert or ignore into data values (?,?,?,?)',
                       (int(i[0]), int(i[2]) >= total, int(i[3]) >= total, i[-1]))

    def show_data_db(self):
        """  print data database
        """
        c = self.conn_data.execute("select * from data")
        for i in c:
            print(i)

    def db_load_lexicon(self):
        """  give an array of all term in lexicon
        """
        c = self.conn_lexicon.execute("select term from lexicon")
        return c.fetchall()

    def db_load_tweet(self):
        """  give an array of all tweets in data
        """
        c = self.conn_data.execute("select tweet from data order by id asc")
        return c.fetchall()

    def db_load_hate(self):
        """  give an array of all hate labels in data
        """
        c = self.conn_data.execute("select hate_speech from data order by id asc;")
        return c.fetchall()

    def db_load_ad_hate(self):
        """  give an array of all hate labels in adversarial database
        """
        c = self.conn_ad.execute("select hate_speech from adversarial order by id asc;")
        return c.fetchall()

    def db_load_ad_tweet(self):
        """  give an array of all tweets in adversarial database
        """
        c = self.conn_ad.execute("select tweet from adversarial order by id asc;")
        return c.fetchall()

    def db_load_extra_hate(self):
        """  give an array of all hate labels in extra data database
        """
        c = self.conn_extra_data.execute("select hate_speech from extra order by id asc;")
        return c.fetchall()

    def db_load_extra_tweet(self):
        """  give an array of all tweets in extra data database
        """
        c = self.conn_extra_data.execute("select tweet from extra order by id asc;")
        return c.fetchall()

    def create_model_db(self):
        """  Create a model database
        """
        with open("./db/create_model_db.sql") as sql_file:
            self.conn_model.executescript(sql_file.read())
            self.conn_model.commit()
        print("done")

    def model_in_db(self, name):
        """  check if a model is in the model database
        """
        listd = self.conn_model.execute("select status from model where name=?", (name,)).fetchall()
        if not listd:
            return False
        return listd[0][0] == 0

    def insert_model_in_db(self, name, model):
        """  insert a model in the model database
        """
        return self.conn_model.execute("INSERT OR REPLACE into model (name,model,cat,status) values (?,?,?,?)",
                                       (name, model, 0, 0,))

    def insert_vect_in_db(self, name, vect):
        """  insert a vectorizer in the model database
        """
        name = name + "_vect"
        return self.conn_model.execute("INSERT OR REPLACE into model (name,model,cat,status) values (?,?,?,?)",
                                       (name, vect, 1, 0,))

    def constructing_model_in_db(self, name):
        """  construct a model, remove existing model in db

        to evade predicting when a model is rebuilding
        """
        return self.conn_model.execute("INSERT OR REPLACE into model (name,model,cat,status) values (?,?,?,?)",
                                       (name, "", 0, 1,))

    def get_model_in_db(self, name):
        """  get a model from the model database
        """
        return self.conn_model.execute("select model from model where name=?", (name,)).fetchall()
