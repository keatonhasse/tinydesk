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

def parse(r: requests.Response, status: bool):
    if not status:
        print('error')
        return None, False
    else:
        return BeautifulSoup(r.content, 'lxml'), True

def request(url: str) -> (any, bool):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup, r.status_code == 200
    #if r.status_code != 200:
    #    return None, False
    #else:
    #    return r, True

def test():
    r, status = request('https://www.npr.org/get/92071316/render/partial/next?start=0')
    if not status:
        print('error')
    else:
        print(r.content)
    #if status == False:
    #    print('error')
    #else:
    #    soup = BeautifulSoup(r.content, 'lxml')
    #    print()

def fetch_episode(url: str):
    soup, status = request(url)
    #soup, s = parse(r, status)
    j = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]
    return j, status

    #r, status = request(url)
   #if not status:
    #    print('error')
    #    return None, False
    #else:
    #    soup = BeautifulSoup(r.content, 'lxml')
    #    j = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]
    #    return j, True
    #r = requests.get(url)
    #if r.status_code != 200:
    #    print('error')
    #    return
    #else:
    #    soup = BeautifulSoup(r.content, 'lxml')
    #    j = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]
    #    return j

def fetch(url: str):
    soup, status = request(url)
    #soup, s = parse(r, status)
    for e in soup.find_all('article', class_='item event-more-article'):
        episode, e_status = fetch_episode(e.find('a').get('href'))
        return episode, e_status

    #r, status = request(url)
    #if not status:
    #    print('error')
    #    return None, False
    #else:
    #    soup = BeautifulSoup(r.content, 'lxml')
    #    for e in soup.find_all('article', class_='item event-more-article'):
    #        episode = fetch_episode(e.find('a').get('href'))
    #        return episode, True
    #r = requests.get(url)
    #if r.status_code != 200:
    #    print('error')
    #    return False
    #else:
    #    soup = BeautifulSoup(r.content, 'lxml')
    #    for el in soup.find_all('article', class_='item event-more-article'):
    #        #print(el)
    #        episode = fetch_episode(el.find('a').get('href'))
    #        print(episode)
    #    return True

def main() -> None:
    #test()
    scraping: bool = True
    page: int = 0
    while scraping:
        url: str = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        #print(fetch(url))
        e, s = fetch(url)
        print(e)
        print(s)
        scraping = s
        page += len(e)
        #r: str = requests.get(URL)
        #soup = BeautifulSoup(r.content, 'html.parser')
        #if r.status_code != 200:
        #    status = False
        #else:
            #els = soup.find_all('article', class_='item event-more-article')
            #for el in els:
                #r2: str = requests.get(el.find('a').get('href'))
                #if r2.status_code != 200:
                #    break
                #else:
                    #soup2 = BeautifulSoup(r2.content, 'html.parser')
                    #j = json.loads(soup2.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]
                    #print(j['subjectOf'][0]['embedUrl'])
                    #print(j['description'])
                    #print(j)
                    #if j['subjectOf'][0]['embedUrl'].endswith('m3u8'):
                    #if j['embedUrl'].endswith('m3u8'):
                        #print(m3u8.load(j['embedUrl']).playlists)
                        #print(m3u8.load(j['subjectOf'][0]['embedUrl']).playlists) #playlist is each stream format
            #page += len(els)

if __name__ == '__main__':
    main()
