## !ncred UPI Pay - [@incred_upibot](https://telegram.me/incred_upibot)
Welcome to *!ncred UPI Pay!*

This bot helps you to create UPI payment link and QR, which you can share with your friends to receive money

*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* This creates QR and link with just the receiver UPI ID. Sender has the freedom to fill the amount to be sent. Send <upi id> to the bot 
Example: *pmcares@sbi*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
	1. *@incred_upibot pmcares@sbi 11*
	2. *@incred_upibot pmcares@sbi*

---

This bot has been developed in Python, built with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and is served from [PythonAnywhere](https://www.pythonanywhere.com/).
QR codes are genearted using [Google Charts API](https://developers.google.com/chart/infographics/docs/qr_codes)

*More Info:*
* [What's encoded in a UPI QR?](https://pa1tech.github.io/blog/upi)
* [Source code of the link generated](https://github.com/pa1tech/upi/)
* [Source code of the bot](https://github.com/pa1tech/upi/tree/master/incred_upibot)
