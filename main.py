import telebot

bot = telebot.TeleBot("8155849903:AAEXuuAvVK_SzoRhPufTFjbbkSMjAtL1UNA")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, '  love به چنل سکند دیت خوش اومدی')

bot.polling()