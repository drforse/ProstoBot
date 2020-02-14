import telebot
from telebot import types
from pymongo import MongoClient
import os

client = MongoClient(os.environ["MongoDB"])
db = client.main
coll = db.prikol

bot=telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет! Подробно в /help")

@bot.message_handler(commands=['help'])
def start_message(message):
  bot.send_message(message.chat.id,"Команды:\n/rules - Правила чата.")

@bot.message_handler(commands=['infoc'])
def chatInfo(message):
  bot.send_message(message.chat.id,"Айди чата "+str(message.chat.id))


@bot.message_handler(commands=['rules'])
def rules(message):
  bot.send_message(message.chat.id,6408)





''''
@bot.message_handler(commands=['gay'])
def start_message(message):
  bot.send_message("Гей чата будет "###):
@bot.message_handler(content_types=['text'])
def text_content(message):
	chatid=coll.find_one({'chatid':message.chat.id})
	if chatid==None:
		reg1 = { "chatid": message.chat.id,"ctrl":0 }
		coll.insert_one(reg)
  else:
    chatid=coll.find_one({'chatid':message.chat.id})
    if chatid!=None:
      for ids in chatid['users']:
        if chatid['users'][ids]['name'] == username1:
'''



bot.polling(none_stop=True)
