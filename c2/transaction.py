from Coin import Exchange
from key import rsa_encrypt, rsa_sign
from key import  Address
class Transaction:
    def __init__(self, sender: Address, sender_private_key, recipient:Address, amount):
        self._sender = sender
        self._sender_private_key = sender_private_key
        self._recipient = recipient
        self._amount = amount
        from datetime import time
        self._timestamp = time()
        if 
    
            