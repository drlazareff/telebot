import telebot
import random as r
import os

##from telebot import apihelper
##apihelper.proxy = {'http':'http://195.201.137.246:1080'}

bot = telebot.TeleBot('1399916936:AAHFUT2KDm5vDc6Spvzd4wDMa_Nh3BJiMSw')

directory= './Stickers'
menuStickers = os.listdir(directory)
menuHookah = ["шмаль и кокос","ёлки","ченить новое из дарка","дыня/арбуз","ягодный","фруктовый","десертный","танж с танжем и танжем", "Хватит курить!", "Для Андрейки","мёд с орешками","цитрусовый для Володьки","пушка страшная","марачино черри с чем-нить","ананас, кокос и абрикос","кисленький","вишневый","супернову для Лёшки"]
menuDrinks = ["пиво","два бада","хватит бухать!!","bud", "гинесс", "стелла", "водички с ледиком","просто воды(", "ягер","козла","любое пиво","чаёк","ром с колой","чё-т я не в настроении"]
menuGames = ["uno","контакт","молча бухаем","в молчанку","в крокодила","в шахматы с борисычем","время серьезное - не до игр!","в бутылочку!","в мафию","в телефоны залипайте, а?!"]

Skills = "Пока я умею : \n/кальян - помогу выбрать паркур \n/пить - помогу с напитками \n/игра - подскажу во что поиграть"


##print(directory+'/'+r.choice(menuStickers))

def choice(message):

	
	newtext = ""

	if message.text.upper() == "/КАЛЬЯН":
		newtext = r.choice(menuHookah)	
	elif message.text.upper() == "/ПИТЬ" :
		newtext = r.choice(menuDrinks)
	elif message.text.upper() == "/ИГРА" :
		newtext = r.choice(menuGames)		
	##elif message.text.upper() == "/HELP" :
	##	newtext = Skills			
	else :
		newtext = ""
	return newtext

@bot.message_handler(commands=['start'])
def get_start_messages(message):
	bot.send_message(message.chat.id,"Старик Евстратий приветствует тебя!")
	bot.send_message(message.chat.id,Skills)

@bot.message_handler(commands=['help'])
def get_help_messages(message):
	bot.send_message(message.chat.id,Skills)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	
	resp = choice(message)
	if resp != "" :
		filename = directory+'/'+r.choice(menuStickers)
		sti = open(filename, 'rb')
		bot.send_sticker(message.chat.id, sti)

		bot.send_message(message.chat.id,resp)
		

bot.polling(none_stop=True, interval=3)


