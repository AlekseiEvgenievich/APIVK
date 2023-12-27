import os
import random

import requests
from dotenv import load_dotenv
from telegram import Bot


def download_image(url, name_path='images/comic.png'):
    response = requests.get(url)
    response.raise_for_status()
    with open(name_path, 'wb') as file:
        file.write(response.content)
        
        
def send_on_telegram(bot_token, folder_name, channel_name, funny_comment):
    max_file_size = 20 * 1024 * 1024
    bot = Bot(token=bot_token)
    for dirpath, dirnames, filenames in os.walk(folder_name):
        for file_name in filenames:
            file_path = '{}/{}'.format(folder_name, file_name)
            if os.path.getsize(file_path) <= max_file_size:
                with open(f'{folder_name}/{file_name}', 'rb') as photo_file:
                    bot.send_photo(chat_id=channel_name, photo=photo_file)
                    bot.send_message(chat_id=channel_name, text=funny_comment)
            os.remove(file_path)
                

def get_random_number_of_comics():
    current_url = 'https://xkcd.com/info.0.json'
    response = requests.get(current_url)
    response.raise_for_status()
    max_number_photo = int(response.json()['num'])
    random_number = random.randint(0, max_number_photo)
    return random_number


def get_image_link(number_of_comics):
    comics_url = f'https://xkcd.com/{number_of_comics}/info.0.json'
    response = requests.get(comics_url)
    response.raise_for_status()
    return response.json()['img']
    
    
def get_funny_comment(number_of_comics):
    comics_url = f'https://xkcd.com/{number_of_comics}/info.0.json'
    response = requests.get(comics_url)
    response.raise_for_status()
    return response.json()['alt']


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    folder_name = os.environ["IMAGE_NAME_FOLDER"]
    channel_name = os.environ["TELEGRAM_CHANNEL_NAME"]
    
    random_number_of_comic = get_random_number_of_comics()
    download_image(get_image_link(random_number_of_comic))
    funny_comment = get_funny_comment(random_number_of_comic)
    send_on_telegram(bot_token, folder_name, channel_name, funny_comment)
