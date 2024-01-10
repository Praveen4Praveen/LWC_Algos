from kyber import Kyber512
pk, sk = Kyber512.keygen()
c, key = Kyber512.enc(pk)
print(key)
_key = Kyber512.dec(c, sk)
print(_key)
assert key == _key
