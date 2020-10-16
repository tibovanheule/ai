import aiosqlite

class DB:

    def __init__():
        self.conn_lexicon = await aiosqlite.connect('db/lexicon.db')
        self.conn_trainings_data = await aiosqlite.connect('db/train_data.db')

	
