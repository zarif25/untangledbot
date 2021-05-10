import os
import time
from scrapper import Provider
from image_manip import create_template
from imgbb import upload_to_imgbb
from fb import post_to_fb
from news_hash import update_hash, get_prev_hash, url_to_hash

while True:
    stories = Provider('http://bdnews24.com/').scrape_stories()
    theme = 'light' if 3 <= time.localtime().tm_hour <= 18 else 'dark'

    # hashing
    latest_hash = url_to_hash(stories[0].url)
    print('latest_hash:', latest_hash)
    previous_hash = get_prev_hash()
    print('previous_hash: ', previous_hash)

    for story in stories:
        current_hash = url_to_hash(story.url)
        if (current_hash == previous_hash):
            break
        title, sub_title, src, date, img = story.get_all()
        post = create_template(title, sub_title, src, date, img, theme)
        img_path = 'posts\\' + current_hash + '.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        print(imgbb_url)

        post_to_fb(imgbb_url, sub_title)

        os.remove(img_path)
    
    update_hash(latest_hash)
    print("done")
    time.sleep(1800)
