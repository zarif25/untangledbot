import os
import time
from logger import log_error, log_warning, log_info
from scrapper import Provider
from image_manip import create_template
from imgbb import upload_to_imgbb
from fb import post_to_fb
from utils import get_theme

provider1 = Provider('http://bdnews24.com/')
provider2 = Provider('https://www.dhakatribune.com/')

while True:
    stories = provider1.get_latest_stories() + provider2.get_latest_stories()
    theme = get_theme()

    for story in stories:
        story.scrape()
        if story.not_valid():
            continue
        title, description, src, date, img, src_url = story.get_all()
        try:
            post = create_template(title, description, src, date, img, theme)
        except Exception as e:
            log_warning("problem creating post", e)
            continue
        img_path = f'posts\\{story.hash}.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        post_to_fb(imgbb_url, description, src_url)
        try:
            os.remove(img_path)
        except Exception as e:
            log_error("problem deleting file", e)

    log_info("done", sep="")
    log_info("previous hashes", Provider.prev_hashes)
    for i in range(4):
        log_info("NEXT UPDATE", f"after {20-i*5}min")
        time.sleep(300)
