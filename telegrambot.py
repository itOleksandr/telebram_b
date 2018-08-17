import telebot
import const
from telebot import types
from geopy.distance import vincenty

bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Адреси аптек', request_location=True)
btn_payment = types.KeyboardButton("Варіанти оплати")
markup_menu.add(btn_address, btn_payment)

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, my Diar', reply_markup=markup_menu)

@bot.message_handler(func = lambda message: True)
def echo_all(message):
    if message.text=='Варіанти оплати':
        bot.reply_to(message,'Приват 24, Готівка, Visa/MasterCard', reply_markup=markup_menu)
    else:
        bot.reply_to(message, message.text, reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True, content_types=['location'])
def pharmacy_location(message):
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for m in const.PHARMACY:
        result = vincenty((m['latm'], m['lonm']), (lat, lon)).meters
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Найближча аптека')
    bot.send_venue(message.chat.id,
                   const.PHARMACY[index]['latm'],
                   const.PHARMACY[index]['lonm'],
                   const.PHARMACY[index]['title'],
                   const.PHARMACY[index]['adress'])
bot.polling()