import os
import telebot

from parser import Parser
from loader import Connector

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()


@bot.message_handler(func=lambda message: True, commands=['firstnews', 'lastnews', 'listnews'])
def update_news_list(message):
    urls = parser.get_detailed()
    objs = [parser.follow(u) for u in urls]
    print(objs)
    connector.insert(objs)
    command = message.html_text
    if command == '/firstnews':
        payload = f"Title: {objs[-1]['title']}\nDate: {objs[-1]['date']}\nUrl: {objs[-1]['url']}\n"
    elif command == '/lastnews':
        payload = f"Title: {objs[0]['title']}\nDate: {objs[0]['date']}\nUrl: {objs[0]['url']}\n"
    elif command == '/listnews':
        payload = '\n\n'.join(['\n'.join([str(obj['date']), obj['title']]) for obj in objs])
    else:
        payload = 'wtf??'
    bot.send_message(message.chat.id, payload)



if __name__ == '__main__':
    connector = Connector()
    parser = Parser()
    bot.polling(none_stop=True)