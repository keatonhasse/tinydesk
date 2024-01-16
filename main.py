import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from yt_dlp import YoutubeDL

from database import Database

def request(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

def fetch_episode(url: str) -> None:
    soup = request(url)
    j = soup.find('script', {'type': 'application/ld+json'}).text
    episode_data = json.loads(j)['subjectOf'][0]
    timestamp = int(datetime.fromisoformat(episode_data['uploadDate']).timestamp())
    episode = (
        episode_data['name'],
        episode_data['description'],
        episode_data['thumbnailUrl'],
        timestamp,
        episode_data['embedUrl']
    )
    if not db.check_timestamp(timestamp):
        db.insert(episode)
    print(episode)

def fetch_episodes(url: str) -> None:
    soup = request(url)
    classes = ['item event-more-article', 'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for episode in episodes:
        url = episode.find('a')['href']
        #fetch_episode(url)

def main() -> None:
    page = 0
    while True:
        r = requests.get(f'https://www.npr.org/get/92071316/remainingCount?start={page}')
        remaining = int(r.text)
        if remaining != 24:
            break
        url = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        fetch_episodes(url)
        page += remaining
    print('all episode urls collected')

if __name__ == '__main__':
    db = Database()
    main()
    db.close()
