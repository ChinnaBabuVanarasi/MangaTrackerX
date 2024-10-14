from fastapi import FastAPI, Body, HTTPException
from starlette import status


from ..utilities.mongodb_crud_api import get_records, insert_records, delete_records
from ..models.PostModels import PostLinks

app2 = FastAPI()


@app2.get('/')
async def helloWorld():
    return "<h1>Hello World </h1>"