import telebot
import config
import sqlite3


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
            chat_id INTEGER,
            Category TEXT ,
            Suma INTEGER,
            Note TEXT 
            )""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT chat_id FROM expenses WHERE chat_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_list = [message.chat.id, "Нераспознанное", 0, ""]
        cursor.execute("INSERT INTO expenses VALUES(?,?,?,?);", user_list)
        connect.commit()
    else:
        bot.send_message(message.chat.id, "Такой пользователь уже существует")


bot.polling(none_stop=True, interval=0)