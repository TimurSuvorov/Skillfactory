import os
from dotenv import load_dotenv

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Не найден файл переменных окружения '.env'")

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("APIKEY")


allcurrency = {"доллар": "USD",
               "рубль": "RUB",
               "евро": "EUR",
               "лари": "GEL",
               "драм": "AMD",
               "биткоин": "BTC",
               "юань": "CNY",
               "така": "BDT",
               "песо": "ARS",
               }
