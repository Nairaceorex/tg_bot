import time

import telebot
from telebot.types import Message
import text
from game import db

bot = telebot.TeleBot('TOKEN')
temp = {}


@bot.message_handler(['start'])
def start(msg: Message):
    if db.is_new_player(msg):
        reg_1(msg)
        temp[msg.chat.id] = {"name": None}
    else:
        bot.send_message(msg.chat.id, f'Ты уже в игре!)')
        menu(msg)


def reg_1(msg: Message):  # тут мы приветствуем игрока и спрашиваем имя
    bot.send_message(msg.chat.id, f'{text.reg} {msg.from_user.first_name}')
    bot.register_next_step_handler(msg, reg_2)


def reg_2(msg: Message):  # спрашиваем оружие
    # Сохраняем имя
    if not temp[msg.chat.id]["name"]:
        temp[msg.chat.id]["name"] = msg.text
    bot.send_message(msg.chat.id, "Выбери своё оружие: Дробовик, Снайперка, Миниган, АК-47")
    bot.register_next_step_handler(msg, reg_3)


def reg_3(msg: Message):
    # Сохраняем оружие
    temp[msg.chat.id]["power"] = msg.text
    db.users.write([
        msg.chat.id, temp[msg.chat.id]["name"],
        msg.text, 100, 10, 1, 0
    ])
    db.heals.write([
        msg.chat.id, {}
    ])
    print("Игрок добавлен в БД")
    bot.send_message(msg.chat.id, text.tren)
    time.sleep(2)
    menu(msg)


@bot.message_handler(['menu'])
def menu(msg: Message):
    bot.send_message(msg.chat.id, text.menu)

@bot.message_handler(['add_heal'])
def add_heal(msg: Message):
    bot.send_message(msg.chat.id, text.tren)
    stats = db.heals.read('userid', msg.chat.id)
    print(stats)


@bot.message_handler(['train'])
def train(msg: Message):
    bot.send_message(msg.chat.id, text.tren)
    stats = db.users.read('userid', msg.chat.id)
    print(stats)
    stats[3]*=1.05
    stats[4]*=1.03
    db.users.write(stats)
    print(stats)


bot.infinity_polling()
