from get_nodes import nodes

def out_console(is_final, step, g):
    for node in g:
        if is_final:
            print(
                f'Final state (step {step}) of router',
                node,
                'table:'
            )
        elif step == 0:
            print(
                f'Start state (step {step}) of router',
                node,
                'table:'
            )
        else:
            print(
                f'Simulation (step {step}) of router',
                node,
                'table:'
            )
        print(f'{"[Source IP]":25} {"[Destination IP]":25} {"[Next Hop]":25} {"[Metric]":7} {"":5}')
        
        if len(g[node]) == 0:
            print()
            continue

        for connection in g[node]:
            print(f'{node:25} {connection:25} {g[node][connection][0]:25} {"":7} {g[node][connection][1]}')
        print()


is_used = True
step = 0

while is_used:
    out_console(False, step, nodes)

    is_used = False
    for node in nodes:
        for v in nodes[node]:
            if nodes[node][v][1] == 1:
                for u in nodes[node]:
                    if v == u:
                        continue
                    if (u not in nodes[v] or nodes[node][u][1] < nodes[v][u][1] - 1):
                        nodes[v][u] = (
                            node,
                            nodes[node][u][1] + 1
                        )
                        is_used = True
    step += 1

out_console(True, step, nodes)