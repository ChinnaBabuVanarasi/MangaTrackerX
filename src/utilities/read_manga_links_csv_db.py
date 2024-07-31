import pandas as pd

from src.utilities.database_connection import get_collection
from src.utilities.page_source import get_date_added


def get_links(filepath=None, use_db=False, collection_name="get_csv_links"):
    """Fetches manga links and dates from either a CSV file or the database.

    Args:
        filepath (str, optional): Path to the CSV file. Required if `use_db` is False.
        use_db (bool, optional): If True, fetches links from the database. Defaults to False.
        collection_name(str,optional): collection name, get from calling functions.Defaults to "get_csv_links"

    Returns:
        list: A list of dictionaries containing manga URLs and dates.
    """
    if use_db:
        csv_collection = get_collection(collection_name)
        return list(csv_collection.find({}, {"manga_url": True, "_id": False}))
    elif filepath:
        df = pd.read_csv(filepath)
        today = get_date_added()
        return [{"manga_url": row["links"], "date_added": today} for _, row in df.iterrows()]
    else:
        raise ValueError("Either filepath or use_db must be provided.")


def get_summary_content(soup):
    default_values = {'rating': 'N/A', 'release': 'N/A'}  # You can customize defaults here
    heading = soup.find_all('div', class_='summary-heading')
    dic = {
        header.text.strip(): header.find_next('div', class_='summary-content').text.strip()
        for header in heading
    }
    # Extract rating with error handling
    manga_rating = ''
    if 'Rating' in dic:
        try:
            manga_rating = dic['Rating'].split('/')[0].split('Average')[1].strip()
        except IndexError:
            pass  # Handle potential errors in rating format
    # Extract other details with defaults
    manga_details = {
        'rating': manga_rating,
        **{key.lower(): dic.get(key, default_values.get(key, '')) for key in
           ['Genre(s)', 'Type', 'Release', 'Status']}
    }
    return manga_details
