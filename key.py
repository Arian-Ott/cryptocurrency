import ipaddress

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

# Function to generate RSA key pair
def generate_rsa_key_pair(key_size=4096):
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=key_size,
		backend=default_backend(),
		
	)
	public_key = private_key.public_key()
	return private_key, public_key

# Function to encrypt a message using RSA
def rsa_encrypt(public_key, message: bytes) -> bytes:
	ciphertext = public_key.encrypt(
		message,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return ciphertext

# Function to decrypt a message using RSA
def rsa_decrypt(private_key, ciphertext: bytes) -> bytes:
	plaintext = private_key.decrypt(
		ciphertext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return plaintext

# Function to sign a message using RSA
def rsa_sign(private_key, message: bytes) -> bytes:
	signature = private_key.sign(
		message,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)
	return signature

# Function to verify a message signature using RSA
def rsa_verify(public_key, message: bytes, signature: bytes) -> bool:
	try:
		public_key.verify(
			signature,
			message,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
		return True
	except InvalidSignature:
		return False
class Address(ipaddress.IPv6Address):
	def __init__(self, adr, pub):
		super().__init__(adr)
		self.pub = pub
		
		
		

# Example usage
if __name__ == '__main__':
	# Generate RSA keys
	private_key, public_key = generate_rsa_key_pair()

	# Serialize keys for storage or transmission
	private_pem = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.TraditionalOpenSSL,
		encryption_algorithm=serialization.NoEncryption()
	)
	public_pem = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	print("Private Key:")
	print(private_pem.decode())

	print("Public Key:")
	print(public_pem.decode())

	# Encrypt and decrypt a message
	message = b"Hello, World!"
	ciphertext = rsa_encrypt(public_key, message)
	print(f"Ciphertext: {ciphertext}")

	plaintext = rsa_decrypt(private_key, ciphertext)
	print(f"Plaintext: {plaintext.decode()}")

	# Sign and verify a message
	signature = rsa_sign(private_key, message)
	print(f"Signature: {signature}")

	verification = rsa_verify(public_key, message, signature)
	print(f"Signature valid: {verification}")
