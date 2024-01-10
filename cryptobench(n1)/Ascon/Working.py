from ascon import *
import time

start = time.time()

debug = False
debugpermutation = False

variant='Ascon-128'
key_size=16

# Key Set
# inp=input("Press 0 to use a random Key or 1 if you want to enter a key:")
# if(inp==1):
#     key=input('Enter the Key 16 Character long:')
# if(inp==0):
#     key   = get_random_bytes(key_size)
key   = get_random_bytes(key_size)

# Nonce Set
# inp=input("Press 0 to use a random Nonce or 1 if you want to enter a Nonce:")
# if(inp==1):
#     nonce=input('Enter the Key 16 Character long:')
# if(inp==0):
#     nonce   = get_random_bytes(16)

nonce   = get_random_bytes(16)
# Associated Data

ad = b"ANY RANDOM DATA"

#Plaintext:

file=open("pt.txt",'rb')

plaintext=file.read()

ciphertext        = ascon_encrypt(key, nonce, ad, plaintext,  variant)
receivedplaintext = ascon_decrypt(key, nonce, ad, ciphertext, variant)

#Writting to text Files:
file2=open("ct.txt",'w')

file2.write(str(ciphertext))


file3=open("rpt.txt",'w')

file3.write(str(receivedplaintext))

end = time.time()

print("The time of execution of above program is :",(end-start) * 10**3, "ms")


