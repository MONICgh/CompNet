#first type
def checksum(data, mod=8):
    step, summ = mod // 8, 0

    for i in range(0, len(data), step):
        summ += int.from_bytes(
            data[i:i + step],
            'big'
        )
    
    summ = (2 ** mod - 1) - summ % (2 ** mod)
    return summ


#second type
def check_checksum(data, mod=8):
    step, summ = mod // 8, 0

    for i in range(0, len(data), step):
        summ += int.from_bytes(
            data[i:i + step],
            'big'
        )

    summ %= (2 ** mod)
    return summ == (2 ** mod - 1)
