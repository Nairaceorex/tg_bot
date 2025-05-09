import telebot
from telebot.types import Message

bot = telebot.TeleBot('TOKEN')
def start(msg: Message):
   kb = telebot.types.ReplyKeyboardMarkup(True, False)
bot.infinity_polling()
