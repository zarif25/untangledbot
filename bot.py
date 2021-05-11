import os
import time
from logger import log_warning, log_info, logs
from scrapper import Provider
from image_manip import create_template
from imgbb import upload_to_imgbb
from fb import post_to_fb
from news_hash import url_to_hash
from utils import get_theme
from discord.ext import commands

client = commands.Bot(command_prefix=".")

@client.command()
async def info():
    channel = client.get_channel(841727986351865896)
    await channel.send('\n'.join(logs['I']))

@client.command()
async def warning():
    channel = client.get_channel(841728105886253106)
    await channel.send('\n'.join(logs['W']))

@client.command()
async def error():
    channel = client.get_channel(841732573411672104)
    await channel.send('\n'.join(logs['E']))

key = os.getenv('DISKEY')

client.run(key)

while True:
    stories = Provider('http://bdnews24.com/').scrape_latest_stories()
    stories += Provider('https://www.dhakatribune.com/').scrape_latest_stories()
    theme = get_theme()

    for story in stories:
        story.scrape()
        title, description, src, date, img, src_url = story.get_all()
        post = create_template(title, description, src, date, img, theme)
        if post == None:
            log_warning("problem in one of the parameters of this story", story.url)
            continue
        img_path = f'posts\\{url_to_hash(story.url)}.PNG'
        post.save(img_path)
        imgbb_url = upload_to_imgbb(img_path)
        if src_url != None:
            description += f"\nSource: {src_url}"
        post_to_fb(imgbb_url, description)
        os.remove(img_path)

    log_info("done")
    for i in range(6):
        log_info("NEXT UPDATE", f"after {30-i*5}min")
        time.sleep(300)
