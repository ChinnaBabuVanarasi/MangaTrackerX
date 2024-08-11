import logging
import os
from datetime import datetime
from logging import getLogger, FileHandler, Formatter
from pathlib import Path


def setup_logging(filename, log_level=logging.DEBUG, default_log_dir="data_ingestion_logs"):
    """
    Sets up a logger with a dedicated log file and folder based on the provided filename.

    Args:
        filename (str): The name of the logger and the base name of the log file.
                           May optionally contain a subdirectory structure separated by '/'.
        log_level (int, optional): The logging level (e.g., logging.DEBUG, logging.INFO).
                                   Defaults to logging.INFO.
        default_log_dir (str, optional): The default directory to create data_ingestion_logs in.
                                          Defaults to "data_ingestion_logs" within the parent directory of the current working directory.

    Returns:
        logging.Logger: The created logger instance.
    """
    # Determine log directory based on filename structure and user preference
    try:
        # Up two levels from current working directory
        log_directory = os.path.join(Path(os.getcwd()).resolve().parent.parent, default_log_dir)

    except FileNotFoundError:
        log_directory = r"D:\PythonProjects\MangaTrackerX\data_ingestion_logs"

    log_file_name = os.path.join(
        f"{log_directory}/{filename}",
        f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    )

    # Create logger directory if it doesn't exist, ignoring potential errors if it already does
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    #
    # Create the logger instance
    logger = getLogger(filename)
    logger.setLevel(log_level)

    # Create a file handler with the specified log level and formatter
    file_handler = FileHandler(log_file_name)
    file_handler.setLevel(log_level)
    formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
