import time
import hashlib
class Block:
    def __init__(self, previous_hash, transactions, timestamp=None):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            f'{self.previous_hash}{[tx.to_string() for tx in self.transactions]}{self.timestamp}{self.nonce}'.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()