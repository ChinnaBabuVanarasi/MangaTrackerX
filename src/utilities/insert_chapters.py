def insert_chapters_data(new_chapters, current_chapter, chapter_collection, record):
    if current_chapter != 0 and float(new_chapters[0]['chapter_num']) > float(current_chapter):
        # Update existing record (prepend last 2 chapters)
        chapter_collection.update_one(
            {"manga_url": record['manga_url']},
            {"$push": {"latest_chapters": {"$each": new_chapters, "$position": 0}}}
        )
    else:
        # Insert new record with the last two latest chapters
        chapter_collection.insert_one({
            "manga_title": record["manga_title"],
            "manga_site": record["manga_site"],
            "manga_url": record['manga_url'],
            "manga_image": record["manga_image"],
            "en_manga_image": record["en_manga_image"],
            "manga_rating": record["manga_rating"],
            "manga_genre": record["manga_genre"],
            "manga_type": record["manga_type"],
            "manga_release": record["manga_release"],
            "manga_status": record["manga_status"],
            "latest_chapters": new_chapters[:2]
        })

