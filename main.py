import time
import os

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from dotenv import load_dotenv
from rates import get_rates, currency_exists, convert_rates

# Load .env file variables in app
load_dotenv()

# Last update / on app start set last update before cache timeout to force load
# new rates from exchangerates api
RATES_LAST_UPDATE = int(time.time())-int(os.getenv("RATES_CACHE_TIMEOUT"))-10

# Currencies rates data object from Rest Api
RATES = get_rates()

webapp = Flask(__name__)
api = Api(webapp)


class ServerTestApi(Resource):
    def get(self):
        print("Debug: Server test")
        return {'server': 'running'}


class RatesApi(Resource):
    def get(self):
        print("Debug: Currencies requested.")
        return RATES


class RatesConvertApi(Resource):
    def get(self, from_value, from_currency, to_currency):

        # Check for from_value to be number
        try:
            from_value = int(from_value)
        except ValueError as e:
            abort(400, error="Money must be number.")

        if currency_exists(RATES, from_currency) is not True:
            abort(400, error=f"Currency from '{from_currency}' does not exist.")

        if currency_exists(RATES, to_currency) is not True:
            abort(400, error=f"Currency to '{to_currency}' does not exist.")

        # convert from one currency to other with exchange rates
        to_value = convert_rates(RATES, from_value, from_currency, to_currency)

        # send result to client
        return {"success": "true", "result": {from_currency: from_value, to_currency: to_value}}


api.add_resource(ServerTestApi, "/")
api.add_resource(RatesApi, "/rates")
api.add_resource(RatesConvertApi, "/convert/<from_value>/<from_currency>/<to_currency>")

parser = reqparse.RequestParser()
parser.add_argument("from_value")
parser.add_argument("from_currency")
parser.add_argument("to_currency")

if __name__ == "__main__":
    webapp.run(debug=True, host="0.0.0.0", port=3333)
