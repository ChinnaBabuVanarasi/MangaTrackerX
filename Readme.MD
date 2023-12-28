# MangaTrackerX
----
## App to extract and track latest chapters of listed Manga links and redirect to their source website.

## MongoDB Collections
----
### MangaLinks Keys
- Manga_url
- Title
- Site
- Date_added

## MangaDetails Keys
- Manga_url
- Title
- Binary_Image
- Image
- Date_added

## MangaChapters Keys
- Manga_url
- Title
- Binary_Image
- Image
- Latest_chapters[{Chapter_name, Chapter_url}]
- Date_added
