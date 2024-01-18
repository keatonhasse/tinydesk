import json
import re
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
#from fastapi import FastAPI
#from yt_dlp import YoutubeDL

from database import Database

def request(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

def parse_episode(soup: BeautifulSoup) -> tuple[str, ...]:
    aria = soup.find('div', class_='speakable').find_all('b')
    graphic_wrapper = soup.find('div', class_='graphicwrapper')
    jwplayer = json.loads(graphic_wrapper.find_all('div')[1]['data-jwplayer'])
    return (
        aria[0].text,
        int(datetime.fromisoformat(soup.find('time')['datetime']).timestamp()),
        jwplayer['image'],
        jwplayer['sources'][0]['file'],
        aria[1].text
    )

def fetch_episode(url: str) -> None:
    print(f'fetching {url}')
    soup = request(url)
    #available = soup.find('p', class_='unvailable')
    #if available is None:
    episode = (url,) + parse_episode(soup)
    db.insert(episode)

def fetch_episodes(url: str) -> None:
    print('fetching episodes')
    path_pattern = r'^\/\d{4}\/\d{2}\/\d{2}\/\d+\/[\a-z-]+$'
    soup = request(url)
    classes = ['item event-more-article',
               'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for episode in episodes:
        episode_url = episode.find('a')['href']
        path = urlparse(episode_url).path
        if not re.match(path_pattern, path):
            continue
        if not db.contains(episode_url):
            fetch_episode(episode_url)

def main() -> None:
    base = 'https://www.npr.org/get/92071316'
    fetch_episodes(f'{base}/render/partial/next?start=0')
    page = db.last_page()
    while True:
        print(page)
        params = f'start={page}'
        remaining = int(requests.get(f'{base}/remainingCount?{params}').text)
        if remaining != 24:
            break
        fetch_episodes(f'{base}/render/partial/next?{params}')
        page += remaining

if __name__ == '__main__':
    db = Database()
    main()
    db.close()
