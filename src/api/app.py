from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def get_all_links():
    return "Hey there! Welcome to MangatrackerX"
