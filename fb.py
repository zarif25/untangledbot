import requests
from logger import log_error, log_warning, log_info
from os import getenv

page_id = 104173088514235
access_token = getenv("FBTOKEN")


def post_to_fb(img_url, title, description, src_url):
    payload = {
        'message': f"{title}\n{description}\nRead more: {src_url}",
        'url': img_url,
        'access_token': access_token
    }

    r = requests.post(f'https://graph.facebook.com/{page_id}/photos',
                      data=payload)
    log_info("uploaded", f"to fb | {r.json()}")
