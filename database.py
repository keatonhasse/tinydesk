import sqlite3

class Database:
    def __init__(self, name='tinydesk.db'):
        self.con = sqlite3.connect(name)
        self.create_table()

    def create_table(self):
        self.con.execute('''
            CREATE TABLE IF NOT EXISTS episodes(
                name,
                description,
                thumbnail,
                upload_date PRIMARY KEY,
                url
            )
        ''')
        self.con.commit()

    def insert(self, episode):
        self.con.execute('INSERT INTO episodes VALUES(?, ?, ?, ?, ?)', episode)
        self.con.commit()

    def select(self):
        self.con.execute('SELECT COUNT(*) FROM episodes')
    
    def check_timestamp(self, timestamp: str) -> bool:
        cur = self.con.cursor()
        cur.execute('SELECT COUNT(*) FROM episodes WHERE upload_date = ?', (timestamp,))
        return cur.fetchone()[0] != 0
