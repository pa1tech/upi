#https://github.com/eternnoir/pyTelegramBotAPI
#https://developers.google.com/chart/infographics/docs/qr_codes
#https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=pa1tech@upi%26pn=Whomsoever%26am=100&chld=H
import telebot,time,os
from telebot import types
from flask import Flask, request

#Telegram Bot Token
TOKEN="TOKEN"

#Flask App
app = Flask(__name__)

@app.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://incred-upibot.herokuapp.com/' + TOKEN)
	return "!", 200

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

start_msg = """Welcome to *!ncred UPI Pay!*

This bot helps you to create UPI payment link and QR, which you can share with your friends to receive money

*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* This creates QR and link with just the receiver UPI ID. Sender has the freedom to fill the amount to be sent. Send <upi id> to the bot 
Example: *pmcares@sbi*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
	1. *@incred_upibot pmcares@sbi 11*
	2. *@incred_upibot pmcares@sbi*

To know more about the working of the bot : /about

*Please note,* the links generated are purely front-end and are not saved on the bot server
"""

help_msg = """*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* This creates QR and link with just the receiver UPI ID. Sender has the freedom to fill the amount to be sent. Send <upi id> to the bot 
Example: *pmcares@sbi*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
	1. *@incred_upibot pmcares@sbi 11*
	2. *@incred_upibot pmcares@sbi*

To know more about the working of the bot : /about
"""

about_msg = """Developer: @pa1tech
Website: https://pa1tech.github.io/

This bot has been developed in Python, built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and is served from [Heroku](https://www.heroku.com/).
QR codes are genearted using [Google Charts API](https://developers.google.com/chart/infographics/docs/qr_codes)

*More Info:*
*+* [What's encoded in a UPI QR?](https://pa1tech411.blogspot.com/2020/04/upi-qr.html)
*+* [Source code of the link generated](https://github.com/pa1tech/upi/)
*+* [Source code of the bot](https://github.com/pa1tech/upi/tree/master/incred_upibot)
"""

upi_video = """ Here is a short video describing what's encoded in a UPI QR
https://youtu.be/qXvwXBQ5YGM
"""

bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN") # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help', 'about'])
def send_welcome(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, start_msg)
	elif message.text == '/help':
		bot.send_message(message.chat.id, help_msg)
	elif message.text == '/about':
		bot.send_message(message.chat.id, about_msg)
		time.sleep(10)
		bot.send_message(message.chat.id, upi_video)

@bot.message_handler(func=lambda message: True)
def chat_handler(message):
	msg = message.text.split(" ")
	cid = message.chat.id

	valid = False
	usage = 0

	if len(msg)==2:
		usage = 1
		if len(msg[0].split("@"))==2:
			valid =  msg[1].isdigit()
	elif len(msg)==1:
		usage = 2
		if len(msg[0].split("@"))==2:
			valid = True

	if valid:
		if usage==1:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever%26am="+msg[1]+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/?%s&%s'>Click here</a></b> to pay Rs.%s to <b>%s</b>\n(or)\nScan the above QR"%(msg[0],msg[1],msg[1],msg[0])
		else:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever"+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/vpa/?%s'>Click here</a></b> to pay <b>%s</b>\n(or)\nScan the above QR"%(msg[0],msg[0])
		bot.send_photo(cid, url,descp,parse_mode="HTML")
	else:
		bot.reply_to(message, "Invalid request, check /help for usage info")

	
@bot.inline_handler(lambda query: len(query.query)>0 )
def query_text(inline_query):
	msg = inline_query.query.split(" ")
	valid = False
	usage = 0

	if len(msg)==2:
		usage = 1
		if len(msg[0].split("@"))==2:
			valid =  msg[1].isdigit()
	elif len(msg)==1:
		usage = 2
		if len(msg[0].split("@"))==2:
			valid = True

	try:
		if valid:
			if usage == 1:
				rep = "VPA: %s - Rs.%s"%(msg[0],msg[1])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever%26am="+msg[1]+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/?%s&%s"%(msg[0],msg[1])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay Rs.%s to %s</b>"%(url1,url2,msg[1],msg[0])
			else:
				rep = "VPA: %s"%(msg[0])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever"+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/vpa/?%s"%(msg[0])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay %s</b>"%(url1,url2,msg[0])
			r = types.InlineQueryResultArticle('1', rep, input_message_content=types.InputTextMessageContent(descp,parse_mode="HTML"))
			bot.answer_inline_query(inline_query.id, [r],cache_time=1)
	except Exception as e:
		print(e)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))