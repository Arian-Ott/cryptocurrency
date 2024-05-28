from Coin import Coin
from key import rsa_encrypt, generate_rsa_key_pair
from key import Address

from transaction import Transaction
class Wallet:
    def __init__(self, account: Address, initial_balance=0):

        self.account = account
        self._public_key_account = self.account.pub
        self._public_key = generate_rsa_key_pair()
        self._private_key_account = rsa_encrypt(self._public_key_account, str(self._public_key[0]).encode())
        self.public_key = self._public_key[1]
        self._amount = initial_balance
    def transact(self, transaction, modifier):
        if modifier == 0:
            if self._amount < 0:
                self._amount = -self._amount
            self._amount +=transaction.amount
        elif modifier ==1:
            if self._amount < 0:
                self._amount = -self._amount
            if self._amount - transaction.amount < 0:
                raise RuntimeError("Transaction amount exceeds balance")
            self._amount -= transaction.amount


    def _modify_balance(self, value):
        return rsa_encrypt(self._public_key, value)
    def __str__(self):
        return str(self.public_key)
    def __repr__(self):
        return f"Wallet(public_key={self.public_key}, amount={self._amount})"
    def balance(self):
        return self._amount

    def __sub__(self, other):

        if (self._amount - float(other)) >= 0:
            self._amount = self._amount - float(other)
            return self._amount
        raise RuntimeError("Cannot subtract a value higher than the balance")


        
        
        
        