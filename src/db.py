"""@package DB
This module manages access to the sqllite databases, these provide better performance than CSV files.

More details.
"""

import aiosqlite

class DB:
    def __init__(self):
        self.conn_lexicon = await aiosqlite.connect('db/lexicon.db')
        self.conn_trainings_data = await aiosqlite.connect('db/train_data.db')
