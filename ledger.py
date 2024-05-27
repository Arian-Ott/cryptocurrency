import hashlib
from math import log10, floor
from ipaddress import IPv6Address
from functools import reduce
from typing import Union, List

# Utility Variables
hasher = hashlib.sha224
z_len = 5
AddressType = IPv6Address


class Address(AddressType):
    def __init__(self, address: str, public_key=None):
        super().__init__(address)
        self.public_key = public_key
		self._private_key = 


# Utility Functions
def is_float(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_hexadecimal(num: str) -> bool:
    try:
        int(num, 16)
        return True
    except ValueError:
        return False


class Coin:
    magn = 12

    def _getval(self, val: Union[int, float, str, 'Coin']) -> int:
        if isinstance(val, int):
            return val * 10 ** self.magn
        elif isinstance(val, float) or (isinstance(val, str) and is_float(val)):
            return self._convert_float_or_str(val)
        elif isinstance(val, Coin):
            return val.value
        else:
            raise TypeError("Type has not been defined")

    def _convert_float_or_str(self, val: Union[float, str]) -> int:
        val_str = str(val)
        spl = val_str.split(".")
        sign = -1 if spl[0].startswith('-') else 1
        spl[0] = spl[0].lstrip('-')

        integer_part = int(spl[0]) * 10 ** self.magn if spl[0] else 0
        fractional_part = 0

        if len(spl) > 1 and spl[1]:
            fractional_part = reduce(
                lambda x, y: x * 10 + y,
                [int(i) for i in spl[1].ljust(self.magn, '0')[:self.magn]]
            )

        return sign * (integer_part + fractional_part)

    def __init__(self, value: Union[int, float, str, 'Coin'], _raw: bool = False):
        if _raw and isinstance(value, int):
            self.value = value
        else:
            self.value = self._getval(value)

    def __repr__(self) -> str:
        s = "-" if self.value < 0 else ""
        value = abs(self.value)
        s += str(int(value / 10 ** self.magn)) + '.' if value >= 10 ** self.magn else '0.'
        if value % (10 ** self.magn) != 0:
            s += '0' * (self.magn - (int(floor(log10(value % (10 ** self.magn))) + 1)))
            s += str(value % (10 ** self.magn)).rstrip('0')
        return s

    def __str__(self) -> str:
        return "£" + self.__repr__()

    def __iadd__(self, other: Union[int, float, str, 'Coin']) -> 'Coin':
        self.value += self._getval(other)
        return self

    def __isub__(self, other: Union[int, float, str, 'Coin']) -> 'Coin':
        self.value -= self._getval(other)
        return self

    def __add__(self, other: Union[int, float, str, 'Coin']) -> 'Coin':
        return Coin(self.value + self._getval(other), _raw=True)

    def __sub__(self, other: Union[int, float, str, 'Coin']) -> 'Coin':
        return Coin(self.value - self._getval(other), _raw=True)

    @classmethod
    def one(cls) -> 'Coin':
        return cls(1)

    @classmethod
    def frac(cls) -> 'Coin':
        return cls(1, _raw=True)




def is_address(address: str) -> bool:
    try:
        Address(address)
        return True
    except ValueError:
        return False


def validate_amount(amount: Union[int, float, str, Coin]) -> Coin:
    return amount if isinstance(amount, Coin) else Coin(amount)


def validate_addr(address: Union[str, Address], name: str) -> Address:
    if isinstance(address, Address):
        return address
    elif isinstance(address, AddressType):
        return Address(str(address))
    else:
        raise ValueError(f"{name} is not a valid address")


from c2.key import rsa_sign, rsa_verify


class Transaction:
    def __init__(self, addr_src: Union[str, Address], addr_target: Union[str, Address],
                 amount: Union[int, float, str, Coin], private_key=None):
        self.addr_src = validate_addr(addr_src, "Source")
        self.addr_target = validate_addr(addr_target, "Target")
        self.amount = validate_amount(amount)
        if private_key:
            self.signature = self.sign_transaction(private_key)
        else:
            self.signature = None

    def sign_transaction(self, private_key):
        data = str(self.addr_src) + str(self.addr_target) + str(self.amount)
        return rsa_sign(private_key, data.encode())

    def verify_transaction(self, public_key):
        data = str(self.addr_src) + str(self.addr_target) + str(self.amount)
        return rsa_verify(public_key, data.encode(), self.signature)

    def __repr__(self) -> str:
        return f"A{self.addr_src}A{self.addr_target}C{str(self.amount)}S{self.signature}"


class Entry:
    num_t = 60  # Number of transactions
    num_h = 6  # Number of hashes required
    sum_r = 6  # Reward given for successful hashing
    assert num_t % 10 == 0

    def __init__(self, reward_addr: Union[str, Address] = None, head: str = None, transactions=None,
                 hashnums=None, z_len: int = z_len):
        if transactions is None:
            transactions = []
        if hashnums is None:
            hashnums = []
        self.reward_addr = validate_addr(reward_addr, "Reward Address") if reward_addr else None
        self.head = head
        self.transactions = list(transactions)
        self.hashnums = list(hashnums)
        self.z_len = z_len

    def check_hash(self, h_val: int, chunk: List[str]) -> bool:
        batch = f'RA{self.reward_addr}R{self.sum_r}HEAD{self.head}' + "\n".join(chunk) + str(h_val)
        return hasher(batch.encode('utf-8')).hexdigest().startswith('0' * self.z_len)

    def validate(self) -> bool:
        if len(self.transactions) != self.num_t:
            return False
        if len(self.hashnums) != self.num_t // 10:
            return False
        if not isinstance(self.reward_addr, Address) or not is_address(str(self.reward_addr)):
            return False
        if not isinstance(self.head, str) or len(self.head) != hasher().digest_size * 2 or not is_hexadecimal(
                self.head):
            return False
        for i in range(len(self.hashnums)):
            chunk = list(map(str, self.transactions[i * 10:(i + 1) * 10]))
            if not self.check_hash(self.hashnums[i], chunk):
                return False
        return True

    def get_remaining(self) -> int:
        return self.num_t - len(self.transactions)

    def add_transaction(self, transaction: Transaction):
        if self.get_remaining() > 0:
            self.transactions.append(transaction)
        else:
            raise ValueError("Transaction limit reached")

    def __repr__(self) -> str:
        return f"Entry(reward_addr={self.reward_addr}, head={self.head}, transactions={self.transactions}, hashnums={self.hashnums})"
