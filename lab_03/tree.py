from typing import Self
from lexer import Token

class TreeNode:
    data = ""
    children: list[Self]
    from_ = -1
    to_ = -1

    def __init__(self, data) -> None:
        self.data = data
        self.children = []

    @staticmethod
    def from_token(token: Token):
        return TreeNode(token.value)


    def add_child(self, node: Self):
        if not len(self.children):
            self.from_ = node.from_
        self.to_ = node.to_

        if node.data == ['<composition>']:
            for ch in node.children:
                self.add_child(ch)
            return
        
        self.children.append(node)
    
    def print(self, tree = None, parent="", id = "main"):
        from graphviz import Digraph
        if not tree:
            tree = Digraph()
            tree.node_attr["shape"] = "plain"
        tree.node(id, str(self.data))
        if parent:
            tree.edge(parent, id)
        
        # print("IN:",  self.data, [ch.data for ch in self.children])
        for i, child in enumerate(self.children):
            child.print(tree, id, id + "." + str(i))
        # print("OUT:",  self.data, [ch.data for ch in self.children])
            
        return tree