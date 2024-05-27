from Coin import Coin
from key import rsa_encrypt
from key import Address
from transaction import  Transaction
class Balance:
    def __init__(self, account: Address):
        self.account = account
        self._public_key = self.account.pub
        self._amount = self._modify_balance(0)
        
        
    def _modify_balance(self, value):
        return rsa_encrypt(self._public_key, value)
    
    def transact(self, transation: Transaction):
        
        
        
        