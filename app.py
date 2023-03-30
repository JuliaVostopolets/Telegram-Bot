import telebot
from config import keys, TOKEN
from extensions import GetPrice, ConvertationEcseption

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def welcome_help (message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}! "
    f"Я бот, который конвертирует валюты. Я постараюсь тебе помочь) "
    f"Чтобы начать работу введи команду в фомате: <имя валюты>"
    f"<в какую валюту перевести><количество переводимой валюты>"
    f'Чтобы увидеть список доступных валют используй команду /values')


@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text,key))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertationEcseption('Слишком много параметров')
        quote, base, amount = values
        total_base= GetPrice.convert(quote,base,amount)
    except ConvertationEcseption as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не могу обработать команду\n{e}, возможно ты написал с большой буквы')
    else:
        text= f'Переводим {quote} в {base} : {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id,text)



bot.polling()
