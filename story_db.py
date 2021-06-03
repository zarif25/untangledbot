import sqlite3
from datetime import datetime, timedelta

from provider import Story

conn = sqlite3.connect('stories.db')
c = conn.cursor()


def __create_table():
    c.execute('''CREATE TABLE STORIES (
        ID      INTEGER PRIMARY KEY AUTOINCREMENT,
        TITLE   TEXT,
        URL     TEXT,
        DATE    TEXT
    );''')


def insert_story(story: Story):
    with conn:
        c.execute("INSERT INTO STORIES (TITLE, URL, DATE) VALUES (?, ?, ?)",
                  (story.title, story.url, story.datetime.strftime("%A, %b %d, %Y")))


def insert_stories(stories):
    for story in stories:
        insert_story(story)


def get_all_stories():
    c.execute("SELECT * FROM STORIES")
    records = c.fetchall()
    return [Story(
        title=record[1],
        url=record[2],
        datetime=datetime.strptime(record[3], "%A, %b %d, %Y")
    ) for record in records]


def __drop_table():
    with conn:
        c.execute("DROP TABLE STORIES;")


def __delete_all_stories():
    with conn:
        c.execute("DELETE FROM STORIES;")


def delete_old_stories():
    stories = get_all_stories()
    not_old_stories = [story for story in stories if story.datetime <
                       datetime.today() - timedelta(days=7)]
    __delete_all_stories()
    insert_stories(not_old_stories)


if __name__ == '__main__':
    __drop_table()
    __create_table()