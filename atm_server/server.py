from flask import Flask, request, jsonify

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

    atm = create_datastore()

    @app.route("/health")
    def health():
        return "pong", 200

    @app.route("/refill", methods=['POST'])
    def refill():
        input_money = parse_refill_input()
        if not input_is_valid(input_money):
            return jsonify("invalid currency"), 400
        atm.refill(input_money)
        return "ok"

    @app.route("/withdrawal", methods=['POST'])
    def withdraw():
        amount = parse_withdrawal_input()
        res = atm.withdraw(amount)
        if 'maximum' in res:
            return jsonify(res), 409
        if res is 'TooManyCoinsException':
            return jsonify({"error": res}), 409
        return res

    return app


def parse_withdrawal_input():
    param = request.get_json()
    amount = param["amount"]
    amount = round(amount, 2)
    if amount > 2000:
        amount = 2000
    return amount


def parse_refill_input():
    param = request.get_json()
    input_money = transfer()
    input_money.bills = param["bills"]
    input_money.coins = param["coins"]
    return input_money