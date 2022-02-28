import time
import os

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from dotenv import load_dotenv
from rates import *
from requests import post

# Load .env file variables in app
load_dotenv()

# .env variables
RATES_CACHE_TIMEOUT = os.getenv('RATES_CACHE_TIMEOUT')
RATES_API_ACCESS_KEY = os.getenv('RATES_API_ACCESS_KEY')
ENV = os.getenv('ENV')
PORT = os.getenv('PORT')

# Currencies with rates data object
RATES_DATA = get_rates(ENV, RATES_API_ACCESS_KEY)


webapp = Flask(__name__)
api = Api(webapp)


class ServerTestApi(Resource):
    # test server is running
    def get(self):
        print("Debug: Server test")
        return {'server': 'running', 'app': 'currency converter'}


class RatesApi(Resource):
    # get list of currencies
    def get(self):
        print("Debug: Currencies requested.")
        return RATES_DATA

    # add new currency and rate
    def post(self):
        args = parser.parse_args()
        print("Debug: Add new currency with rate.")

        # Currency name should be uppercase and 3 chars in length
        new_currency = args["new_currency"].upper()[0:3]
        new_rate = args["new_rate"]

        try:
            new_rate = float(new_rate)
        except ValueError as e:
            abort(400, error="Rate must be float.")

        if currency_exists(RATES_DATA, new_currency) is True:
            abort(400, error=f"Currency '{new_currency}' already exists.")

        add_currency_rate(RATES_DATA, new_currency, new_rate)
        return {"success": "true", "result": {new_currency: new_rate, "rates": RATES_DATA["rates"]}}

    # update existing currency with new rate
    def put(self):
        args = parser.parse_args()
        print("Debug: Update currency with new rate.")

        # Currency name should be uppercase and 3 chars in length
        currency = args["currency"].upper()[0:3]
        new_rate = args["new_rate"]

        try:
            new_rate = float(new_rate)
        except ValueError as e:
            abort(400, error="Rate must be float.")

        if currency_exists(RATES_DATA, currency) is not True:
            abort(400, error=f"Currency '{currency}' does not exists.")

        update_currency_rate(RATES_DATA, currency, new_rate)
        return {"success": "true", "result": {currency: new_rate, "rates": RATES_DATA["rates"]}}, 201

    # delete existing currency
    def delete(self):
        args = parser.parse_args()
        print("Debug: Delete currency.")

        currency = args["currency"].upper()

        if currency_exists(RATES_DATA, currency) is not True:
            abort(400, error=f"Currency '{currency}' does not exists.")

        delete_currency(RATES_DATA, currency)
        return {"success": "true", "result": {"rates": RATES_DATA["rates"]}}, 204


class RatesResetApi(Resource):
    # get list of currencies
    def post(self):
        print("Debug: Reset currencies list.")
        RATES_DATA = get_rates(ENV, RATES_API_ACCESS_KEY)
        return RATES_DATA


class RatesConvertApi(Resource):
    def get(self, from_value, from_currency, to_currency):
        global RATES_DATA

        if get_rates_latest_timestamp(RATES_DATA) + int(RATES_CACHE_TIMEOUT) < int(time.time()):
            print("Debug: Cache timeout. Rates updated.")
            RATES_DATA = get_rates(ENV, RATES_API_ACCESS_KEY)

        from_currency = from_currency.upper()[0:3]
        to_currency = to_currency.upper()[0:3]

        # Check for from_value to be number
        try:
            from_value = float(from_value)
        except ValueError as e:
            abort(400, error="Money must be number.")

        if currency_exists(RATES_DATA, from_currency) is not True:
            abort(400, error=f"Currency from '{from_currency}' does not exist.")

        if currency_exists(RATES_DATA, to_currency) is not True:
            abort(400, error=f"Currency to '{to_currency}' does not exist.")

        # convert from one currency to other with exchange rates
        to_value = convert_rates(RATES_DATA, from_value, from_currency, to_currency)

        # send result to client
        return {"success": "true", "result": {from_currency: from_value, to_currency: to_value}}


api.add_resource(ServerTestApi, "/")
api.add_resource(RatesApi, "/rates")
api.add_resource(RatesResetApi, "/rates/reset")
api.add_resource(RatesConvertApi, "/convert/<from_value>/<from_currency>/<to_currency>")

parser = reqparse.RequestParser()
parser.add_argument("currency")
parser.add_argument("from_value", type=float, help="Money value must be number.")
parser.add_argument("from_currency")
parser.add_argument("to_currency")
parser.add_argument("new_currency")
parser.add_argument("new_rate", type=float, help="Rate value must be float.")

if __name__ == "__main__":
    webapp.run(debug=True, host="0.0.0.0", port=PORT)
