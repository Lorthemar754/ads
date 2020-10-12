# pip install python-whois
# pip install python-dateutil
import whois
import telebot
import requests
import time
import datetime
from dateutil import parser

bot = telebot.TeleBot(' ')
time_now = (int(datetime.datetime.now().timestamp()))

#Получение exp даты в epoch
def data(a):
    data_time = (a['expiration_date'])
    if isinstance(data_time, list):
        try:
            exp_data = (data_time[0])
        except TypeError:
            exp_data = data_time
    else:
        try:
            exp_data = parser.parse(data_time)
        except TypeError:
            exp_data = data_time
    return int(exp_data.timestamp())

#Примерное врменя ожидаения, 100 доменов ~ 30 секунд
def wait_time(b):
    time = (30 * b)/ 100
    return time

#здарова
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вечер в хату,\nдай домены')

@bot.message_handler(content_types=['text'])
def send_text(message):
    counter = 0
    msg = message.json
    str_domains = (msg['text'])
    domains = str_domains.split('\n')
    len_domains = len(domains)
    time_for_waint = wait_time(len_domains)
    bot.send_message(message.chat.id, f'Примерно {time_for_waint} сек.')
    result = []
    result_coming = []
#получение инфы с хуиза
    for q in domains:
        try:
            w = whois.whois(q)
        except whois.parser.PywhoisError:
            result.append(q)
#проверяет есть ли инфа по домену
        try:
            if (w['expiration_date']) == None:
                result.append(q)
            else:
                domain_free_time = data(w)
                if domain_free_time - time_now < 604800: #604800 - неделя в секундах
                    result_coming.append(q + ' освободится - ' + str((w['expiration_date'])))
        except KeyError:
            result.append(q)
        counter += 1
        print (f'{counter}. {q}')
    msg_result_coming = ('\n'.join(result_coming))
    if not result:
        bot.send_message(message.chat.id, 'Свободных нет')
        if not result_coming:
            pass
        else:
            bot.send_message(message.chat.id, f'Ближайшие:\n{msg_result_coming}')
    else:
        msg_result = ('\n'.join(result))
        bot.send_message(message.chat.id, f'Свободные:\n{msg_result}')
        if not result_coming:
            pass
        else:
            bot.send_message(message.chat.id, f'Ближайшие:\n{msg_result_coming}')
bot.polling(none_stop=True)
