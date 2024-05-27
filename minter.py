from ledger import Entry, hasher


class Minter:
	def __init__(self, ledger_reader, ledger=None):
		self.reader = ledger_reader(ledger) if ledger is not None else ledger_reader
		self.current_head = "mock_ledger_head"  # Start with an initial head

	def mint(self, entry: Entry):
		# Simulate fetching the current ledger head
		ledger_head = self.current_head
		# Logic to verify transactions
		if len(entry.transactions) > 0:
			for transaction in entry.transactions:
				if not transaction.verify_transaction(transaction.addr_target.public_key):
					raise ValueError("Invalid transaction signature")
	# Simulate updating the ledger head after minting the entry
		self.current_head = self.generate_new_head(entry)
		print("Entry minted successfully. New ledger head:", self.current_head)
	def generate_new_head(self, entry):
		# This method would contain logic to generate a new ledger head,
		# possibly involving hashing the current entry along with the previous head
		return hasher(f"{self.current_head}{entry}").hexdigest()