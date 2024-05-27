from typing import Union


class Exchange:
    def __init__(self, currency, coin, exchange_rate):
        self.currency = currency
        self.coin = coin
        self.exchange_rate = exchange_rate
    def __repr__(self):
        return f"Exchange({self.currency}, {self.coin}, {self.exchange_rate})"
    def __str__(self):
        return f"({self.currency}, {self.coin}, {self.exchange_rate})"
    def __iter__(self):
        return iter((self.currency, self.coin, self.exchange_rate))
class Coin:
    magn = 1

    def __init__(self, amount: int):

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        self._amount = amount
        self._value = amount * Coin.magn

    def _getValue(self):
        return self._value

    def __repr__(self):
        return f"Coin(amount={self._value})"

    def __iadd__(self, other):
        self._value += other.getValue()
        return self

    def __isub__(self, other):
        if self._value - other.getValue() < 0:
            raise ValueError("Cannot have negative balance")
        self._value -= other.getValue()
        return self

    def __float__(self):
        return float(self._value)
    def get_money_value(self, exchange: Exchange):
        return self._value * exchange.exchange_rate

if __name__ == '__main__':
    e1 = Exchange("EUR", Coin, 2.56)
    c1 = Coin(44)
