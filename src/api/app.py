from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def get_all_links():
    return "Hey there! Welcome to MangatrackerX"


@app.post('/api/manga_link')
async def add_manga_link(manga_url: str):
    return manga_url