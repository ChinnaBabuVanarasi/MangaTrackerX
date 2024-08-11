from fastapi import FastAPI
from fastapi import FastAPI

from src.utilities.mongodb_crud import get_records

app = FastAPI()


@app.get('/api/links')
async def get_all_links():
    records = get_records('get_manga_chapters')
    links = [record['manga_url'] for record in records]
    return links


@app.get('/api/metadata')
async def get_all_metadata():
    records = get_records('get_manga_chapters')
    metadata = [{k: v for k, v in d.items() if k != 'latest_chapters'} for d in records]
    return metadata


@app.get('/api/metadata/{manga_title}')
async def get_metadata_one(manga_title: str):
    records = get_records(collection_name='get_manga_chapters', search_key=manga_title)
    return records
