import telebot
from telebot import types
from config import allcurrency, TOKEN
from extension import Converter

# Создание кнопок для /help
keyboard_help = types.ReplyKeyboardMarkup(row_width=2 , resize_keyboard=True , one_time_keyboard=True)
commandset = ["/values", "/allcurrencies"]
buttons = []
for com in commandset:
    buttons.append(types.KeyboardButton(com))
keyboard_help.add(*buttons)


# Создание кнопок для /start
keyboard_start = types.ReplyKeyboardMarkup(row_width=2 , resize_keyboard=True , one_time_keyboard=True)
commandset = ["/help", "/values", "/allcurrencies"]
buttons = []
for com in commandset:
    buttons.append(types.KeyboardButton(com))
keyboard_start.add(*buttons)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def starter(message: telebot.types.Message):
    user = message.from_user.first_name
    helptext = f"Здравствуйте, [{user}]\. \nБот поможет произвести конвертацию валют по свежему курсу\. "  \
               "\nЧтобы начать работу, введите команду боту в формате: " \
               "\n _\<исходная\>_ _\<целевая\>_ _\<количество\>_ " \
               "\n*Пример*: доллар рубль 320" \
               "\n\n *Доступные команды*: \n  /help \- справка \n  /values \- список доступных валют" \
               "\n  /allcurrency \- скачать все валюты мира"
    bot.reply_to(message , helptext , parse_mode="MarkdownV2", reply_markup=keyboard_start)

@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message):
    user = message.from_user.first_name
    helptext = f"Введите команду боту в формате: " \
               "\n _\<исходная\>_ _\<целевая\>_ _\<количество\>_ " \
               "\n*Пример*: доллар рубль 320" \
               "\n\n *Доступные команды*: \n  /values \- список доступных валют" \
               "\n  /allcurrency \- все валюты мира"
    bot.reply_to(message , helptext , parse_mode="MarkdownV2" , reply_markup=keyboard_help)


@bot.message_handler(commands=["values"])
def currency(message: telebot.types.Message):
    text = "*Доступные валюты:*"
    for cur_k, cur_v in allcurrency.items():
        par = f"{cur_k}: {cur_v}"
        text = "\n · ".join((text, str(par)))
    bot.reply_to(message, text, parse_mode="MarkdownV2", reply_markup=types.ReplyKeyboardRemove())


# Хэндлер для отправки файла по команде
@bot.message_handler(commands=['allcurrencies'])
def sendallcur(message: telebot.types.Message):
    with open("All currencies of World.pdf", "rb") as curfile:
        bot.send_document(message.chat.id, curfile, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.lower().split(" ")
    inputcheck = Converter.inputhandling(values)  # Проверка/обработка ввода
    if inputcheck:
        bot.reply_to(message, inputcheck["error"])
    else:
        get_price = Converter.getpricehandling(*values)  # Проверка/обработка подключения к API + результат
        if get_price.get("error"):
            bot.reply_to(message, get_price["error"])
        else:
            base_, target_, amount = values
            printout = f"Цена {amount} {allcurrency[base_]} составляет {float(get_price['target_result']):.3f} {allcurrency[target_]}"
            bot.reply_to(message, printout)


bot.polling(non_stop=True)
