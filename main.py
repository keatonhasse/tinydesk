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

def fetch_episode(url: str) -> None:
    print(f'fetching {url}')
    soup = request(url)
    #available = soup.find('p', class_='unvailable')
    #if available is None:
    aria = soup.find('div', class_='speakable').find_all('b')
    title = aria[0].text
    timestamp = int(datetime.fromisoformat(soup.find('time')['datetime']).timestamp())
    jw_player = soup.find('div', class_='graphicwrapper')
    jw_player_json = json.loads(jw_player.find_all('div')[1]['data-jwplayer'])
    thumbnail = jw_player_json['image']
    content_url = jw_player_json['sources'][0]['file']
    description = aria[1].text
    episode = (
        url,
        title,
        timestamp,
        thumbnail,
        content_url,
        description
    )
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
