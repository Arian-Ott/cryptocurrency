from Balance import Wallet
from key import Address, generate_rsa_key_pair
import transaction
if __name__ == '__main__':
    private_key_user1, public_key_user1 = generate_rsa_key_pair()
    private_key_user2, public_key_user2 = generate_rsa_key_pair()

    # Create addresses for users
    addr1 = Address("2001:db8::1", public_key_user1)
    addr2 = Address("2001:db8::2", public_key_user2)
    w1 = Wallet(addr1, initial_balance=5)
    w2 = Wallet(addr2, initial_balance=2)
    t1 = transaction.Transaction(addr1,private_key_user1,w1, w2,2)
    print(repr(w1))
