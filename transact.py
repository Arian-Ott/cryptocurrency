from ky import Key
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def is_valid(self):
        return self.sender and self.recipient and self.amount > 0

    def sign_transaction(self, private_key):
        if self.sender == private_key.get_public_key():
            self.signature = private_key.sign(self.to_string())
        else:
            raise ValueError("You cannot sign transactions for other wallets!")

    def verify_transaction(self, public_key):
        if not self.signature:
            raise ValueError("No signature in this transaction!")
        return Key().verify(self.to_string(), self.signature, public_key)

    def to_string(self):
        return f'{self.sender}{self.recipient}{self.amount}'
