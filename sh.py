import telebot
import random as r

bot = telebot.TeleBot('1399916936:AAHFUT2KDm5vDc6Spvzd4wDMa_Nh3BJiMSw')

	


def choice(message):

	menuHookah = ["шмаль и кокос","а кальянщик чё говорит?","сам чё не умеешь чтоли?","ягодный","фруктовый","десертный","вкусный", "Любой", "Хватит курить!", "Для Андрейки","мёд с орешками","цитрусовый для Володьки","пушка страшная","марачино черри с чем-нить","ананас, кокос и абрикос","на выбор мастера","я в домике","супернову для Лёшки"]
	menuDrinks = ["пиво","два бада","хватит бухать!!","bud", "пох чо", "стелла", "водички с ледиком", "лёдику","козла и потемнее","чаёк","ром с колой","чё-т я не в настроении"]
	menuGames = ["uno","контакт","молча бухаем","в молчанку","в крокодила","в шахматы с борисычем","время серьезное - не до игр!","в бутылочку!","в мафию","в телефоны залипайте, а?!"]
	
	newtext = ""

	if message.text.upper() == "/КАЛЬЯН":
		newtext = r.choice(menuHookah)	
	elif message.text.upper() == "/ПИТЬ" :
		newtext = r.choice(menuDrinks)
	elif message.text.upper() == "/ИГРА" :
		newtext = r.choice(menuGames)		
	elif message.text.upper() == "/HELP" :
		newtext = ("Пока я умею : \n/кальян - помогу выбрать паркур \n/пить - помогу с напитками \n/игра - подскажу во что поиграть")			
	else :
		newtext = ""
	return newtext


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	
	resp = choice(message)
	if resp != "" :
		bot.send_message(message.chat.id,resp)

bot.polling(none_stop=True, interval=5)


