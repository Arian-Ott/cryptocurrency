from Block import Block
from transact import Transaction
import time
class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 100

    def create_genesis_block(self):
        # Create an initial block with no transactions
        return Block('0', [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        if not self.pending_transactions:
            raise ValueError("No transactions to mine")

        reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
        block_transactions = self.pending_transactions + [reward_tx]

        block = Block(self.get_latest_block().hash, block_transactions, time.time())
        block.mine_block(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(block)

        # Clear pending transactions after mining
        self.pending_transactions = []

    def add_transaction(self, transaction):
        if not transaction.sender or not transaction.recipient:
            raise ValueError("Transaction must include sender and recipient")
        if not transaction.is_valid():
            raise ValueError("Cannot add invalid transaction to chain")

        sender_balance = self.get_balance(transaction.sender)
        if transaction.amount > sender_balance:
            raise ValueError(f"Not enough balance. Current balance: {sender_balance}")

        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.sender == address:
                    balance -= trans.amount
                if trans.recipient == address:
                    balance += trans.amount
        return balance
