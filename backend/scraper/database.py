import sqlite3

class Database:
    def __init__(self, name='../tinydesk.db'):
        self.con = sqlite3.connect(name)
        self.create_tables()
    
    def close(self) -> None:
        self.con.close()

    def create_tables(self) -> None:
        self.con.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                thumbnail TEXT
            );
        ''')
        self.con.commit()

    def insert(self, episode: tuple[str, ...]) -> None:
        self.con.execute('''
            INSERT INTO episodes VALUES (?, ?, ?, ?, ?);
        ''', episode)
        self.con.commit()
    
    def last_page(self) -> int:
        cur = self.con.cursor()
        cur.execute('SELECT COUNT(*) FROM episodes')
        return cur.fetchone()[0]
    
    def contains(self, url: str) -> bool:
        cur = self.con.cursor()
        cur.execute('SELECT COUNT(*) FROM episodes WHERE url = ?', (url,))
        return cur.fetchone()[0] != 0
