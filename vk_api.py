import os
import random
from pathlib import Path

import requests
from dotenv import load_dotenv
from telegram import Bot


def send_on_telegram(bot_token, outpath, channel_name, funny_comment):
    max_file_size = 20 * 1024 * 1024
    bot = Bot(token=bot_token)
    if os.path.getsize(outpath) <= max_file_size:
        with open(outpath, 'rb') as photo_file:
            bot.send_photo(chat_id=channel_name, photo=photo_file)
            bot.send_message(chat_id=channel_name, text=funny_comment)


def download_random_comic(folder_name):
    current_url = 'https://xkcd.com/info.0.json'
    current_response = requests.get(current_url)
    current_response.raise_for_status()
    max_photo_number = int(current_response.json()['num'])
    random_number = random.randint(0, max_photo_number)
    comics_url = f'https://xkcd.com/{random_number}/info.0.json'
    comics_response = requests.get(comics_url)
    comics_response.raise_for_status()
    image_response = requests.get(comics_response.json()['img'])
    image_response.raise_for_status()
    file_name = f'xcd_{random_number}'
    outpath = Path.cwd() / folder_name / file_name
    with open(outpath, 'wb') as file:
        file.write(image_response.content)
    return outpath, comics_response.json()['alt']


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    folder_name = os.environ["IMAGE_NAME_FOLDER"]
    channel_name = os.environ["TELEGRAM_CHANNEL_NAME"]
    
    outpath,funny_comment = download_random_comic(folder_name)
    try:
        send_on_telegram(bot_token, outpath, channel_name, funny_comment)
    finally:
        os.remove(outpath)
