import json
import sqlite3
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from yt_dlp import YoutubeDL

class Episode:
    name: str
    description: str
    thumbnail: str
    upload_date: str
    url: str

    def __init__(self, name: str, description: str, thumbnail:str , upload_date: str, url: str) -> None:
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.upload_date = upload_date
        self.url = url

def request(url: str) -> BeautifulSoup:
    r: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(r.content, 'lxml')
    return soup

def fetch_episode(url: str) -> None:
    soup: BeautifulSoup = request(url)
    j = soup.find('script', {'type': 'application/ld+json'}).text
    e = json.loads(j)['subjectOf'][0]
    timestamp = int(datetime.fromisoformat(e['uploadDate']).timestamp())
    episode = (e['name'],
        e['description'],
        e['thumbnailUrl'],
        timestamp,
        e['embedUrl'])
    '''e = Episode(episode['name'],
                episode['description'],
                episode['thumbnailUrl'],
                int(datetime.fromisoformat(episode['uploadDate']).timestamp()),
                episode['embedUrl'])'''
    if db.check(timestamp):
        db.insert(episode)
    #print(f'{e.name}\n{e.description}\n{e.thumbnail}\n{e.upload_date}\n{e.url}\n')

def fetch_episodes(url: str) -> None:
    soup: BeautifulSoup = request(url)
    classes = ['item event-more-article', 'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for e in episodes:
        url = e.find('a').get('href')
        fetch_episode(url)

class Database:
    def __init__(self, name='tinydesk.db'):
        print('init db')
        self.con = sqlite3.connect(name)
        self.create_table()

    def create_table(self):
        print('create table')
        self.con.execute('''CREATE TABLE IF NOT EXISTS episodes(name,
            description,
            thumbnail,
            upload_date PRIMARY KEY,
            url)''')
        self.con.commit()

    def insert(self, episode):
        self.con.execute('INSERT INTO episodes VALUES(?, ?, ?, ?, ?)', episode)
        self.con.commit()

    def select(self):
        pass
    
    def check(self, timestamp) -> bool:
        cur = self.con.cursor()
        cur.execute('SELECT COUNT(*) FROM episodes WHERE upload_date = ?', (timestamp,))
        res = cur.fetchone()
        return res[0] == 0

def main() -> None:
    scraping: bool = True
    page: int = 0

    while scraping:
        r = requests.get(f'https://www.npr.org/get/92071316/remainingCount?start={page}')
        remaining: int = int(r.text)
        if remaining != 24:
            scraping = False
            break
        url: str = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        fetch_episodes(url)
        page += remaining
    print('all episode urls collected')

if __name__ == '__main__':
    db = Database()
    main()
    db.close()
