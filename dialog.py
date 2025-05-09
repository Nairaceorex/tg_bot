import telebot
from telebot.types import Message

bot = telebot.TeleBot('TOKEN')

n = 0

@bot.message_handler(['start'])
def start(msg: Message):
   bot.send_message(msg.chat.id, "Назови число от 1 до 10")
   bot.register_next_step_handler(msg, number_two)

def number_two(msg: Message):
   global n
   n = int(msg.text)
   if n not in range(1, 11):
       bot.send_message(msg.chat.id, "Ты ошибся в диапазоне!")
       start(msg)
       return
   bot.send_message(msg.chat.id, "Назови еще одно число от 1 до 10")
   bot.register_next_step_handler(msg, result)


def result(msg: Message):
    m = int(msg.text)
    if m not in range(1, 11):
        bot.send_message(msg.chat.id, "Ты ошибся в диапазоне!")
        number_two(msg)
        return

    bot.send_message(msg.chat.id, f"Если возвести {n} в {m} степень, "
                                  f"то получится число {n ** m}")


bot.infinity_polling()