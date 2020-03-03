import telebot
from telebot import types
from pymongo import MongoClient
import os
import uuid
import random

client = MongoClient(os.environ["MongoDB"])
db = client.main
rulesColl = db.rules
adminsColl=db.admins
ruletkaColl=db.ruletka

uuidID = uuid.uuid1() 

admins2=adminsColl.find_one({"ID": 2552})

bot=telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет! Подробно в /help")

@bot.message_handler(commands=['help'])
def help_message(message):
  bot.send_message(message.chat.id,"Команды:\n/rules - Правила чата.\n/adminshelp - Команды для админов.")

@bot.message_handler(commands=['adminshelp'])
def admins_command(message):
	user = bot.get_chat_member(message.chat.id, message.from_user.id)
	if user.status == 'creator' or user.status == 'administrator':
		bot.send_message(message.chat.id,"Команды для админов:\n/newrules - Новые правила чата(Отвечать на чье-либо сообщение).\n/pin - Закрепить сообщение(Отвечать на чье-либо сообщение).\n/unpin - Открепить сообщение")
	else:
		bot.send_message(message.chat.id,"Вы не администратор чата!")

@bot.message_handler(commands=['infoc'])
def chatInfo(message):
  bot.send_message(message.chat.id,F"Айди чата: {message.chat.id}")

@bot.message_handler(commands=['randomnumber'])
def randomNumber(message):
	if len(message.text.split()) == 2:
		bot.send_message(message.chat.id,"/randomnumber {число1} {число2}")
		return
 	if len(message.text.split()) == 1:
		randn=random.randint(0,100)
 	else:
 		args = message.split()[1:]
		randn=random.randint(args[0], args[1])
	bot.send_message(message.chat.id, randn)

@bot.message_handler(commands=['pin'])
def PinMessage(message):
	if message.reply_to_message!=None:
		user = bot.get_chat_member(message.chat.id, message.from_user.id)
		if user.status == 'creator' or user.status == 'administrator':
			bot.pin_chat_message(message.chat.id,message.reply_to_message.message_id)
			bot.send_message(message.chat.id,"Успешно выполнено!")
		else:
			bot.send_message(message.chat.id,"Вы не администратор!")
	else:
		bot.send_message(message.chat.id,"Ответьте на сообщение.")
		
@bot.message_handler(commands=['unpin'])
def unPinMessage(message):
	user = bot.get_chat_member(message.chat.id, message.from_user.id)
	if user.status == 'creator' or user.status == 'administrator':
		bot.unpin_chat_message(message.chat.id)
		bot.send_message(message.chat.id,"Успешно выполнено!")
	else:
		bot.send_message(message.chat.id,"Вы не администратор чата!")

@bot.message_handler(commands=['infou'])
def userInfo(message):
	if message.reply_to_message!=None:
		bot.send_message(message.chat.id,f"Айди учатника: {message.reply_to_message.from_user.id}")
	else:
		bot.send_message(message.chat.id,f"Ваш айди: {message.from_user.id}")

@bot.message_handler(commands=['infom'])
def messageInfo(message):
	if message.reply_to_message!=None:
		bot.send_message(message.chat.id,f"Айди сообщения: {message.reply_to_message.message_id}")
	
@bot.message_handler(commands=['rules'])
def rules(message):
	if message.chat.id==-1001317298639:
		rulesid=rulesColl.find_one({"rules": {'$exists': True}})
		rulesChatId=rulesColl.find_one({"chatid": {'$exists': True}})
		bot.forward_message(message.chat.id,f"{rulesChatId['chatid']}",f"{rulesid['rules']}")

@bot.message_handler(commands=['newrules'])
def newrules(message):
	if message.reply_to_message!=None:
		user = bot.get_chat_member(message.chat.id, message.from_user.id)										
		if user.status == 'creator' or user.status == 'administrator':
			deleterules = rulesColl.delete_many ({})
			newrules = { "rules": message.reply_to_message.message_id,"chatid":message.chat.id}
			rulesColl.insert_one(newrules)
			bot.send_message(message.chat.id,"Правила установлены!")	
		else:
			bot.send_message(message.chat.id,"Вы не администратор чата!")
'''											
@bot.message_handler(commands=['create_ruletka'])
def createRuleka(message):
	ruletkaChat=ruletkaColl.find_one({"chatid": message.chat.id,"ctrl":0})
	if ruletkaChat == None:
		newRuletka = { "chatid": message.chat.id}
		ruletkaColl.insert_one(newRuletka)	
		bot.send_message(message.chat.id,"Рулетка успешно создана!")
	else:
		bot.send_message(message.chat.id,"В этом чате уже создана рулетка!")

@bot.message_handler(commands=['remove_ruletka'])
def removeRuletka(message):
	ruletkaChat=ruletkaColl.find_one({"chatid": message.chat.id})
	if ruletkaChat!=None:
		removeruletka = ruletkaColl.remove({"chatid":message.chat.id})
		bot.send_message(message.chat.id,"Рулетка удалена.")
	else:
		bot.send_message(message.chat.id,"Рулетка еще не была создана!")
							
@bot.message_handler(commands=['addruletka'])
def addRuletka(message):
	addruletka = message.text.split(' ')[1]
	if message.text.split(' ')==[1]:
		ruletkaChat=ruletkaColl.find_one({"chatid": message.chat.id})	
		for ids in ruletkaChat['users']:
			if x['users'][ids]['name'] != addruletka:
				ruletkaColl.update_one({"chatid":message.chat.id }, {'$set':{repr(uuidID.bytes): addruletka}})
				bot.send_message(message.chat.id,"Значение успешно добавлено в рулетку!")
			else:
				bot.send_message(message.chat.id,"Такое значение уже существует в рулетке!")
							
							
	else:
		bot.send_message(message.chat.id,"/addruletka Значение(имя,кличка и т.д.)"

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
