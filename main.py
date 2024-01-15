import json
import sqlite3
from datetime import datetime

import requests
from bs4 import BeautifulSoup
#from flask import Flask
from yt_dlp import YoutubeDL

class Episode:
    def __init__(self, name, description, thumbnail, upload_date, url):
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.upload_date = upload_date
        self.url = url

def request(url: str) -> BeautifulSoup:
    r: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(r.content, 'lxml')
    return soup

def fetch_episode(url: str):
    soup = request(url)
    j = soup.find('script', {'type': 'application/ld+json'}).text
    episode = json.loads(j)['subjectOf'][0]
    e = Episode(episode['name'],
                episode['description'],
                episode['thumbnailUrl'],
                int(datetime.fromisoformat(episode['uploadDate']).timestamp()),
                episode['embedUrl'])
    print(f'{e.name}\n{e.description}\n{e.thumbnail}\n{e.upload_date}\n{e.url}\n')

def fetch_episodes(url: str):
    soup = request(url)
    classes = ['item event-more-article', 'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for e in episodes:
        url = e.find('a').get('href')
        fetch_episode(url)

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
    main()
