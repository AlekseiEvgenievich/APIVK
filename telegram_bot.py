import telegram
import os

bot = telegram.Bot(token='6582158196:AAFIuq5HWmLBxrWvjrpQ_VgT4xRM72NUrKs')
#print(bot.get_me())
updates = bot.get_updates()
print(updates)
#bot.send_message(text='Hi Johnssss!', chat_id='@python_memes_from_me')
#bot.send_document(chat_id='@python_memes_from_me', document=open('./xc.png', 'rb'))
for path, directories, files in os.walk("./images/"):
    print(files)
