import telebot
from config import *
import sqlite3
from telebot import types


category = ""
suma_tovara = 0
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    #Кнопки:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить расход")
    btn2 = types.KeyboardButton("Удалить расход")
    btn3 = types.KeyboardButton("Посчитать результат")
    btn4 = types.KeyboardButton("Удалить все расходы")
    markup.add(btn1, btn2, btn3, btn4)
    #Добавление юзера в базу данных:
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
            chat_id INTEGER,
            Категория TEXT ,
            Сумма INTEGER,
            Примечание TEXT 
            )""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT chat_id FROM expenses WHERE chat_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_list = [message.chat.id, "Нераспознанное", 0, ""]



        cursor.execute("INSERT INTO expenses VALUES(?,?,?,?);", user_list)
        connect.commit()
        text = "Привет! Меня зовут Бот-Финансовый помощник."
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Такой пользователь уже существует", reply_markup=markup)


def set_data(data, categor):
    global category
    global suma_tovara
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    user_list = [data.chat.id, categor, suma_tovara, category]
    cursor.execute("INSERT INTO expenses VALUES(?,?,?,?);", user_list)
    category = ""
    suma_tovara = 0
    connect.commit()


def delet_data(categ, suma, people):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM expenses WHERE Примечание = "{categ}" and Сумма = {suma} and chat_id = {people}')
    connect.commit()


def delet_all_const(message):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    mes = message.text
    if mes == "Да":
        cursor.execute(f'DELETE FROM expenses WHERE chat_id = {message.chat.id}')
        bot.send_message(message.chat.id, "Вы удалили все расходы")
    elif mes == "Нет":
        bot.send_message(message.chat.id, "Вы решили не удалять свои расходы, можете продолжать работу")
    connect.commit()


def set_cons(message):
    global category
    global suma_tovara
    categ, rub = message.text.split('-')
    rub = rub.strip()
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Продукты', callback_data="prod")
    btn2 = types.InlineKeyboardButton(text='Бытхимия, мебель, хозтовары', callback_data="xim")
    btn3 = types.InlineKeyboardButton(text='Одежда, игрушки, секции', callback_data="odezda")
    btn4 = types.InlineKeyboardButton(text='Счета', callback_data="chet")
    btn5 = types.InlineKeyboardButton(text='Транспорт', callback_data="transport")
    btn6 = types.InlineKeyboardButton(text='Фастфуд, алкоголь, сигареты', callback_data="fastfud")
    btn7 = types.InlineKeyboardButton(text='Связь, интернет', callback_data="internet")
    btn8 = types.InlineKeyboardButton(text='Лекарство, средства по уходу за собой', callback_data="apteka")
    btn9 = types.InlineKeyboardButton(text='Прочее', callback_data="prochee")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    category = categ.strip()
    suma_tovara = int(rub.replace(" ", ""))
    bot.send_message(message.chat.id, f"В какую категорию добавить {categ.replace(' ', '')}?", reply_markup=markup)


def delet_cons(message):
    x, y = message.text.split('-')
    x2 = x.strip()
    y = int(y.strip())
    people = message.chat.id
    delet_data(x2, y, people)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'prod':
        set_data(call.message, "Продукты")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'xim':
        set_data(call.message, "Бытхимия, мебель, хозтовары")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'odezda':
        set_data(call.message, "Одежда, игрушки, секции")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'chet':
        set_data(call.message, "Счета")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'transport':
        set_data(call.message, "Транспорт")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'fastfud':
        set_data(call.message, "Фастфуд, алкоголь, сигареты")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'internet':
        set_data(call.message, "Связь, интернет")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'apteka':
        set_data(call.message, "Лекарство, средства по уходу за собой")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    elif call.data == 'prochee':
        set_data(call.message, "Прочее")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расход записан")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Произошла ошибка...")


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "Добавить расход":
        bot.send_message(message.chat.id, "Введите свой расход, например: хлеб - 32, деньги на телефон-450")
        bot.register_next_step_handler(message, set_cons)
    elif message.text == "Удалить расход":
        bot.send_message(message.chat.id, "Введите расход и сумму, который хотите удалить, например: хлеб - 32, деньги на телефон-450")
        bot.register_next_step_handler(message, delet_cons)
    elif message.text == "Посчитать результат":
        suma_trat = 0
        suma_obz = 0
        connect = sqlite3.connect("user.db")
        cursor = connect.cursor()
        cursor.execute(f'SELECT * FROM expenses WHERE chat_id = {message.chat.id}')
        result = cursor.fetchone()
        for result in cursor:
            if result[1] == "Фастфуд, алкоголь, сигареты":
                suma_trat += result[2]
                suma_obz += result[2]
            else:
                suma_obz += result[2]
        bot.send_message(message.chat.id, f"Вы потратили {suma_obz} руб \nЕсли бы не тратили деньга на фастфуд, алкоголь, сигареты, то вы могли бы сэкономить {suma_trat} руб")
        connect.commit()
    elif message.text == "Удалить все расходы":
        bot.send_message(message.chat.id, "Вы уверены что хотите удалить все свои расходы?\nНапишите да, если хотите удалить или нет, если вы передумали.")
        bot.register_next_step_handler(message, delet_all_const)
    else:
        bot.send_message(message.chat.id, "Я не понял, что вы ввели? Повторите попытку...")


bot.polling(none_stop=True, interval=0)