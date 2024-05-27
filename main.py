from ledger import Coin, Address, Transaction, Entry
from c2.key import generate_rsa_key_pair
from minter import Minter

# Generate RSA keys for two users
private_key_user1, public_key_user1 = generate_rsa_key_pair()
private_key_user2, public_key_user2 = generate_rsa_key_pair()

# Create addresses for users
addr1 = Address("2001:db8::1", public_key_user1)
addr2 = Address("2001:db8::2", public_key_user2)

# Create Coins
coin1 = Coin(1234)
coin2 = Coin("56.78")

# Create transactions
transaction1 = Transaction(addr1, addr2, coin1, private_key_user1)
transaction2 = Transaction(addr2, addr1, coin2, private_key_user2)
print(transaction2)
# Create an Entry with transactions
entry = Entry(reward_addr=addr1, head="mock_ledger_head", transactions=[transaction1, transaction2])


# Mock ledger reader with simple get_head function
class MockLedgerReader:
    def __init__(self):
        pass

    def get_head(self):
        return "mock_ledger_head"


# Initialize Minter with the mock ledger reader
ledger_reader_instance = MockLedgerReader()
minter = Minter(ledger_reader_instance)

# Mint the entry
minter.mint(entry)

# Print transactions to show the output
print(entry.transactions)
