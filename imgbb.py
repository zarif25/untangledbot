import base64
import logging
from os import getenv
import time

import requests

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

key = getenv("IMGBBKEY")
logging.info(f"IMGBBKEY: {key}")

def upload_story_to_imgbb(story):
    '''
    Uploads story image to imgbb

    Args:
        story: story to upload

    Returns:
        url of the uploaded image
    '''
    story_img = story.get_story_img()
    story_img.save_as('temp.PNG')
    time.sleep(2)
    with open('temp.PNG', "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        image = base64.b64encode(file.read())
        payload = {
            "key": key,
            "image": image,
            "expiration": 600
        }
        logging.info(f"Uploading {story} to imgbb")
        res = requests.post(url, payload)
        try:
            uploaded_url = res.json()['data']['url']
            logging.info(f"Uploaded {story} to imgbb. URL is {uploaded_url}")
            return uploaded_url
        except Exception as e:
            logging.error(res.json())
            logging.error("Could not upload image because " + str(e))
