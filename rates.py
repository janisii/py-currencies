import time
import datetime
from requests import get


# delete currency
def delete_currency(rates, currency):
    if currency_exists(rates, currency) is not True:
        return False

    del rates["rates"][currency]
    return True


# update currency with new rate
def update_currency_rate(rates, currency, new_rate):
    if currency_exists(rates, currency) is not True:
        return False

    rates["rates"][currency] = new_rate
    return True


# add new custom currency and rate
def add_currency_rate(rates, new_currency, new_rate):
    if currency_exists(rates, new_currency) is True:
        return False

    rates["rates"][new_currency] = new_rate
    return True


# convert money from one currency to other
def convert_rates(rates, value, from_currency, to_currency):
    return value / rates["rates"][from_currency] * rates["rates"][to_currency]


# Check if currency exists in rates
def currency_exists(rates, currency):
    return currency in rates["rates"]


# Get currencies rates
def get_rates(env, api_access_key=''):
    if env == 'dev':
        return get_test_rates()
    if env == 'prod':
        return get_api_rates(api_access_key)


# Get rates latest timestamp
def get_rates_latest_timestamp(rates):
    if "timestamp" in rates:
        return rates["timestamp"]

    return 0


# Get actual currencies rates from ExchangeRatesApi (prod env)
def get_api_rates(api_access_key):
    exchange_rates_request = get("http://api.exchangeratesapi.io/v1/latest?access_key=" + api_access_key + "&format=1")

    if exchange_rates_request.status_code != 200:
        return None

    exchange_rates_data = exchange_rates_request.json()

    if exchange_rates_data["success"] is not True:
        return None

    return exchange_rates_data


# Get test currencies rates (dev env)
def get_test_rates():
    rates = {
        "success": "true",
        "timestamp": int(time.time()),
        "base": "EUR",
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "rates": {
            "BTC": 0.000028869014,
            "EUR": 1,
            "GBP": 0.841179,
            "LVL": 0.681871,
            "RUB": 94.535583,
            "USD": 1.127263,
        }
    }
    return rates
