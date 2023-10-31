import asyncio
#import csv
import json
#import sqlite3

import httpx
#import m3u8
import requests
#import youtube_dl
from bs4 import BeautifulSoup
#from flask import Flask

async def request(client, url: str) -> (BeautifulSoup, bool):
    r = await client.get(url)
    #r: requests.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(r.content, 'lxml')
    return soup, r.status_code == 200

def test():
    r, status = request('https://www.npr.org/get/92071316/render/partial/next?start=0')
    if not status:
        print('error')
    else:
        print(r)

def fetch_episode(url: str):
    soup, status = request(url)
    print('got episode')
    j = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)['subjectOf'][0]

def fetch(url: str):
    soup, status = request(url)
    episodes = soup.find_all('article', class_='item event-more-article')
    print('got episodes')
    for e in episodes:
        fetch_episode(e.find('a').get('href'))
    return episodes, status

def print_titles(episodes):
    for e in episodes:
        print(e.find('h2', class_='title').text)

async def main() -> None:
    #test()
    scraping: bool = True
    page: int = 0
    while scraping:
        url: str = f'https://www.npr.org/get/92071316/render/partial/next?start={page}'
        async with httpx.AsyncClient() as client:
            pass
        episodes, status = fetch(url)
        scraping = status
        page += len(episodes)
        print_titles(episodes)

if __name__ == '__main__':
    main()
