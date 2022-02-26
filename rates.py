import time
import datetime


def convert_rates(rates, value, from_currency, to_currency):
    return value / rates["rates"][from_currency] * rates["rates"][to_currency]


# Check if currency exists in rates
def currency_exists(rates, currency):
    return currency in rates["rates"]


# Get currencies rates
def get_rates():
    return get_test_rates()


# Get test currencies rates (for dev purposes)
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

