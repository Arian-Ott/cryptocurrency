from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import uuid
import hashlib


class Key:
    def __init__(self, passphrase: str | None):


        if isinstance(passphrase, str):
            self._passphrase = self._passwd_hash(passphrase)

        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4098)
        self.public_key = self.private_key.public_key()
        self.id = uuid.uuid4().hex

    def _passwd_hash(self, passphrase):
        if passphrase == None or len(passphrase) <= 8:
            raise ValueError("Passphrase invalid or None")

        return hashlib.sha512(
            hashlib.blake2s(hashlib.sha512(passphrase.encode('utf-8'), usedforsecurity=True).hexdigest().encode(),
                            digest_size=32).hexdigest().encode(), usedforsecurity=True)

    def get_public_key(self):
        return self.public_key

    def sign(self, message, passphrase):
        if not self._passphrase == self._passwd_hash(passphrase):
            raise InvalidSignature('Passphrase')

        # Use SHA-256 instead of SHA-1
        return self.private_key.sign(message.encode('utf-8'), padding.PKCS1v15(), hashes.SHA256())

    def verify(self, message, signature, public_key):
        try:
            # Use SHA-256 instead of SHA-1
            public_key.verify(signature, message.encode('utf-8'), padding.PKCS1v15(), hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    def __str__(self):
        return str(self.id)
