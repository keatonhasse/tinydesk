import sqlite3
from fastapi import FastAPI

app = FastAPI()

@app.get('/episodes')
def get_episodes():
    con = sqlite3.connect('tinydesk.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM episodes LIMIT 5;')
    rows = cur.fetchall()
    con.close()
    return  rows

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
