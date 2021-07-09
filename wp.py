import base64
from datetime import datetime

import requests

from providers import Story


class WordpressApi:

    __MAP_CATEGORY_TO_ID = {
        "Bangladesh": 13,
        "World": 14,
        "Business": 15,
        "Sports": 16,
        "Entertainment": 17,
        "Education": 18,
        "Technology": 19,
        "Health": 20,
    }

    def __init__(self, URL, USERNAME, PASSWORD) -> None:
        self.__URL = URL
        self.__CREED = USERNAME + ':' + PASSWORD
        self.__TOKEN = base64.b64encode(self.__CREED.encode())
        self.__HEADER = {'Authorization': 'Basic ' +
                         self.__TOKEN.decode('utf-8')}

    # FIXME: handle exceptions: use a wpuploaderror exception
    def post_story(self, story: Story, image_path):
        print("uploading to wordpress", story)
        with open(image_path, 'rb') as image_file:
            media = {
                'file': image_file,
                'caption': story.title,
                'description': story.summary
            }
            image = requests.post(self.__URL + '/media',
                                  headers=self.__HEADER, files=media)
        img_id = image.json()['id']
        categories = [self.__MAP_CATEGORY_TO_ID.get(story.topic, 21)]
        post = {
            'date': story.dtime.strftime("%Y-%m-%d") + 'T' + datetime.now().strftime("%H:%M:%S"),
            'title': story.title,
            'featured_media': img_id,
            'content': f'''
            {story.summary}<br>
            Read more: <a href="{story.display_url}">{story.source}</a>
            ''',
            'status': 'publish',
            'categories': categories
        }
        requests.post(self.__URL+'/posts',
                          headers=self.__HEADER, json=post)
