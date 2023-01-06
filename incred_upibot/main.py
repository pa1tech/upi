#https://github.com/eternnoir/pyTelegramBotAPI
#https://developers.google.com/chart/infographics/docs/qr_codes
#https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=pa1tech@upi%26pn=Whomsoever%26am=100&chld=H
import telebot,time,logging
from telebot import types
import sys
import re

#telebot.logger.setLevel(logging.DEBUG)
TOKEN="TOKEN"
bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN") # You can set parse_mode by default. HTML or MARKDOWN

start_msg = """Welcome to *!ncred UPI Pay!*

This bot helps you to create UPI payment link and QR, which you can share with your friends to receive money

*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
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

*Please note,* the links generated are purely front-end and are not saved on the bot server
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

about_msg = """Developer: @pa1tech
Website: https://pa1tech.github.io/

This bot has been developed in Python, built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and is served from [PythonAnywhere](https://www.pythonanywhere.com/).
QR codes are genearted using [Google Charts API](https://developers.google.com/chart/infographics/docs/qr_codes)

*More Info:*
*+* [What's encoded in a UPI QR?](https://pa1tech411.blogspot.com/2020/04/upi-qr.html)
*+* [Source code of the link generated](https://github.com/pa1tech/upi/)
*+* [Source code of the bot](https://github.com/pa1tech/upi/tree/master/incred_upibot)
"""

upi_video = """ Here is a short video describing what's encoded in a UPI QR
https://youtu.be/qXvwXBQ5YGM
"""

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

			r = types.InlineQueryResultArticle('1', rep, input_message_content=types.InputTextMessageContent(descp,parse_mode="HTML"))
			bot.answer_inline_query(inline_query.id, [r],cache_time=1)
	except Exception as e:
		print(e)

def main_loop():
	bot.polling(True)
	while 1:
		time.sleep(3)


if __name__ == '__main__':
	try:
		main_loop()
	except KeyboardInterrupt:
		print('\nExiting by user request.\n')
		sys.exit(0)