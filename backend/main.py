import os
import sqlite3

from fastapi import FastAPI
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get('/episodes')
def get_episodes():
    con = sqlite3.connect('tinydesk.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM episodes ORDER BY timestamp DESC;')
    rows = cur.fetchall()
    con.close()
    return rows

@app.get('/episodes/{video_id}', response_class=FileResponse)
def fetch_episode(video_id):
    path = f'./episodes/{video_id}.mp3'
    if not os.path.exists(path):
        options = {
            'outtmpl': './episodes/%(id)s.mp3',
            'format': 'bestaudio',
            'quiet': True
        }
        url = f'https://youtube.com/watch?v={video_id}'
        with YoutubeDL(options) as ydl:
            ydl.download(url)
    return path

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
