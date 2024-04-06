from functools import cached_property
from typing import Self
from binarytree import Node as BTNode


class TreeNode:
    value: str
    left: Self
    right: Self
    index: int

    def __init__(self, value: str, left: Self = None, right: Self = None, index: int = None):
        self.value = value
        self.left = left
        self.right = right
        self.index = index
        self.firstpos = None
        self.nullable = None
        self.lastpos = None
        self.followpos = []

    # @cached_property
    def count_nullable(self) -> bool:
        if self.left:
            self.left.count_nullable()
        if self.right:
            self.right.count_nullable()

        if self.value == '*':
            self.nullable = True
        elif self.value == '|':
            self.nullable = self.left.nullable or self.right.nullable
        else:
            self.nullable = False
        return self.nullable
        # if self.value == '|':
        #     return self.left.is_nullable() or self.right.is_nullable()
        # elif self.value == '*':
        #     return True
        # elif self.value == '.':
        #     return self.left.is_nullable() and self.right.is_nullable()
        # else:
        #     return False

    # @cached_property
    def count_firstpos(self) -> list[Self]:
        if self.left:
            self.left.count_firstpos()
        if self.right:
            self.right.count_firstpos()

        if self.value in ['*', '+']:
            self.firstpos = self.left.firstpos.copy()
        elif self.value == '.':
            self.firstpos = self.left.firstpos.copy()
            if self.left.nullable:
                self.firstpos += self.right.firstpos
        elif self.value == '|':
            self.firstpos = self.left.firstpos + self.right.firstpos
        else:
            self.firstpos = [self]
        return self.firstpos

        # if self.value == '|':
        #     return self.left.firstpos().copy() + self.right.firstpos().copy()
        # elif self.value == '*':
        #     return self.left.firstpos().copy()
        # elif self.value == '.':
        #     return self.left.firstpos().copy() + self.right.firstpos().copy() \
        #         if self.left.is_nullable() else self.left.firstpos().copy()
        # else:
        #     return [self]

    # @cached_property
    def count_lastpos(self) -> list[Self]:
        if self.left:
            self.left.count_lastpos()
        if self.right:
            self.right.count_lastpos()

        if self.value in ['*', '+']:
            self.lastpos = self.left.lastpos.copy()
        elif self.value == '.':
            self.lastpos = self.right.lastpos.copy()
            if self.right.nullable:
                self.lastpos += self.left.lastpos
        elif self.value == '|':
            self.lastpos = self.left.lastpos + self.right.lastpos
        else:
            self.lastpos = [self]
        return self.lastpos
        # if self.value == '|':
        #     return self.left.lastpos().copy() + self.right.lastpos().copy()
        # elif self.value == '*':
        #     return self.left.lastpos().copy()
        # elif self.value == '.':
        #     return self.left.lastpos().copy() + self.right.lastpos().copy() \
        #         if self.right.is_nullable() else self.right.lastpos().copy()
        # else:
        #     return [self]

    def count_followpos(self):
        if self.left:
            self.left.count_followpos()
        if self.right:
            self.right.count_followpos()
        if self.value == '.':
            for i in self.left.lastpos:
                i.followpos += self.right.firstpos
        elif self.value == '*':
            for i in self.lastpos:
                i.followpos += self.firstpos

    # @cached_property
    def firstpos_index(self) -> list[int]:
        return list(map(lambda node: node.index, self.firstpos))

    # @cached_property
    def lastpos_index(self) -> list[int]:
        return list(map(lambda node: node.index, self.lastpos))

    def print_tree(self) -> None:
        print(to_binarytree_index(self))

    def view(self):
        print(to_binarytree(self))

    def __repr__(self) -> str:
        return f'{self.index}'

    def __str__(self, level=0, prefix="Root: ") -> str:
        ret = " " * (level * 2) + prefix + self.value + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, f":L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, f"R--- ")
        return ret


def to_binarytree_index(node: TreeNode) -> BTNode | None:
    """Converts custom Node to binarytree.Node for visualization."""
    if node is None:
        return None
    bt_node = BTNode(str(
        f"{node.firstpos_index()} "
        f"[{node.value}{':' + str(node.index) if node.index is not None else ""}] "
        f"{node.lastpos_index()}\t{node.nullable}"
    ))
    bt_node.left = to_binarytree_index(node.left)
    bt_node.right = to_binarytree_index(node.right)
    return bt_node


