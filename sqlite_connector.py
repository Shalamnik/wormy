import sqlite3


class SQLiteConnector:
    def __init__(self, file='wormy.db'):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        if value:
            raise KeyError(value)
        self.conn.close()
