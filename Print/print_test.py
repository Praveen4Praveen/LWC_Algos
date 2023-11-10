from Print.encrypt import encrypt as print_encrypt
from Print.decrypt import decrypt as print_decrypt
import os
from cryterion import cryterion
import hashlib


MODE = "ECB"
THUMBNAIL_SIZE = 32
# fmt: off
KEY = [0xC2, 0x88, 0x95, 0xBA, 0x32, 0x7B]
PERMKEY = [0x69, 0xD2, 0xCD, 0xB6]
# fmt: on

key_size = len(KEY) + len(PERMKEY)
block_size = 6


def encrypt_wrapper(plaintext: bytes):
	key = int("0x" + bytes(KEY).hex(), 16)
	permkey = int("0x" + bytes(PERMKEY).hex(), 16)
	ciphertext = bytearray()

	for i in range(0, len(plaintext), block_size):
		block = int("0x" + plaintext[i : i + block_size].hex(), 16)
		state = print_encrypt(block, key, permkey)

		ciphertext.extend(state.to_bytes(block_size, byteorder='big'))

	return bytes(ciphertext)

def decrypt_wrapper(ciphertext: bytes):
	key = int("0x" + bytes(KEY).hex(), 16)
	permkey = int("0x" + bytes(PERMKEY).hex(), 16)
	plaintext = bytearray()

	for i in range(0, len(ciphertext), block_size):
		block = int("0x" + ciphertext[i : i + block_size].hex(), 16)
		state = print_decrypt(block, key, permkey)
		plaintext.extend(state.to_bytes(block_size, byteorder='big'))

	return bytes(plaintext)


source_files = (__file__, "Print/encrypt.py", "Print/decrypt.py")

if (HOST := os.getenv("RECEIVER")) is not None:
	# HOST = "192.168.166.32"
	PORT = 8000

	P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
	checksum = hashlib.sha256(P).hexdigest()

	print(f"\nPlaintext: {P}...")
	P = cryterion.pad(P, block_size)
	C = cryterion.encrypt(
		lambda plaintext: encrypt_wrapper(plaintext),
		P,
		key_size,
		block_size,
		cryterion.code_size_from_files(source_files),
	)


	cryterion.sendall(bytes(C), HOST, PORT)
	print(f"Ciphertext: {bytes(C)}...")
	print(f"Plaintext Checksum: {checksum}")
else:
	HOST = "0.0.0.0"
	PORT = 8000

	C = cryterion.recvall(HOST, PORT)
	D = cryterion.decrypt(
                lambda ciphertext: decrypt_wrapper(ciphertext),
                C,
                key_size,
                block_size,
                cryterion.code_size_from_files(source_files)
        )
	#print(f"Plaintext: {D}...")

	D = cryterion.unpad(D)
	checksum = hashlib.sha256(D).hexdigest()

	print(f"\nCiphertext: {C}...")
	print(f"Plaintext: {D}...")
	print(f"Plaintext Checksum: {checksum}")
