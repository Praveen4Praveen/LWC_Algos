from cyclops import Cyclops, cycles
from time import sleep


assert Cyclops().cycles == 0

with Cyclops() as c:
    x = sum(list(range(10_000)))

print(f"{c.cycles = } cycles")
