import telebot
import random
import json
from telebot import types
import requests


class YandexGPT:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog

    def send_request(self, question, role_text):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = {
            "modelUri": f'gpt://{self.catalog}/yandexgpt-lite',
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 1000
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"{role_text}"
                },
                {
                    "role": "user",
                    "text": f"{question}"
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        text = response.json()['result']['alternatives'][0]['message']['text']
        return text


token = ''
catalog = ''

token = ''
bot = telebot.TeleBot(token)

todo = []
user_state = ''
DIALOG_STATE = 'dialog'


@bot.message_handler(commands=['start'])
def start(message):
    description = 'Я бот бот - нейросеть. Жми кнопку или команду /ask чтобы задать вопрос'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('задать вопрос')
    markup.add(button1)
    bot.send_message(message.chat.id, description, reply_markup=markup)


@bot.message_handler(commands=['ask'])
@bot.message_handler(commands=['задать вопрос'])
def ask(message):
    global user_state
    user_state = DIALOG_STATE
    bot.reply_to((message, 'Диалог начат. Выйти - команда /end'))

@bot.message_handler(func=lambda message: True)
def get_question(message):
    if user_state == DIALOG_STATE:

        bot.reply_to(message, 'Я ничего не знаю')

bot.infinity_polling()
