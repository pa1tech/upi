#https://github.com/eternnoir/pyTelegramBotAPI
#https://developers.google.com/chart/infographics/docs/qr_codes
#https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=pa1tech@upi%26pn=Whomsoever%26am=100&chld=H

import telebot,time,os
from telebot import types
from flask import Flask, request
import re


#Telegram Bot Token
TOKEN="TOKEN"
bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")

#Flask App
app = Flask(__name__)

@app.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://vercel-upi-bot.vercel.app/' + TOKEN)
	return "!", 200

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200
start_msg = """Welcome to *!ncred UPI Pay!*

This bot helps you to create UPI payment link and QR, which you can share with your friends to receive money

*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* Send <upi id> to the bot. Sender has the freedom to fill the amount to be sent 
Example: *pmcares@sbi*

*Bank A/C, IFSC and Amount:* Beneficiary a/c no., IFSC and payable amount are to be sent in the format <a/c no.><space><ifsc><space><amount>
Example: *917897897897 PYTM0123456 116*

*Bank A/C, IFSC:* Send <a/c no.><space><ifsc> to the bot. Sender has the freedom to fill the amount to be sent. 
Example: *917897897897 PYTM0123456*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
	1. *@incred_upibot pmcares@sbi 11*
	2. *@incred_upibot pmcares@sbi*
	3. *@incred_upibot 917897897897 PYTM0123456 116*
	4. *@incred_upibot 917897897897 PYTM0123456*

To know more about the working of the bot : /about

*Please note,* the links generated are purely front-end and are not saved on the bot server

PS: Looks like the payment via link is being allowed on BHIM but other apps are not allowing for security reasons. QR's work just fine
"""

help_msg = """*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* This creates QR and link with just the receiver UPI ID. Sender has the freedom to fill the amount to be sent. Send <upi id> to the bot 
Example: *pmcares@sbi*

*Bank A/C, IFSC and Amount:* Beneficiary a/c no., IFSC and payable amount are to be sent in the format <a/c no.><space><ifsc><space><amount>
Example: *917897897897 PYTM0123456 116*

*Bank A/C, IFSC:* This creates QR and link to the specified a/c no. and IFSC. Sender has the freedom to fill the amount to be sent. Send <a/c no.><space><ifsc> to the bot 
Example: *917897897897 PYTM0123456*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
	1. *@incred_upibot pmcares@sbi 11*
	2. *@incred_upibot pmcares@sbi*
	3. *@incred_upibot 917897897897 PYTM0123456 116*
	4. *@incred_upibot 917897897897 PYTM0123456*

To know more about the working of the bot : /about
"""

about_msg = """
This bot has been developed in Python, built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and is served from Heroku).
QR codes are genearted using [Google Charts API](https://developers.google.com/chart/infographics/docs/qr_codes)

Developer: @pa1tech
"""

@bot.message_handler(commands=['start', 'help', 'about'])
def send_welcome(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, start_msg)
	elif message.text == '/help':
		bot.send_message(message.chat.id, help_msg)
	elif message.text == '/about':
		bot.send_message(message.chat.id, about_msg)
	
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

		if len(msg[0].split("@"))==1:
			x = re.findall("^[a-zA-Z]{4}[0-9]{7}$", msg[1])
			valid = ((msg[0].isdigit()) & (len(x)==1))
			usage = 3

	elif len(msg)==3:
		if len(msg[0].split("@"))==1:
			x = re.findall("^[a-zA-Z]{4}[0-9]{7}$", msg[1])
			valid = ((msg[0].isdigit()) & (len(x)==1) & (msg[2].isdigit()))
			usage = 4

	elif len(msg)==1:
		usage = 2
		if len(msg[0].split("@"))==2:
			valid = True

	if valid:
		if usage==1:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever%26am="+msg[1]+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/?%s&%s'>Click here</a></b> to pay ₹%s to <b>%s</b>\n(or)\nScan the above QR"%(msg[0],msg[1],msg[1],msg[0])
		elif usage==2:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever"+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/?%s'>Click here</a></b> to pay <b>%s</b>\n(or)\nScan the above QR"%(msg[0],msg[0])
		elif usage==3:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=%s@%s.ifsc.npci"%(msg[0],msg[1])+"%26pn=Whomsoever"+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/bank/?%s&%s'>Click here</a></b> to pay <b>%s-%s</b>\n(or)\nScan the above QR"%(msg[0],msg[1],msg[0],msg[1])
		elif usage==4:
			url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=%s@%s.ifsc.npci"%(msg[0],msg[1])+"%26pn=Whomsoever%26am="+msg[2]+"&chld=H?raw=True"
			descp = "<b><a href='https://pa1tech.github.io/upi/bank/?%s&%s&%s'>Click here</a></b> to pay ₹%s to <b>%s-%s</b>\n(or)\nScan the above QR"%(msg[0],msg[1],msg[2],msg[2],msg[0],msg[1])

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

		if len(msg[0].split("@"))==1:
			x = re.findall("^[a-zA-Z]{4}[0-9]{7}$", msg[1])
			valid = ((msg[0].isdigit()) & (len(x)==1))
			usage = 3

	elif len(msg)==3:
		if len(msg[0].split("@"))==1:
			x = re.findall("^[a-zA-Z]{4}[0-9]{7}$", msg[1])
			valid = ((msg[0].isdigit()) & (len(x)==1) & (msg[2].isdigit()))
			usage = 4

	elif len(msg)==1:
		usage = 2
		if len(msg[0].split("@"))==2:
			valid = True

	try:
		if valid:
			if usage == 1:
				rep = "VPA: %s - ₹%s"%(msg[0],msg[1])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever%26am="+msg[1]+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/?%s&%s"%(msg[0],msg[1])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay ₹%s to %s</b>"%(url1,url2,msg[1],msg[0])
			elif usage == 2:
				rep = "VPA: %s"%(msg[0])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa="+msg[0]+"%26pn=Whomsoever"+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/?%s"%(msg[0])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay %s</b>"%(url1,url2,msg[0])
			elif usage == 3:
				rep = "A/C: %s - IFSC: %s"%(msg[0],msg[1])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=%s@%s.ifsc.npci"%(msg[0],msg[1])+"%26pn=Whomsoever"+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/bank/?%s&%s"%(msg[0],msg[1])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay %s-%s</b>"%(url1,url2,msg[0],msg[1])
			elif usage == 4:
				rep = "A/C: %s - IFSC: %s - ₹%s"%(msg[0],msg[1],msg[2])
				url1 = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=%s@%s.ifsc.npci"%(msg[0],msg[1])+"%26pn=Whomsoever%26am="+msg[2]+"&chld=H?raw=True"
				url2 = "https://pa1tech.github.io/upi/bank/?%s&%s&%s"%(msg[0],msg[1],msg[2])
				descp = "Scan this <a href='%s'>QR</a>\n(or)\n<b><a href='%s'>Click here</a> to pay ₹%s to %s-%s</b>"%(url1,url2,msg[2],msg[0],msg[1])

			r = types.InlineQueryResultArticle('1', rep, input_message_content=types.InputTextMessageContent(descp,parse_mode="HTML"),thumb_url="https://pa1tech.github.io/upi/incred_upibot/botpic.jpg")
			bot.answer_inline_query(inline_query.id, [r],cache_time=1)
	except Exception as e:
		print(e)