def num2bits(num, bitlength):
    bits = []
    for i in range(int(bitlength)):
        bits.append(num & 1)
        num >>= 1
    return bits

def bits2num(bits):
    num = 0
    for i, x in enumerate(bits):
        assert x == 0 or x == 1
        num += (x << i)
    return num

def _update_round_counter(counter):
    t = 1 ^ counter[-1] ^ counter[-2]
    counter.pop()
    counter.insert(0, t)
    return counter

_sbox = (
    (0, 1, 3, 6, 7, 4, 5, 2),
    (0, 1, 7, 4, 3, 6, 5, 2),
    (0, 3, 1, 6, 7, 5, 4, 2),
    (0, 7, 3, 5, 1, 4, 6, 2),
)

def decrypt(cipherText, long_key, short_key, block_bits = 48):
    # compute length for counter
    if block_bits == 48:
        counter = [0, 0, 0, 0, 0, 0]
    elif block_bits == 96:
        counter = [0, 0, 0, 0, 0, 0, 0]
    else:
        import sys
        sys.stderr.write("ERROR: invalid block_bits\n")
        sys.exit(-1)

    iterations = 48

    counters = []

    for i in range(iterations):
        counter = _update_round_counter(counter.copy())
        counters.append(counter)


    text = num2bits(cipherText, block_bits)
    round_key = num2bits(long_key, block_bits)
    perm_key = num2bits(short_key, block_bits * 2 / 3)

    state = [None] * block_bits # temp variable

    for round in range(iterations):
        for i in range(int(block_bits / 3)):
            after = bits2num(text[3*i : 3*i + 3])
            row = bits2num(perm_key[2*i : 2*i + 2])

            column = -1
            for j in range(len(_sbox[row])):
                if (_sbox[row][j] == after):
                    column = j
                    break

            before = num2bits(column, 3)
            for k in range(3):
                state[3*i + k] = before[k]


        for county in range(len(counters[iterations - round - 1])):
            state[county] = state[county] ^ counters[iterations - round - 1][county]


        for i in range(block_bits - 1):
            text[i] = state[(3 * i) % (block_bits - 1)]
        text[block_bits - 1] = state[block_bits - 1]


        for i in range(block_bits):
            text[i] ^= round_key[i]


    return bits2num(text)

