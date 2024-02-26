import base64
from flask import Flask, render_template, request, session
import requests
from typing import Union
import flask
import secrets
from database_conn import get_collection
from datetime import datetime

# Generate a secure random secret key for Flask
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key


def get_api_records(api_url):
    url = f"https://linkifinity-api-4p3puslswa-uc.a.run.app/{api_url}"
    response = requests.get(url=url)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        return data
    else:
        return {'error': 'Failed to fetch data'}, response.status_code


@app.route("/")
def index() -> str:
    """
    Remove 'submitted' key from session and render the index.html template.

    Returns:
        str: The rendered HTML template.
    """
    session.pop("submitted", None)
    return render_template("index.html")


@app.route("/manga")
def manga():
    records = get_api_records('chapters')
    mangas = []
    for record in records:
        chapters = record['Latest_chapters']
        if len(chapters) > 2:
            record['Latest_chapters'] = chapters[:2]
        else:
            record['Latest_chapters'] = chapters
        mangas.append(record)
    return render_template("manga_chapters_list.html", mangas=mangas)


@app.route("/chapters/<title>", methods=["GET"])
def chapters(title):
    chapters_url = f'chapters/{title}'
    manga = get_api_records(chapters_url)
    manga_len = False if not manga else True
    return render_template(
        "manga_chapters.html", manga=manga, manga_len=manga_len, title=title
    )


@app.route("/saveurl", methods=["POST"])
def save_data_to_mongodb() -> Union[str, "flask.Response"]:
    """
    Save user input data to MongoDB if it does not already exist.

    Returns:
        - If data already exists: A rendered template with a message.
        - If data does not exist: A rendered template with a message and an insert message.
    """
    links_collection = get_collection("get_csv_links")  # get_manga_links()
    current_datetime = datetime.now()
    date_added = datetime(
        current_datetime.year, current_datetime.month, current_datetime.day
    )

    user_input = request.form["user_input"]
    data = {"Manga_url": user_input}
    existing_data = links_collection.find_one(data)
    if existing_data:
        message = "Data already exists in the database!"
    else:
        data["Date_added"] = date_added
        links_collection.insert_one(data)
        message = "Data saved successfully to MongoDB!"

    return render_template(
        "index.html", message=message, insert_message=not existing_data
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
