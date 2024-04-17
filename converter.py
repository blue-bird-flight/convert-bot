import telebot
from extensions import ConvertException
from extensions import CurrencyConverter
from config import Token, values

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['help', 'start'])
def hlp(message: telebot.types.Message):
    mess_text = 'чтобы начать \n необходимо ввести запрос в следующем формате: \n ''кол-во валюты1 валюта1 валюта2'' \n доступные валюты : /values'
    bot.reply_to(message, mess_text)


@bot.message_handler(commands=['values'])
def val(message: telebot.types.Message):
    mess_text = 'доступные вылюты'
    for key in values.keys():
        mess_text = '\n'.join((mess_text, key))
    bot.reply_to(message, mess_text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        data = message.text.split(' ')
        if len(data) != 3:
            raise ConvertException('не верный формат ввода')
        amount, quote, base = data
        quote, base = quote.title(), base.title()
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'неверный формат ввода \n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n {e}')
    else:
        text = f' {amount} {quote} =  {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)