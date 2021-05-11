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
    t_hour = (time.localtime().tm_hour + 6) % 24
    theme = 'light' if 3 <= t_hour <= 18 else 'dark'

    # hashing
    latest_hash = url_to_hash(stories[0].url)
    print('LATEST HASH:', latest_hash)
    previous_hash = get_prev_hash()
    print('PREVIOUS HASH:', previous_hash)

    for story in stories:
        current_hash = url_to_hash(story.url)
        if (current_hash == previous_hash):
            break
        title, description, src, date, img = story.get_all()
        if None in [title, description, src, date, img]:
            print(f"Error: problem in one of the parameters of this story: {story.url}")
            continue
        title_wraped = textwrap.wrap(title, width=38)
        description_wraped = textwrap.wrap(description, width=48)
        if len(description_wraped) > 7:
            description_wraped = description_wraped[:7]
            i = 6
            while i > 0:
                if '.' in description_wraped[i]:
                    description_wraped[i] = description_wraped[i].split('.')[
                        0] + "."
                    break
                else:
                    del description_wraped[i]
                i -= 1
        post = create_template(
            title_wraped, description_wraped, src, date, img, theme)
        img_path = 'posts\\' + current_hash + '.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        post_to_fb(imgbb_url, description)
        os.remove(img_path)

    update_hash(latest_hash)
    print("done")
    for i in range(6):
        print(f"next update in {30-i*5}min")
        time.sleep(300)
