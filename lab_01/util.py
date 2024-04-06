def fix_names(first, last, table):
    names = []

    for f, v in table:
        if f not in names:
            names += [f]
        for t in table[f, v]:
            if not t in names:
                names += [t]
    newTable = {}
    for f, v in table:
        newTable[(names.index(f), v)] = [names.index(t) for t in table[f, v]]
    return [names.index(t) for t in first], [names.index(t) for t in last], newTable


def reverse_ka(first, last, Dtran):
    newDtran = {}
    for f, v in Dtran:
        for t in Dtran[(f, v)]:
            if (t, v) not in newDtran:
                newDtran[(t, v)] = []
            newDtran[(t, v)] += [f]
    return last, first, newDtran


def to_dfa(first, last, table):
    def nodes_to_state_name(l):
        return tuple(set(l))

    symbols = []
    for _, v in table:
        symbols += [v]
    symbols = list(set(symbols))

    queue = [first.copy()]

    newTable = {}
    states = []

    while len(queue):
        nodes = queue.pop()
        states.append(nodes_to_state_name(nodes))
        for c in symbols:
            state = []
            for node in nodes:
                if (node, c) in table:
                    state += table[(node, c)]
            state = nodes_to_state_name(state)

            if not len(state):
                continue
            newTable[(nodes_to_state_name(nodes), c)] = [state]

            if state not in states:
                queue.append(state)

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    return [nodes_to_state_name(first)], [
        state for state in states if intersection(state, last)
    ], newTable


def check_ka(st, fir, las, table):
    state = fir[0]
    for c in st:
        print(state, c)
        if (state, c) not in table:
            return False
        state = table[(state, c)][0]

    return state in las