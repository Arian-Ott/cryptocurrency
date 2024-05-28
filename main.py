import random
from tqdm import tqdm
from key import Key

from Blockchain import Blockchain
from transaction import Transaction


def test_key_class():
    key_instance = Key()
    message = "Test message"
    signature = key_instance.sign(message)
    assert key_instance.verify(
        message, signature, key_instance.get_public_key()
    ), "Key class test failed"
    print("Key class test passed")


def test_transaction_class():
    sender_key = Key()
    recipient_key = Key()
    tx = Transaction(sender_key.get_public_key(), recipient_key.get_public_key(), 10)
    tx.sign_transaction(sender_key)
    assert tx.verify_transaction(
        sender_key.get_public_key()
    ), "Transaction class test failed"
    print("Transaction class test passed")


def test_blockchain_class():
    blockchain = Blockchain(difficulty=2)
    sender_key = Key()
    recipient_key = Key()

    tx1 = Transaction(sender_key.get_public_key(), recipient_key.get_public_key(), 10)
    tx1.sign_transaction(sender_key)
    blockchain.add_transaction(tx1)

    blockchain.mine_pending_transactions(sender_key.get_public_key())

    print(
        "Balance of recipient:", blockchain.get_balance(recipient_key.get_public_key())
    )


def setup_initial_balances(blockchain, sender_key, initial_balance):
    # Create a transaction that initializes the sender's balance
    genesis_transaction = Transaction(
        None, sender_key.get_public_key(), initial_balance
    )
    blockchain.pending_transactions.append(genesis_transaction)
    blockchain.mine_pending_transactions(sender_key.get_public_key())


def test_blockchain_class():
    blockchain = Blockchain(difficulty=2)
    sender_key = Key()
    recipient_key = Key()

    # Setup initial balance
    setup_initial_balances(blockchain, sender_key, 1000)

    tx1 = Transaction(sender_key.get_public_key(), recipient_key.get_public_key(), 10)
    tx1.sign_transaction(sender_key)
    blockchain.add_transaction(tx1)

    # Mine pending transactions
    blockchain.mine_pending_transactions(sender_key.get_public_key())

    print(
        "Balance of recipient:", blockchain.get_balance(recipient_key.get_public_key())
    )


test_key_class()
test_transaction_class()
test_blockchain_class()


def main():
    blockchain = Blockchain(difficulty=2)
    sender_key = Key()
    recipient_key = Key()
    other_miners = [Key() for _ in tqdm(range(30))]
    # Setup initial balance
    setup_initial_balances(blockchain, sender_key, 1000)

    for i in range(500):
        tx = Transaction(
            sender_key.get_public_key(), recipient_key.get_public_key(), 10
        )
        tx.sign_transaction(sender_key)
        blockchain.add_transaction(tx)
        mnr = random.choice(other_miners).get_public_key()
        blockchain.mine_pending_transactions(mnr)

        print(f"Iteration {i + 1}:")
        print("Balance of miner", blockchain.get_balance(mnr))

        print("Balance of sender:", blockchain.get_balance(sender_key.get_public_key()))
        print(
            "Balance of recipient:",
            blockchain.get_balance(recipient_key.get_public_key()),
        )


if __name__ == "__main__":
    main()
