from provider import Story
import requests
from datetime import datetime
import base64
from PIL import Image
import urllib

url = "https://www.untangled.news/wp-json/wp/v2"
username = "untangled"
password = "44lq TNn3 QmGK vCfe RKsx ZpPA"
creed = username + ":" + password
token = base64.b64encode(creed.encode())
header = {'Authorization': 'Basic ' + token.decode('utf-8')}


def post_story_to_wp(story: Story):
    has_image = True
    try:
        urllib.request.urlretrieve(story.img_url, "temp.PNG")
        media = {
            'file': open('temp.PNG', 'rb'),
            'caption': story.title,
            'description': story.details
        }
        image = requests.post(url + '/media', headers=header, files=media)
        img_id = image.json()['id']
    except Exception:
        has_image = False
    post = {
        'date': story.datetime.strftime("%Y-%m-%d") + 'T' + datetime.now().strftime("%H:%M:%S"),
        'title': story.title,
        'content': f'''
        {story.details}<br>
        Read more: <a href="{story.url}">{story.src.split(',')[-1]}</a>
        ''',
        'status': 'publish',
    }
    if has_image:
        post['featured_media'] = img_id,
    r = requests.post(url+'/posts', headers=header, json=post)