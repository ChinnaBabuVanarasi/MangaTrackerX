import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(filename):
    if "chapter" in filename:
        filename = f"Chapters/{filename}"
        name = filename.split("/")[1].split("_logger")[0]
    else:
        filename = filename
        name = filename.split("_logger")[0]
    try:
        log_directory = os.path.join(Path(os.getcwd()).parent.parent.resolve(), 'logs')
    except FileNotFoundError:
        log_directory = r"C:\\Users\\chinn\\PycharmProjects\\MangaTrackerX\\logs"
    log_file_name = str(os.path.join(f"{log_directory}/{filename}",
                                     f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"))
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)

    # Create a log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
