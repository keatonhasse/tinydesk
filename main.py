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
    print(f'fetching {url}')
    soup = request(url)
    available = soup.find('p', class_='unvailable')
    playlist = soup.find('ul', class_='playlist')
    if available is None and playlist is None:
        print('still fetching')
        json_text = soup.find('script', {'type': 'application/ld+json'}).text
        json_data = json.loads(json_text)
        if 'subjectOf' in json_data:
            episode_data = json_data['subjectOf'][0]
            if 'embedUrl' in episode_data:
                timestamp = int(datetime.fromisoformat(episode_data['uploadDate']).timestamp())
                description = soup.find('meta', {'name': 'description'})['content']
                description = description.replace('amp;', '')
                episode = (
                    url,
                    episode_data['name'],
                    timestamp,
                    episode_data['thumbnailUrl'],
                    episode_data['embedUrl'],
                    description
                )
                db.insert(episode)

def fetch_episodes(url: str) -> None:
    print('fetch episodes')
    soup = request(url)
    classes = ['item event-more-article', 'item event-more-article article-type-audio']
    episodes = soup.find_all('article', class_=classes)
    for episode in episodes:
        url = episode.find('a')['href']
        if not db.check_url(url) and url not in skip_urls:
            fetch_episode(url)

def main() -> None:
    page = db.last_page()
    print(page)
    while True:
        r = requests.get(f'https://www.npr.org/get/92071316/remainingCount?start={page}')
        remaining = int(r.text)
        if remaining != 24:
            break
        url = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        fetch_episodes(url)
        page += remaining
        db.update_page(page)
    print('all episode urls collected')

if __name__ == '__main__':
    skip_urls = (
        'https://www.npr.org/2014/10/04/353534954/ryan-keberle-catharsis-tiny-desk-concert',
        'https://www.npr.org/2022/12/09/1140051996/eliane-elias-tiny-desk-concert',
        'https://www.npr.org/series/761983313/tiny-desk-playlists',
        'https://www.npr.org/music'
    )
    db = Database()
    main()
    db.close()
