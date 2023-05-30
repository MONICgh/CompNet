from main import checksum, check_checksum

test = b'[abacabc_a;wiechrstbjrn]'
ans = 138

assert checksum(test) == ans
print('test checksum 1: OK')

assert check_checksum(bytes([ans]) + test)
print('test check_checksum 1: OK')

assert not check_checksum(bytes([ans - 8]) + test)
print('test check_checksum 2: OK')

assert not check_checksum(bytes([0]) + test)
print('test check_checksum 3: OK')