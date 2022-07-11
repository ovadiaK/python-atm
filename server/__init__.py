import math
import os

from flask import Flask, make_response, request, jsonify

from store import create_datastore, transfer

valid_bills = {"200", "100", "20"}
valid_coins = {"10", "5", "1", "0.1", "0.01"}


def input_is_valid(money_input):
    for bill in money_input.bills:
        if bill not in valid_bills:
            return False
    for coin in money_input.coins:
        if coin not in valid_coins:
            return False
    return True


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    atm = create_datastore()

    @app.route("/health")
    def health():
        resp = make_response("pong", 200)
        return resp

    @app.route("/refill", methods=['POST'])
    def refill():
        param = request.get_json()
        input_money = transfer()
        input_money.bills = param["bills"]
        input_money.coins = param["coins"]
        if not input_is_valid(input_money):
            response = jsonify("invalid currency")
            response.status_code = 400
            return response
        atm.refill(input_money)
        return "ok"

    @app.route("/withdrawal", methods=['POST'])
    def withdraw():
        param = request.get_json()
        amount = param["amount"]
        amount = round(amount, 2)
        if amount > 2000:
            amount = 2000
        res = atm.withdraw(amount)
        if 'maximum' in res:
            response = jsonify(res)
            response.status_code = 409
            return response
        if res is 'TooManyCoinsException':
            return jsonify({"error": res}), 409
        return res

    return app

