import sqlite3

class Database:
    def __init__(self, name='tinydesk.db'):
        self.con = sqlite3.connect(name)
        self.create_tables()

    def create_tables(self) -> None:
        self.con.execute('''
            CREATE TABLE IF NOT EXISTS episodes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                thumbnail TEXT NOT NULL,
                embed_url TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        self.con.execute('''
            CREATE TABLE IF NOT EXISTS page(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_page INTEGER NOT NULL
            )
        ''')
        self.con.commit()

    def insert(self, episode: tuple[str, ...]) -> None:
        self.con.execute(
            '''INSERT INTO episodes(
                url,
                title,
                upload_date,
                thumbnail,
                embed_url,
                description
            ) VALUES(?, ?, ?, ?, ?, ?)''', episode
        )
        self.con.commit()

    def update_page(self, page: int) -> None:
        self.con.execute(f'UPDATE page SET last_page = {page} WHERE id = 1')
        self.con.commit()

    def select(self):
        pass
    
    def last_page(self) -> int:
        cur = self.con.cursor()
        cur.execute('SELECT last_page FROM page WHERE id = 1')
        return cur.fetchone()[0]
    
    def check_url(self, url: str) -> bool:
        cur = self.con.cursor()
        cur.execute('SELECT COUNT(*) FROM episodes WHERE url = ?', (url,))
        return cur.fetchone()[0] != 0
