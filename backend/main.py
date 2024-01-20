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
    videos = YoutubeSearch(f'{title} Tiny Desk Concert', max_results=2).to_dict()
    if videos[0]['channel'] == 'NPR Music' or videos[1]['channel'] == 'NPR Music':
        if 'Home' in videos[0]['title'] and 'Home' in title:
            return videos[0]['id']
        return videos[1]['id']

def parse_episode(url: str, episode) -> tuple[str, ...]:
    url = episode.find('a')['href']
    title = episode.find('h2', class_='title').text
    time = episode.find('time')['datetime']
    timestamp = int(datetime.strptime(time, '%Y-%m-%d').timestamp())
    image = episode.find('img')
    thumbnail = None
    if image:
        thumbnail = re.search(r'[\w-]+\.(jpg|jpeg|png)', image['src']).group(0)
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
