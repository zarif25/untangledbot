import os
import time
import textwrap
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
        if None in [title, sub_title, src, date, img]:
            print(f"Error: problem in one of the parameters of this story: {story.url}")
            continue
        src = '<debugging>'
        title_wraped = textwrap.wrap(title, width=38)
        sub_title_wraped = textwrap.wrap(sub_title, width=48)
        if len(sub_title_wraped) > 8:
            sub_title_wraped = sub_title_wraped[:8]
            i = 7
            while i > 0:
                if '.' in sub_title_wraped[i]:
                    sub_title_wraped[i] = sub_title_wraped[i].split('.')[
                        0] + "."
                    break
                else:
                    del sub_title_wraped[i]
                i -= 1
        post = create_template(
            title_wraped, sub_title_wraped, src, date, img, theme)
        img_path = 'posts\\' + current_hash + '.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        print(imgbb_url)
        post_to_fb(imgbb_url, sub_title)
        os.remove(img_path)

    update_hash(latest_hash)
    print("done")
    for i in range(6):
        print(f"next update in {30-i*5}min")
        time.sleep(300)
