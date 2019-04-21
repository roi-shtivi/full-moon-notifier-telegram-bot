import sqlite3


class SubscribersDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('subscribers.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers
                               (chat_id type UNIQUE)''')

    def insert(self, chat_id):
        self.cursor.execute('''INSERT INTO subscribers VALUES ({})'''.format(chat_id))
        self.conn.commit()

    def delete(self, chat_id):
        self.cursor.execute('''DELETE FROM subscribers WHERE chat_id={}'''.format(chat_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_all_subscribers(self):
        return [chat_id for (chat_id, ) in self.cursor.execute('SELECT chat_id FROM subscribers')]
