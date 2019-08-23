from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time
import os
import random
import requests
import telepot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = open('config/token.conf', 'r').read().replace("\n", "")
message_list = os.listdir("message")

bot = telepot.Bot(TOKEN)

if not os.path.exists("logs"):
    os.makedirs("logs")

user_list = []
new_user = ""

def welcome(bot, update):
    global new_user
    print(update.message)
    for new_user_obj in update.message.new_chat_members:
        if update.message.from_user.id in user_list:
            user_list.remove(update.message.from_user.id)
        url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
        headers = {"Content-type": "application/json"}
        params = '{"chat_id": "@hcxpaycoin", "text": "Welcome! Please input one word below if you are not a bot.\n 1. First \n 2. Second \n 3. Third \n 4. Fourth"}'
        r = requests.post(url, headers = headers, data = params)
        print(r)

        open("logs/logs_" + time.strftime('%d_%m_%Y') + ".txt","w").write("\nupdate status: " + str(update))
        chat_id = update.message.chat.id
        # new_user = ""
        message_rnd = random.choice(message_list)
        WELCOME_MESSAGE = open('message/' + message_rnd , 'r').read().replace("\n", "")

        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            print(e)
            new_user = new_user_obj['first_name']
        print(new_user, message_rnd)
        bot.sendMessage(chat_id=chat_id, text=WELCOME_MESSAGE.replace("{{username}}",str(new_user)), parse_mode='HTML')

def get_message(bot, update):
    global new_user
    print(99999,update.message)
    print(66666, user_list)
    text = update.message.text
    if update.message.from_user.id not in user_list:   
        if text == 'First' or text == 'Second' or text == 'Third' or text == 'Fourth':
            bot.sendMessage(chat_id=update.message.chat_id, text=new_user + " joined successfully")
            user_list.append(update.message.from_user.id)
            print("id1: ", update.message.from_user.id)
        else:
            print("remove id: ", update.message.from_user.id)
            user_list.remove(update.message.from_user.id)
            bot.kickChatMember(update.message.chat_id, update.message.from_user.id)
    # else:
    #     bot.sendMessage(chat_id=update.message.chat_id, text="Hello")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    open("logs/error.txt","w").write("\nupdate status: " + str(update) + "\nerror: " + str(error))

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text, get_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
