import time
from provider import Bdnews24, DHKTribune, DStar, TBSNews
import story_db

sleep_time = 30  # minutes
hours_passed = 0

while True:
    stories = []
    for provider in Bdnews24, DHKTribune, DStar, TBSNews:
        stories.extend(provider().get_stories())

    previous_stories = story_db.get_all_stories()

    for story in stories:
        if story not in previous_stories:
            story_db.insert_story(story)
            previous_stories.append(story)
            # story.save_story_image()
            print(f"new story: {story}")  # debug
            story.upload_to_fb()
        else:
            print(f"old story: {story}")  # debug
    time.sleep(sleep_time * 60)
    hours_passed += 0.5
    if hours_passed >= 24:
        story_db.delete_old_stories()
        hours_passed = 0
