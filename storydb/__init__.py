import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from providers import Story


class DBStory(Story):
    def __init__(self, record):
        provider_name = record[1]
        self.__record = record
        lang = record[10]
        super().__init__(provider_name, lang=lang)

    def get_title(self): return self.__record[2]
    def get_summary(self): return self.__record[3]
    def get_dtime(self): return datetime.fromisoformat(self.__record[4])
    def get_topic(self): return self.__record[5]
    def get_source(self): return self.__record[6]
    def get_base_url(self): return self.__record[7]
    def get_display_url(self): return self.__record[8]
    def get_img_url(self): return self.__record[9]


__BASE_DIR = Path(__file__).parent

conn = sqlite3.connect(__BASE_DIR/'stories.db')
c = conn.cursor()


def __create_table():
    c.execute('''CREATE TABLE STORIES (
        ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        PROVIDER_NAME   TEXT,
        TITLE           TEXT,
        SUMMARY         TEXT,
        DTIME           TEXT,
        TOPIC           TEXT,
        SOURCE          TEXT,
        BASE_URL        TEXT,
        DISPLAY_URL     TEXT,
        IMG_URL         TEXT,
        LANG            TEXT
    );''')


def insert(story: Story):
    """Inserts story to db"""
    if not story.is_complete():
        print("The story was not uploaded to the database because it was incomplete")
        return
    with conn:
        c.execute(
            """INSERT INTO STORIES (
                PROVIDER_NAME,
                TITLE,
                SUMMARY,
                DTIME,
                TOPIC,
                SOURCE,
                BASE_URL,
                DISPLAY_URL,
                IMG_URL,
                LANG
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                story.provider_name,
                story.title,
                story.summary,
                story.dtime,
                story.topic,
                story.source,
                story.base_url,
                story.display_url,
                story.img_url,
                story.lang
            )
        )


def insert_all(stories):
    """Inserts all the stories to db"""
    for story in stories:
        insert(story)


def get_all() -> list[Story]:
    """
    Returns:
        All the stories from db
    """
    c.execute("SELECT * FROM STORIES")
    records = c.fetchall()
    return [DBStory(record) for record in records]


def exact_same_exists(story: Story):
    """
    Returns:
        True if a story exactly same as the input story exists in the db, else False
    """
    for story2 in get_all():
        if story.is_exactly_same(story2):
            return True
    return False


def similar_exists(story: Story) -> Story:
    """
    Returns:
        A story similar to the input story if it exists in the db, else None
    - Can be used as boolean for checking if a similar story exists
    """
    for story2 in get_all():
        if story == story2:
            return story2


def __drop_table():
    with conn:
        c.execute("DROP TABLE STORIES;")


def __delete_all():
    """Deletes all stories in the db"""
    with conn:
        c.execute("DELETE FROM STORIES;")


def delete_old_stories(days: int):
    """Deletes stories that are older than days(args)"""
    stories = get_all()
    not_old_stories = [story for story in stories if story.dtime >
                       datetime.today() - timedelta(days=days)]
    __delete_all()
    insert_all(not_old_stories)
