import os
import time
from logger import log_warning, log_info
from scrapper import Provider
from image_manip import create_template
from imgbb import upload_to_imgbb
from fb import post_to_fb
from news_hash import update_hash, get_prev_hash, url_to_hash

while True:
    stories = Provider('http://bdnews24.com/').scrape_stories()
    t_hour = (time.localtime().tm_hour + 6) % 24
    theme = 'light' if 3 <= t_hour <= 18 else 'dark'

    # hashing
    latest_hash = url_to_hash(stories[0].url)
    log_info('latest hash', latest_hash)
    previous_hash = get_prev_hash()
    log_info('previous hash', previous_hash)

    for story in stories:
        current_hash = url_to_hash(story.url)
        if (current_hash == previous_hash): break
        story.scrape()
        title, description, src, date, img = story.get_all()
        post = create_template(title, description, src, date, img, theme)
        if post == None:
            log_warning("problem in one of the parameters of this story", story.url)
            continue
        img_path = 'posts\\' + current_hash + '.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        post_to_fb(imgbb_url, description)
        os.remove(img_path)

    update_hash(latest_hash)
    log_info("done")
    for i in range(6):
        log_info("NEXT UPDATE", f"after {30-i*5}min")
        time.sleep(300)
