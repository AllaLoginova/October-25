import telebot
import random

token = '7985795571:AAFs5VcM9Yo7K-CY8ufRPcl-zrMreKukPLc'
bot = telebot.TeleBot(token)

count = 0
bot_number = random.randint(1, 5)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")


@bot.message_handler(commands=['game'])
def game(message):
    bot.send_message(message.chat.id, 'Угадай число, которое я загадал')
    bot.send_message(message.chat.id, 'Введи число')


@bot.message_handler(content_types=['text'])
def get_user_number(message):
    global count, bot_number

    # print(bot_number)
    user_number = int(message.text.strip())

    if bot_number == user_number:
        bot.reply_to(message, f"Угадал! Попыток было: {count}")

    else:
        bot.send_message(message.chat.id, '“Не угадал')
        count += 1


bot.infinity_polling()
# bot.polling(non_stop=True)