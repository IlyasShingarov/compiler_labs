from graphviz import Digraph

from syntax_tree import SyntaxTree, TreeNode


class FiniteAutomata:
    # syntax_tree: SyntaxTree
    start: list[tuple]
    end: list[tuple]
    transitions: list[tuple]

    def __init__(self, start, end, transitions) -> None:
        self.start = start
        self.end = end
        self.transitions = transitions

    @property
    def graph(self) -> Digraph:
        g = Digraph(format='png')

        g.node('S', 'Start')
        g.node('E', 'End')

        for i in self.start:
            g.edge('S', str(i))

        for i in self.end:
            g.edge(str(i), 'E')

        for f, v in self.transitions:
            for t in self.transitions[(f, v)]:
                g.node(str(f))
                g.node(str(t))
                g.edge(str(f), str(t), v)

        return g

    @classmethod
    def from_tree(cls, syntax_tree: SyntaxTree):
        start, end, trans = regex_to_finite_automata(
            syntax_tree=syntax_tree,
            alphabet=syntax_tree.alphabet
        )
        instance = cls(start, end, trans)
        return instance

    def rename_nodes(self):
        names = []

        for f, v in self.transitions:
            if f not in names:
                names += [f]
            for t in self.transitions[f, v]:
                if t not in names:
                    names += [t]

        new_transitions = {}
        for f, v in self.transitions:
            new_transitions[(names.index(f), v)] = [names.index(t) for t in self.transitions[f, v]]
        print(names)
        new_start, new_end = [names.index(t) for t in self.start], [names.index(t) for t in self.end]

        self.start = new_start
        self.end = new_end
        self.transitions = new_transitions
        return self

    def reverse(self):
        start = self.start
        end = self.end
        new_transitions = {}
        for f, v in self.transitions:
            for t in self.transitions[(f, v)]:
                if (t, v) not in new_transitions:
                    new_transitions[(t, v)] = []
                new_transitions[(t, v)] += [f]
        self.start = end
        self.end = start
        self.transitions = new_transitions
        return self

    def to_dfa(self):
        def nodes_to_state_name(l):
            return tuple(set(l))

        symbols = []
        for _, v in self.transitions:
            symbols += [v]
        symbols = list(set(symbols))

        queue = [self.start.copy()]

        new_transitions = {}
        states = []

        while len(queue):
            nodes = queue.pop()
            states.append(nodes_to_state_name(nodes))
            for c in symbols:
                state = []
                for node in nodes:
                    if (node, c) in self.transitions:
                        state += self.transitions[(node, c)]
                state = nodes_to_state_name(state)

                if not len(state):
                    continue
                new_transitions[(nodes_to_state_name(nodes), c)] = [state]

                if state not in states:
                    queue.append(state)

        def intersection(lst1, lst2):
            lst3 = [value for value in lst1 if value in lst2]
            return lst3

        new_start, new_end = [nodes_to_state_name(self.start)], [
            state for state in states if intersection(state, self.end)
        ]

        self.start = new_start
        self.end = new_end
        self.transitions = new_transitions
        return self


def regex_to_finite_automata(syntax_tree: SyntaxTree, alphabet: list, terminator: str = '#'):
    def get_state(nodes: list[TreeNode]):
        return tuple(sorted([node.index for node in nodes]))

    def is_end(nodes: list[TreeNode]):
        for node in nodes:
            if node.value == terminator:
                return True
        return False

    syntax_tree_root = syntax_tree.root

    Dstates = []
    table = {}
    queue = [syntax_tree_root.firstpos]

    last = []

    while len(queue):
        state = queue.pop()
        Dstates += [get_state(state)]

        for c in alphabet:
            U = []
            for p in state:
                if p.value == c:
                    U += p.followpos
            U = list(set(U))
            if not len(U):
                continue

            if get_state(U) not in Dstates:
                print(get_state(U))
                print(Dstates)
                queue.append(U)

            table[get_state(state), c] = [get_state(U)]
            # print(get_state(state), c, [get_state(U)])

        if is_end(state):
            last += [get_state(state)]

    return [Dstates[0]], last, table
