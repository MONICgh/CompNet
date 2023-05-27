from random import randint

addr_list = set(['.'.join(
    [str(randint(0, 255)) for _ in range(4)]
    ) for _ in range(5)])

nodes = {addr: {} for addr in addr_list}
for addr in addr_list:
    for dif_addr in addr_list:
        if not(addr == dif_addr or randint(0, 99) >= 20):
            nodes[dif_addr][addr] = (addr, 1)
            nodes[addr][dif_addr] = (dif_addr, 1)


print(f'{"[Source IP]":25} {"[Connections]":25}')
for addr in addr_list:
    print(f'{addr:25} [{", ".join(nodes[addr])}]')

