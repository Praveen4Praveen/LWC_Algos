from Present.pypresent import Present
import os
from cryterion import cryterion
import hashlib


THUMBNAIL_SIZE = 32
# fmt: off
KEY = bytes([0x88, 0xE3, 0x4F, 0x8F, 0x08, 0x17, 0x79, 0xF1, 0xE9, 0xF3, 0x94, 0x37, 0x0A, 0xD4, 0x05, 0x89])

# Create a Camellia instance with the key
cipher = Present(KEY)

key_size = len(KEY)
block_size = 8
# cipher = ECB(
#     cryterion.int_from_bytes(bytes(KEY)),
#     key_size=key_size * 8,
#     block_size=block_size * 8,
# )

# Use cipher.encode_block and cipher.decode_block for encryption and decryption
def present_encrypt(plaintext: bytes):
    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i: i + block_size]
        encrypted_block = cipher.encrypt(block)
        ciphertext.extend(encrypted_block)

    return bytes(ciphertext)


def present_decrypt(ciphertext: bytes):
    plaintext = bytearray()

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i: i + block_size]
        decrypted_block = cipher.decrypt(block)
        plaintext.extend(decrypted_block)

    return bytes(plaintext)


source_files = (__file__, "Present/pypresent.py")


if (HOST := os.getenv("RECEIVER")) is not None:
    # HOST = "192.168.166.32"
    PORT = 8000

    P = cryterion.random_text(int(os.getenv("PLAINTEXT")))
    checksum = hashlib.sha256(P).hexdigest()

    P = cryterion.pad(P, block_size)
    C = cryterion.encrypt(
        lambda plaintext: present_encrypt(plaintext),
        P,
        key_size,
        block_size,
        cryterion.code_size_from_files(source_files),
    )

    cryterion.sendall(bytes(C), HOST, PORT)

    print(f"\nPlaintext: {P}...")
    print(f"Ciphertext: {bytes(C)}...")
    print(f"Plaintext Checksum: {checksum}")
else:
    HOST = "0.0.0.0"
    PORT = 8000

    C = cryterion.recvall(HOST, PORT)

    D = cryterion.decrypt(
        lambda ciphertext: present_decrypt(ciphertext),
        C,
        key_size,
        block_size,
        cryterion.code_size_from_files(source_files),
    )
    D = cryterion.unpad(D)
    checksum = hashlib.sha256(D).hexdigest()

    print(f"\nCiphertext: {C}...")
    print(f"Plaintext: {D}...")
    print(f"Plaintext Checksum: {checksum}")
