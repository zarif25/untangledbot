import logging
from os import getenv

import requests

from imgbb import upload_story_to_imgbb
from provider import Story

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


class GraphAPI:
    def __init__(self, PAGE_ID: int, ACCESS_TOKEN: str) -> None:
        self.__ACCESS_TOKEN = ACCESS_TOKEN
        self.__url = f'https://graph.facebook.com/{PAGE_ID}/photos'

    def post_img(self, message: str, img_url: str) -> str:
        '''Post image with a message in Facebook

        Args:
            message: message in the Facebook post
            img_url: image of the Facebook post (jpg/png/others)
        Returns:
            id of the post

        '''
        payload = {
            'message': message,
            'url': img_url,
            'access_token': self.__ACCESS_TOKEN
        }
        res = requests.post(self.__url, data=payload).json()
        try:
            return res['id']
        except Exception:
            logging.error(res)
            logging.error("Couldn't post to FB")


PAGE_ID = getenv("PAGEID")
logging.info(f"PAGE_ID: {PAGE_ID}")
ACCESS_TOKEN = getenv("FBTOKEN")
logging.info(f"ACCESS_TOKEN: {ACCESS_TOKEN}")

fb_api = GraphAPI(PAGE_ID, ACCESS_TOKEN)


def post_story_to_fb(story: Story):

    message = f"{story.title}\n\n{story.details}\n\nRead more: {story.url}"
    img_url = upload_story_to_imgbb(story)

    logging.info(f"Posting {story} to fb")
    res = fb_api.post_img(message, img_url)
    logging.info(f"Posted {story} to fb. Post ID is {res}")