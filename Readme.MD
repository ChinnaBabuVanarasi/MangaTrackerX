# MangaTrackerX
----
## App to extract and track latest chapters of listed Manga links and redirect to their source website.

## MongoDB Collections
----
### csv_links
- manga_url
- Date_added

## manga_metadata
- manga_title
- manga_site
- manga_url
- manga_image
- en_manga_image
- manga_rating
- manga_genre
- manga_type
- manga_release
- manga_status
- date_added

## manga_chapters
- manga_title
- manga_site
- manga_url
- manga_image
- en_manga_image
- manga_rating
- manga_genre
- manga_type
- manga_release
- manga_status
- latest_chapters[
    {
      chapter_num,
      chapter_url,
      chapter_added,
    }
  ]
