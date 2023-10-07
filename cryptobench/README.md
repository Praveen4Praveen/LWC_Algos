## Notes
- Compares 41 existing symmetric key lightweight cryptography (plain encryption) algorithms over 7 performance metrics (Block/Key size, Memory, Gate Area, Latency, Throughput, Power & Energy requirements along with hardware and soft- ware efficiency) as recommended by the NIST report for resource-constrained IoT devices.

## Instructions
```
# Run in terminal after SSH if [backspace doesn't work](https://unix.stackexchange.com/a/45473).
export TERM=vt100

rsync -Pa --exclude __pycache__ --exclude arena cryptobench btp@192.168.166.32:~/

PYTHONPATH="$PYTHONPATH:./cyclops" python hight_test_CBC.py
```

## Dependencies
- `pip install hwcounter`

## References
- <https://singleboardbytes.com/289/connect-wi-fi-enable-ssh-without-monitor-raspberry-pi.htm>
- <https://github.com/Daksh-Axel/Midori128-64/tree/main/App>
- [Midori: A Block Cipher for Low Energy](https://eprint.iacr.org/2015/1142.pdf)

### SIMON and SPECK
- <https://github.com/inmcm/Simon_Speck_Ciphers/tree/master/Python/simonspeckciphers>
- [The SIMON and SPECK Families of Lightweight Block Ciphers](https://eprint.iacr.org/2013/404)
- <https://github.com/bozhu/NSA-ciphers/>
