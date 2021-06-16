import logging
from utils import sleep_with_reminder
from wordpress import post_story_to_wp
import story_db
from fb import post_story_to_fb
from provider import Bdnews24, DHKTribune, DStar, Story, TBSNews
from constants import SLEEP_TIME, REMIND_AFTER
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

hours_passed = 0

while True:
    stories: list[Story] = []
    for provider in [Bdnews24, DHKTribune, DStar, TBSNews]:
        stories.extend(provider().get_stories())

    previous_stories = story_db.get_all_stories()

    for story in stories:
        if story not in previous_stories:
            story_db.insert_story(story)
            previous_stories.append(story)
            logging.info(f"Working on new story: {story}")
            # post_story_to_fb(story)
            try:
                post_story_to_wp(story)
            except Exception:
                pass
        else:
            logging.info(f"Skipping old story: {story}")
    sleep_with_reminder(SLEEP_TIME * 60, REMIND_AFTER * 60)
    hours_passed += SLEEP_TIME / 60
    if hours_passed >= 24:
        story_db.delete_old_stories()
        hours_passed = 0
