import requests
from log_config import logger
import time
import datetime
import os



# Save a remote file to local disk
def save_file(file_url,file_name):
    """
    Downloads a file from a url

    Args:
        file_url (str): remote file url

    Returns:
        A string containing path to locally saved file
    """

    try:
        # get unix timestamp
        time_now = datetime.datetime.utcnow()
        timestamp_now = time_now.strftime("%s")

        # generate tmp file with timestamp
        file_name = timestamp_now + '-' + file_name

        # generate relative path based on current running location + generated file name
        file_path = os.path.join(os.getcwd(), file_name)

        # get data from remote source
        file_data = requests.get(file_url).content

        # save file locally
        with open(file_path, 'wb') as handler:
            handler.write(file_data)

    except Exception as e:
        # Handle any exceptions that arise during image generation.
        logger.error(f"Error saving image: {e}\n")
        return None

    return file_path

def delete_file(file_path):
    try:
        os.remove(file_path)
        return True

    except FileNotFoundError:
        logger.error(f"Could not find file to delete: {e}\n")
        return False

    except Exception as e:
        # Handle any exceptions that arise during image generation.
        logger.error(f"Error deleting file: {e}\n")
        return False
