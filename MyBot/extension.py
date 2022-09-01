import requests
import json
from config import allcurrency, API_KEY


class CurrencyExchangeError(Exception):
    pass

class Converter:

    @staticmethod
    def inputhandling(values):
        try:
            # Check: формат ввода
            if len(values) != 3:
                raise CurrencyExchangeError(f"Неверный формат ввода")
            base_, target_, amount_ = values
            # Check: корректность ввода исходной валюты
            if allcurrency.get(base_) is None:
                raise CurrencyExchangeError(f"Ошибка ввода валюты '{base_}'")
            # Check: корректность ввода целевой валюты
            elif allcurrency.get(target_) is None:
                raise CurrencyExchangeError(f"Ошибка ввода валюты '{target_}'")
            # Check: идентичность валют
            elif base_ == target_:
                raise CurrencyExchangeError(f"Невозможна конвертация одной и той же валюты '{base_}'")
            # Check: корректность ввода числа
            try:
                amount_ = float(amount_.replace(",", "."))
            except ValueError:
                raise CurrencyExchangeError(f"Некорректный ввод количества '{amount_}'")

        except CurrencyExchangeError as err:
            return {"error": err}

    @staticmethod
    def getpricehandling(base_ , target_ , amount):
        base, target = allcurrency[base_], allcurrency[target_]
        get_url = f"https://api.apilayer.com/exchangerates_data/convert?to={target}&from={base}&amount={amount}&" \
                  f"apikey={API_KEY}"
        try:
            resp = requests.request("GET", get_url)
        except requests.ConnectionError:
            err = f"Ошибка ответа сервера. Попробуйте позже."
            return {"error": err}
        else:
            text_resp = json.loads(resp.content)
            target_amount = text_resp['result']
            return {"target_result": target_amount}

