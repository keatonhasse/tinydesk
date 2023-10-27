import json
#import sqlite3

import m3u8
import requests
#import youtube_dl
from bs4 import BeautifulSoup
#from flask import Flask

class Episode:
    def __init__(self, title, description, url, audio_url, video_url):
        self.title = title
        self.description = description
        self.url = url
        self.audio_url = audio_url
        self.video_url = video_url

    #def __str__(self):
    #    return f'{self.title}'

# script type="application/ld+json"

def getEpisodes() -> list[str, ...]:
    episodes: list[str, ...] = []
    for el in soup.find_all('article', class_='item event-more-article'):
        episode = Episode()
        episode.title = el.find('a')
        print(episode)
        #episodes.append()
    return episodes

def main() -> None:
    status: bool = True
    page: int = 0
    while status:
        URL: str = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        r: str = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        if r.status_code != 200:
            status = False
        else:
            els = soup.find_all('article', class_='item event-more-article')
            for el in els:
                r2: str = requests.get(el.find('a').get('href'))
                if r2.status_code != 200:
                    break
                else:
                    soup2 = BeautifulSoup(r2.content, 'html.parser')
                    j = json.loads(soup2.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]
                    #print(j['subjectOf'][0]['embedUrl'])
                    print(j['description'])
                    #print(j)
                    #if j['subjectOf'][0]['embedUrl'].endswith('m3u8'):
                    #if j['embedUrl'].endswith('m3u8'):
                        #print(m3u8.load(j['embedUrl']).playlists)
                        #print(m3u8.load(j['subjectOf'][0]['embedUrl']).playlists) #playlist is each stream format
            #page += len(els)

if __name__ == '__main__':
    main()
