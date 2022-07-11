import math


def create_datastore():
    return datastore()


exception = "TooManyCoinsException"


class datastore:
    def __init__(self):
        self.values = [200, 100, 20, 10, 5, 1, 0.1, 0.01]
        self.bills = {"200": 7, "100": 4, "20": 15}
        self.coins = {"10": 10, "5": 1, "1": 10, "0.1": 12, "0.01": 21}

    def withdraw(self, amount):
        result = transfer()
        for currentValue in self.values:
            if currentValue <= amount:
                formatted_value = "{}".format(currentValue)
                if formatted_value in self.bills:
                    amount = self.take_money_from_bills(amount, currentValue, formatted_value, result)
                elif formatted_value in self.coins:
                    amount = self.take_money_from_coins(amount, currentValue, formatted_value, result)
        if not math.isclose(amount, 0, abs_tol=0.001):
            return {"maximum": result.amount}
        if result.coin_count > 50:
            return exception
        res = {"result": {"bills": [result.bills], "coins": [result.coins]}}
        return res

    def take_money_from_coins(self, amount, current_value, formatted_value, result):
        while self.coins[formatted_value] > 0:
            self.coins[formatted_value] -= 1
            result.coin_count += 1
            amount -= current_value
            result.amount += current_value
            if formatted_value not in result.coins:
                result.coins[formatted_value] = 1
            else:
                result.coins[formatted_value] += 1
            if amount < current_value:
                break
        return amount

    def take_money_from_bills(self, amount, current_value, formatted_value, result):
        while self.bills[formatted_value] > 0:
            self.bills[formatted_value] -= 1
            amount -= current_value
            result.amount += current_value
            if formatted_value not in result.bills:
                result.bills[formatted_value] = 1
            else:
                result.bills[formatted_value] += 1
            if amount < current_value:
                break
        return amount

    def refill(self, money_input):
        for bill in money_input.bills:
            self.bills[bill] += money_input.bills[bill]
        for coin in money_input.coins:
            self.coins[coin] += money_input.coins[coin]


class transfer:
    def __init__(self):
        self.coin_count = 0
        self.amount = 0
        self.bills = {}
        self.coins = {}
