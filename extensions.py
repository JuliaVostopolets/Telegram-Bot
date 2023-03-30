import requests
import json
from config import keys
class ConvertationEcseption(Exception):
    pass

class GetPrice:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertationEcseption(f'Нельзя переводить одинаковые валюты- {base}')
        base_ticker, quote_ticker = keys[base], keys[quote]
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertationEcseption(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertationEcseption(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertationEcseption(f'Не удалось обработать количество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        price=total_base*int(amount)
        return price

