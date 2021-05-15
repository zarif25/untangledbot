import os
import time
from logger import log_error, log_warning, log_info
from scrapper import Provider
from image_manip import create_template
from imgbb import upload_to_imgbb
from fb import post_to_fb
from news_hash import url_to_hash, previous_hashes
from utils import get_theme

provider1 = Provider('http://bdnews24.com/')
provider2 = Provider('https://www.dhakatribune.com/')

while True:
    stories = provider1.get_latest_stories() + provider2.get_latest_stories()
    theme = get_theme()

    for story in stories:
        story.scrape()
        title, description, src, date, img, src_url = story.get_all()
        try:
            post = create_template(title, description, src, date, img, theme)
        except Exception as e:
            log_warning("problem creating post", e)
            continue
        img_path = f'posts\\{url_to_hash(story.url)}.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        if src_url != None:
            description += f"\nSource: {src_url}"
        post_to_fb(imgbb_url, description)
        try:
            os.remove(img_path)
        except Exception as e:
            log_error("problem deleting file", e)

    log_info("done", sep="")
    for i in range(4):
        log_info("NEXT UPDATE", f"after {20-i*5}min")
        log_info("previous hashes", previous_hashes)
        time.sleep(300)
