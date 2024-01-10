from Ascon.ascon import ascon_encrypt
from Ascon.ascon import ascon_decrypt
import os
from cryterion import cryterion
import hashlib

key = b"\xd2\x93\x10=9\xea\xd4&\x9f8Z\x04'\x17\xd6D"
nonce = b'\xc9R\xe9\xce\x05S\x99T\xd4\xa0\xd4tP)\xc6\xf0'
ad = b"ANY RANDOM DATA"
variant = 'Ascon-128'
key_size = 16
block_size = 1

def encrypt_wrapper(plaintext: bytes):
	ciphertext = ascon_encrypt(key, nonce, ad, plaintext, variant)
	return ciphertext


def decrypt_wrapper(ciphertext: bytes):
        plaintext = ascon_decrypt(key, nonce, ad, ciphertext, variant)
        return plaintext


source_files = (__file__, "Ascon/ascon.py")

if (HOST := os.getenv("RECEIVER")) is not None:
        # HOST = "192.168.166.32"
        HOST = os.getenv("RECEIVER")
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

        #print(f"\nPlaintext: {P}...")
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
        #D = cryterion.unpad(D)
        checksum = hashlib.sha256(D).hexdigest()

        print(f"\nCiphertext: {C}...")
        print(f"Plaintext: {D}...")
        print(f"Plaintext Checksum: {checksum}")
