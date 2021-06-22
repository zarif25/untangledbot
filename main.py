import os
import shutil
import traceback
from os import getenv
from time import sleep

import requests
from PIL import UnidentifiedImageError

import storydb
from discord_webhook import log_error_to_discord
from fb import FacebookApi, FbUploadError
from imgbb import ImgbbApi, ImgbbUploadError
from providers.bdnews24 import Bdnews24
from providers.bntribune import BnTribune
from providers.dhktribune import DHKTribune
from providers.dstar import DStar
from providers.ittefaq import Ittefaq
from providers.tbs import TBS
from storyimage import ImageCreator
from wp import WordpressApi

PAGE_ID = getenv("PAGEID")
ACCESS_TOKEN = getenv("FBTOKEN")
fb_api = FacebookApi(PAGE_ID, ACCESS_TOKEN)

KEY = getenv("IMGBBKEY")
imgbb_api = ImgbbApi(KEY)

USERNAME = getenv("WP_USERNAME")
PASSWORD = getenv("WP_PW")
WP_URL_EN = getenv("WP_URL")
WP_URL_BN = getenv("WP_URL_BN")
wp_api_en = WordpressApi(WP_URL_EN, USERNAME, PASSWORD)
wp_api_bn = WordpressApi(WP_URL_BN, USERNAME, PASSWORD)


def save_image_from_url_as(url: str) -> str:
    """saves the image and returns the file name. Yeah it makes sure that the file is created even if it can't download the image"""
    filename = url.split('?')[0].split('/')[-1]
    with open(filename, 'wb') as temp_image_file:
        with requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'}) as response:
            if response.status_code == 200:
                response.raw.decode_content = True
            shutil.copyfileobj(response.raw, temp_image_file)
    return filename

hours_passed = 0
while True:
    for provider in (Bdnews24, TBS, DStar, BnTribune, DHKTribune, Ittefaq):
        print(f"Extracting stories from {provider}")
        try:
            new_stories = provider().get_stories()
            for story in new_stories:
                try:
                    if not story.is_complete():
                        continue
                    if storydb.exact_same_exists(story):
                        continue
                    if not storydb.similar_exists(story):
                        temp_image_path = save_image_from_url_as(story.img_url)
                        try:
                            temp_story_image_path = "temp_story_image.PNG"
                            ImageCreator.from_story(story, temp_image_path).get_image().save(temp_story_image_path)
                        except UnidentifiedImageError as e:
                            log_error_to_discord(story.img_url)
                            raise e
                        try:
                            if story.lang == 'en':
                                wp_api_en.post_story(story, temp_image_path)
                            else:
                                wp_api_bn.post_story(story, temp_image_path)
                            story_image_url = imgbb_api.upload_image(temp_story_image_path)
                            fb_caption = f"{story.title}\n\n{story.summary}\nRead more: {story.display_url}\n\nTopic: #{story.topic}"
                            fb_api.post_image(fb_caption, story_image_url)
                        except (FbUploadError, ImgbbUploadError) as e:
                            print(e)
                        finally:
                            os.remove(temp_image_path)
                            os.remove(temp_story_image_path)
                except Exception as e:
                    log_error_to_discord(f"Something went wrong while uploading this story:\n{story.base_url}\n" + str(traceback.format_exc()))
                storydb.insert(story)
        except Exception as e:
            log_error_to_discord("Something went wrong:" + str(traceback.format_exc()))
    print("Gonna take a nap for 30mins. 😴")
    sleep(1600)
    hours_passed += 0.5
    if hours_passed >= 24:
        storydb.delete_old_stories(3)
        hours_passed = 0


"""
TODO:
1. dont repeat sources in discord
"""