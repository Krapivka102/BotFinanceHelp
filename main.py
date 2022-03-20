import telebot
import config


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Как круто, это же мой первый бот!')

bot.polling(none_stop=True, interval=0)