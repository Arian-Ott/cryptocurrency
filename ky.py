from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
class Key:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4098)
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        return self.public_key

    def sign(self, message):
        # Use SHA-256 instead of SHA-1
        return self.private_key.sign(message.encode('utf-8'), padding.PKCS1v15(), hashes.SHA256())

    def verify(self, message, signature, public_key):
        try:
            # Use SHA-256 instead of SHA-1
            public_key.verify(signature, message.encode('utf-8'), padding.PKCS1v15(), hashes.SHA256())
            return True
        except InvalidSignature:
            return False