def to_binarytree(node: TreeNode) -> BTNode | None:
    """Converts custom Node to binarytree.Node for visualization."""
    if node is None:
        return None
    bt_node = BTNode(str(
        f"[{node.value}{':' + str(node.index) if node.index is not None else ""}] "
    ))
    bt_node.left = to_binarytree(node.left)
    bt_node.right = to_binarytree(node.right)
    return bt_node


def parse_regex(regular_expression: str) -> tuple[TreeNode, int]:
    """Parse the regular expression into a syntax tree."""

    def parse_expression(input_list: list[str] | str):
        """Parse alternation."""
        node = parse_sequence(input_list)
        while input_list and input_list[0] == '|':
            op = input_list.pop(0)
            rhs = parse_sequence(input_list)
            node = TreeNode(op, node, rhs)
        return node

    def parse_sequence(input_list: list[str] | str):
        """Parse concatenation."""
        node = parse_factor(input_list)
        while input_list and input_list[0] not in '|)':
            rhs = parse_factor(input_list)
            node = TreeNode('.', node, rhs)  # Use '.' to represent concatenation
        return node

    def parse_factor(input_list: list[str] | str):
        """Parse literals and Kleene stars."""
        if input_list[0] == '(':
            input_list.pop(0)  # Remove '('
            node = parse_expression(input_list)  # Parse subexpression
            input_list.pop(0)  # Remove ')'
        else:
            nonlocal index
            node = TreeNode(input_list.pop(0), index=index)  # Literal
            # print(f'{node.value} - {node.index}')
            index += 1

        if input_list and input_list[0] == '*':
            node = TreeNode(input_list.pop(0), node)  # Apply Kleene star
        return node

    index = 1
    return parse_expression(list(regular_expression)), index


def get_leaf_nodes_rec(node: TreeNode, acc: list) -> list[TreeNode]:
    if node.value == '*':
        return acc + get_leaf_nodes_rec(node.left, acc)
    elif node.index is not None:
        return acc + [node]
    else:
        return acc + get_leaf_nodes_rec(node.left, acc) + get_leaf_nodes_rec(node.right, acc)


def get_leaf_nodes(tree_root: TreeNode) -> list[TreeNode]:
    return get_leaf_nodes_rec(tree_root, [])


def get_alphabet(nodes: list):
    return list(map(lambda node: node.value, nodes))


class SyntaxTree:
    root: TreeNode
    leaf_count: int
    followpos_list: list[list[TreeNode]] | list[None]

    def __init__(self, expr: str):
        self.root, self.leaf_count = parse_regex(expr)
        self.root.count_nullable()
        self.root.count_lastpos()
        self.root.count_firstpos()
        self.root.count_followpos()
        print(self.root.followpos)
        # self.followpos_list = [None for i in range(self.leaf_count - 1)]
        # self.followpos(self.root)

    # def followpos(self, node: TreeNode):
    #     if node.value == '.':
    #         for i in map(lambda n: n.index, node.left.lastpos):
    #             if self.followpos_list[i - 1]:
    #                 self.followpos_list[i - 1] = list(set(self.followpos_list[i - 1] + node.right.firstpos))
    #             else:
    #                 self.followpos_list[i - 1] = node.right.firstpos
    #
    #         self.followpos(node.left)
    #         self.followpos(node.right)
    #
    #     elif node.value == '*':
    #         for i in map(lambda n: n.index, node.lastpos):
    #             if self.followpos_list[i - 1]:
    #                 self.followpos_list[i - 1] = list(set(self.followpos_list[i - 1] + node.firstpos))
    #             else:
    #                 self.followpos_list[i - 1] = node.firstpos
    #         self.followpos(node.left)
    #     return self.followpos_list

    # def get_followpos(self, node):
    #     fp = self.followpos_list[node.index - 1]
    #     return fp if fp is not None else []

    # @cached_property
    # def followpos_list_index(self):
    #     return list(
    #         map(lambda fp: list(map(lambda node: node.index, fp)) if fp is not None else None, self.followpos_list)
    #     )

    @cached_property
    def leaf_nodes(self):
        return get_leaf_nodes_rec(self.root, [])

    @cached_property
    def alphabet(self):
        return list(set(map(lambda node: node.value, self.leaf_nodes)))

    def print_tree(self):
        self.root.print_tree()

    def view(self):
        self.root.view()
