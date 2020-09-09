import telebot
import random as r
import os
import requests
from bs4 import BeautifulSoup

##TO DO: переделать в конфиг

bot = telebot.TeleBot('1399916936:AAHFUT2KDm5vDc6Spvzd4wDMa_Nh3BJiMSw')

if os.name == 'nt' :
	directory= './Stickers'
else :
	directory= directory= '/home/evs/telebot/Stickers'


menuStickers = os.listdir(directory)
menuHookah = ["шмаль и кокос","ёлки","ченить новое из дарка","дыня/арбуз","ягодный","фруктовый","десертный","танж с танжем и танжем", "Хватит курить!", "Для Андрейки","мёд с орешками","цитрусовый для Володьки","пушка страшная","марачино черри с чем-нить","ананас, кокос и абрикос","кисленький","вишневый","супернову для Лёшки"]
menuDrinks = ["пиво","два бада","хватит бухать!!","bud", "гинесс", "стелла", "водички с ледиком","просто воды(", "ягер","козла","любое пиво","чаёк","ром с колой","чё-т я не в настроении"]
menuGames = ["uno","контакт","молча бухаем","в молчанку","в крокодила","в шахматы с борисычем","время серьезное - не до игр!","в бутылочку!","в мафию","в телефоны залипайте, а?!"]

Skills = "Пока я умею : \n/кальян - помогу выбрать паркур \n/пить - помогу с напитками \n/игра - подскажу во что поиграть \n /юмор - подниму настроение"

NoImages = ("/ЮМОР")

##print(directory+'/'+r.choice(menuStickers))

def choice(message):

	
	newtext = ""

	if message.text.upper() == "/КАЛЬЯН":
		newtext = r.choice(menuHookah)	
	elif message.text.upper() == "/ПИТЬ" :
		newtext = r.choice(menuDrinks)
	elif message.text.upper() == "/ИГРА" :
		newtext = r.choice(menuGames)		
	elif message.text.upper() == "/ЮМОР" :
		newtext = getHumor()			
	else :
		newtext = ""
	return newtext


def getHumor():

	try:
		
		HEADERS = {  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', }
		response = requests.get('https://bash.im/random',headers=HEADERS)
		soup = BeautifulSoup(response.text, 'html.parser')
		HumorList=[]
		htmlParse = soup.find_all("div","quote__body")

		for item in htmlParse:
			HumorList.append(item)

		humor = str(r.choice(htmlParse))
		humor = replaceTags(humor)	
		return humor	
	except :
		return "Ой, нишмагла ("	

def replaceTags(text) :
	text = text.replace("</br>","")
	text = text.replace("<br/>","\n")
	text = text.replace("<br>","\n")
	text = text.replace('<div class="quote__body">',"")
	text = text.replace("</div>","")
	text = text.replace("&lt;","<")
	text = text.replace("&gt;",">")

	text = text.lstrip()

	return text



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
		if NoImages.count(message.text.upper()) == 0 :
			filename = directory+'/'+r.choice(menuStickers)
			sti = open(filename, 'rb')
			bot.send_sticker(message.chat.id, sti)

		bot.send_message(message.chat.id,resp)
		

bot.polling(none_stop=True, interval=3)


