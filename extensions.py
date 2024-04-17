import requests
import json
from config import values


class ConvertException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertException(f'нельзя перевести {quote} в {base}')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise ConvertException(f'нет валюты {quote}')

        try:
            base_ticker = values[base]
        except KeyError:
            raise ConvertException(f'нет валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'введите число вместо {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[values[base]]) * amount
        return total_base