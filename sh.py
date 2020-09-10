import telebot
from telebot import types
import random as r
import os
import requests
from bs4 import BeautifulSoup


##TO DO: переделать в конфиг
if os.name == 'nt' :
	Token = '1149687109:AAE3JO1YV7yezQXeq3epacsXtQOu1cZsdq0'
	directory= str(os.getcwd())+'\\'
else :
	Token = '1399916936:AAHFUT2KDm5vDc6Spvzd4wDMa_Nh3BJiMSw'
	directory= '/home/evs/telebot/'

bot = telebot.TeleBot(Token)

menuHookah = []
menuStickers = []
menuDrinks = []
menuGames = []

skillType = ''
skillFileName = ''
initNewSkill = False
skillQuestion = ''


def initParams() :
	global menuDrinks;
	global menuStickers;
	global menuHookah;
	global menuGames;

	menuStickers = os.listdir(directory+'Stickers/')
	
	menuHookah = []
	with open(directory+'Hookah.txt',encoding='utf-8') as f:
		for line in f:
			st = str(line.replace(chr(10),''))
			st = st.strip()
			if len(st)>0 :
				menuHookah.append(st.lower())
	f.close()
	menuDrinks = []	
	with open(directory+'Drinks.txt',encoding='utf-8') as f:
		for line in f:
			st = str(line.replace(chr(10),''))
			st = st.strip()
			if len(st)>0 :
				menuDrinks.append(st.lower())
	f.close()	
	menuGames = []
	with open(directory+'Games.txt',encoding='utf-8') as f:
		for line in f:
			st = str(line.replace(chr(10),''))
			st = st.strip()
			if len(st)>0 :
				menuGames.append(st.lower())
	#		f.close()	
	f.close()

init = initParams()


def getKeyboard(Type) :
	keyboard = types.InlineKeyboardMarkup()

	if Type == 'main' :

		key_hookah = types.InlineKeyboardButton(text='Кальян', callback_data='Кальян')
		key_drinks = types.InlineKeyboardButton(text='Напиток', callback_data='Пить')
		key_games = types.InlineKeyboardButton(text='Игра', callback_data='Игра')
		key_humor = types.InlineKeyboardButton(text='Шутка', callback_data='Юмор')
		keyboard.row(key_hookah,key_drinks)
		keyboard.row(key_games,key_humor)

	elif Type == 'new' :
		key_hookah = types.InlineKeyboardButton(text='Кальян', callback_data='newHookah')
		key_drinks = types.InlineKeyboardButton(text='Напиток', callback_data='newDrinks')
		key_games = types.InlineKeyboardButton(text='Игра', callback_data='newGames')
		keyboard.row(key_hookah,key_drinks,key_games)

	elif Type == 'all' :
		key_hookah = types.InlineKeyboardButton(text='Кальяны', callback_data='allHookah')
		key_drinks = types.InlineKeyboardButton(text='Напитки', callback_data='allDrinks')
		key_games = types.InlineKeyboardButton(text='Игры', callback_data='allGames')
		keyboard.row(key_hookah,key_drinks,key_games)	
		
	return keyboard

Skills = "Смотри чего я умею : \nкальян - помогу выбрать паркур \nпить - помогу с напитками \nигра - подскажу во что поиграть \nюмор - подниму настроение"

NoImages = ("юмор")


## start choice
def choice(message):
	newtext = ""

	if message.lower() == "кальян":
		newtext = r.choice(menuHookah)	
	elif message.lower() == "пить" :
		newtext = r.choice(menuDrinks)
	elif message.lower() == "игра" :
		newtext = r.choice(menuGames)		
	elif message.lower() == "юмор" :
		newtext = getHumor()			
	else :
		newtext = ""
	return newtext
## end choice

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

#TO DO : сделать адекватную замену
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


