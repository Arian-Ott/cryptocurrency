
from key import rsa_encrypt, rsa_sign
from key import  Address

class Transaction:
    def __init__(self, sender: Address, sender_private_key, sender_wallet, recipient, amount):
        self._sender = sender
        self._sender_wallet = sender_wallet
        self._sender_private_key = sender_private_key
        self._recipient = recipient
        self.amount = amount

        self._sender_wallet.transact(self, 1)

        self._recipient.transact(self,0)


    def get_transaction_value(self):
        return self.amount
    def __call__(self, other):
        return
    def __str__(self):
        return  rsa_encrypt(public_key=self._recipient.public_key, message=self.get_transaction_value()), rsa_sign(self._sender_private_key,rsa_encrypt(public_key=self._recipient.public_key, message=self.get_transaction_value()) )

    def __float__(self):
        return self.amount


    
            