import time
import hashlib
import uuid

import main2

class Block:
    def __init__(self, previous_hash, transactions, timestamp=None):
        self._id = uuid.uuid4().hex
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha512(
            f'{self.previous_hash}{[tx.to_string() for tx in self.transactions]}{self.timestamp}{self.nonce}{self._id}'.encode(),usedforsecurity=True).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()