def sendAnswer (chatId,textQuestion) :
	global initNewSkill;

	textQuestion = textQuestion.strip()
	textQuestion = textQuestion.lower()

	if initNewSkill == True :
		if skillType == 'Hookah' :
			k = menuHookah.count(textQuestion)
			fin = 'такой кальян )'
			finSuccess = ' новый кальян : '
		elif skillType == 'Drinks' :
			k = menuDrinks.count(textQuestion)
			fin = 'такой напиток )'
			finSuccess = ' новый напиток : '
		elif skillType == 'Games' :
			k = menuGames.count(textQuestion)
			fin = 'такую игру )'
			finSuccess = ' новую игру : '
		else :
			k = 0

		if k > 0 :
			bot.send_message(chatId,'Хе-Хе! А я уже знаю '+fin)
		else :
			#try : 
			f = open(directory+skillFileName,'a',encoding='utf-8')				
			f.write(textQuestion+'\n')	
			f.close()
			initParams()
			bot.send_message(chatId,'Ура! Я выучил '+finSuccess+textQuestion)	
			#except :	
			#	bot.send_message(chatId,'что-то пошло не так( не смог запомнить(')	

		initNewSkill = False	

	else :
		resp = choice(textQuestion)
		if resp != "" :
			if NoImages.count(textQuestion.upper()) == 0 :
				filename = directory+'Stickers/'+r.choice(menuStickers)
				sti = open(filename, 'rb')
				bot.send_sticker(chatId, sti)
				bot.send_message(chatId,resp)


def addSkill(chatId,Skill) :
	 global skillType;
	 global skillFileName;
	 global skillQuestion;
	 global initNewSkill;

	 skillType = Skill.replace('new','')
	 skillFileName  = skillType+'.txt'

	 if skillType == 'Hookah' :
	 	skillQuestion = 'Про какой кальян ты хочешь мне рассказать?'
	 elif skillType == 'Drinks' :	
	 	skillQuestion = 'Про какой напиток ты хочешь мне рассказать?'
	 elif skillType == 'Games' :	
	 	skillQuestion = 'Про какую игру ты хочешь мне рассказать?'
	 else :
	 	skillQuestion = 'Про что ты хочешь мне рассказать?'
	 initNewSkill = True	

	 bot.send_message(chatId,skillQuestion)

def saySkills(chatId,Skill) :
	 skillType = Skill.replace('all','')
	 Skills = ''
	 if skillType == 'Hookah' :
	 	Skills = 'Вот такие кальяны я знаю : \n'	
	 	for item in menuHookah :
	 		Skills = Skills + item+'\n'
	 elif skillType == 'Drinks' :	
	 	Skills = 'Вот такие напитки я знаю : \n'	
	 	for item in menuDrinks :
	 		Skills = Skills + item+'\n'
	 elif skillType == 'Games' :	
	 	Skills = 'Вот такие игры я знаю : \n'	
	 	for item in menuGames :
	 		Skills = Skills + item+'\n'
	 else :
	 	Skills='че-то я забыл всё('
	
	 bot.send_message(chatId,Skills)	 


## Старт программы ! 

@bot.message_handler(commands=['start'])
def get_start_messages(message):
	bot.send_message(message.chat.id,"Старик Евстратий приветствует тебя! \n Чем я могу тебе помочь?",reply_markup=getKeyboard('main'))
	
@bot.message_handler(commands=['help'])
def get_help_messages(message):
	bot.send_message(message.chat.id,Skills)

@bot.message_handler(commands=['new'])
def get_help_messages(message):
	bot.send_message(message.chat.id,"О чем ты хочешь мне рассказать?",reply_markup=getKeyboard('new'))

@bot.message_handler(commands=['all'])
def get_help_messages(message):
	bot.send_message(message.chat.id,"О чем тебе рассказать?",reply_markup=getKeyboard('all'))	


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	sendAnswer(message.chat.id,message.text)





@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data.find('new') >= 0 : 
		addSkill(call.message.chat.id,call.data)
	elif call.data.find('all') >= 0 : 	
		saySkills(call.message.chat.id,call.data)
	else :
		sendAnswer(call.message.chat.id,call.data)
    	

bot.polling(none_stop=True, interval=3)


