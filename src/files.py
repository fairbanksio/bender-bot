import datetime
import os
import requests

from log_config import logger


# Save a remote file to local disk
def save_file(file_url, file_name):
    """
    Downloads a file from a url

    Args:
        file_url (str): remote file url

    Returns:
        A string containing path to locally saved file
    """

    try:
        # Generate file path with timestamp & current working directory
        file_path = os.path.join(
            os.getcwd(), f'{datetime.datetime.utcnow().strftime("%s")}-{file_name}'
        )

        # Download and save data from the remote source
        response = requests.get(file_url)
        response.raise_for_status()
        with open(file_path, "wb") as handler:
            handler.write(response.content)

        logger.debug(f"💾 File saved: {file_path}\n")

    except Exception as e:
        # Handle any exceptions that arise during image generation.
        logger.error(f"⛔ Error saving file: {e}\n")
        return None

    return file_path


def open_file(file_path):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            return contents
    except Exception as e:
        logger.error(f"⛔ Error opening file: {e}\n")


def delete_file(file_path):
    try:
        os.remove(file_path)
        return True

    except FileNotFoundError:
        logger.error(f"🤷 Could not find file: {e}\n")
        return False

    except Exception as e:
        # Handle any exceptions that arise during image generation.
        logger.error(f"⛔ Error deleting file: {e}\n")
        return False
