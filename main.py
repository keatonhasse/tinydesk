import json
import re
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
#from fastapi import FastAPI
from youtube_search import YoutubeSearch
#from yt_dlp import YoutubeDL

from database import Database

def request(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

def fetch_video_id(title: str) -> str:
    video = YoutubeSearch(title, max_results=1).to_dict()
    print(video[0]['id'])
    return video[0]['id']

def parse_episode(url: str, episode) -> tuple[str, ...]:
    print(f'fetching {url}')
    url = episode.find('a')['href']
    title = episode.find('h2', class_='title').text
    time = episode.find('time')['datetime']
    timestamp = int(datetime.strptime(time, '%Y-%m-%d').timestamp())
    thumbnail = re.search(r'[\w-]+\.(jpg|jpeg|png)', episode.find('img')['src']).group(0)
    episode = (
        fetch_video_id(title),
        url,
        title,
        timestamp,
        thumbnail
    )
    db.insert(episode)

def fetch_episodes(url: str) -> None:
    soup = request(url)
    classes = ['item event-more-article',
               'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for episode in episodes:
        episode_url = episode.find('a')['href']
        path = urlparse(episode_url).path
        if path in BAD_PATHS:
            continue
        if not db.contains(episode_url):
            parse_episode(episode_url, episode)

def main() -> None:
    base = 'https://www.npr.org/get/92071316'
    fetch_episodes(f'{base}/render/partial/next?start=0')
    page = db.last_page()
    while True:
        print(f'fetching page {page}')
        params = f'start={page}'
        remaining = int(requests.get(f'{base}/remainingCount?{params}').text)
        if remaining != 24:
            break
        fetch_episodes(f'{base}/render/partial/next?{params}')
        page += remaining

if __name__ == '__main__':
    BAD_PATHS = (
        '/2021/04/23/989905360/tiny-desk-meets-afropunk-chocquibtown-nenny-luedji-luna-calma-carmona',
        '/2015/12/10/459054571/sharon-jones-the-dap-kings-play-one-for-hanukkah',
        '/series/761983313/tiny-desk-playlists',
        '/music'
    )
    db = Database()
    main()
    db.close()
