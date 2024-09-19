from fastapi import FastAPI, Body, HTTPException
from starlette import status

from src.utilities.mongodb_crud_api import get_records, insert_records, delete_records
from src.models.PostModels import PostLinks

app = FastAPI()


@app.get('/api/links', status_code=status.HTTP_200_OK)
async def get_all_links():
    try:
        records = get_records(endpoint='all_links')
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get('/api/chapters', status_code=status.HTTP_200_OK)
async def get_all_metadata():
    try:
        records = get_records(endpoint='chapters')
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get('/api/chapter', status_code=status.HTTP_200_OK)
async def get_metadata_one(query: str):
    try:
        records = get_records(search_key=query, endpoint='chapter')
        if not records:
            return HTTPException(status_code=404, detail=f'{query} - Manga Not Found')
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.post("/api/insert_link", status_code=status.HTTP_201_OK)
async def insert_data_to_db(links: PostLinks = Body()):
    try:
        validated_data = links.dict()
        result = insert_records(collection_tag=validated_data['tags'], links=validated_data["links"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")


@app.delete("/api/delete_record", status_code=status.HTTP_200_OK)
async def delete_records_db(links: PostLinks = Body()):
    try:
        validated_data = links.dict()
        result = delete_records(collection_tag=validated_data['tags'], payload=validated_data["links"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting records: {str(e)}")
