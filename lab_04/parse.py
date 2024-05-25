from lexer import Lexer, Token
from tree import TreeNode

'''
Сделано частично
<expression'>       -> <relation op> <s-expression> | ε
<s-expression>      -> <term> <term rest> | <sign> <term> <term rest>
<term rest>         -> <s-expression'> | ε
<s-expression'>     -> <add op> <term> <s-expression'> | ε
<term>              -> <factor> <term'>
<term'>             -> <mult op> <factor> <term'> | ε

<factor>            -> <ident> | <const> | ( <s-expression> ) | not <factor>

<relation op>       -> = | <> | < | <= | > | >=
<add op>            -> + | - | or
<mult op>           -> * | / | div | mod | and


<sign>              -> + | -
<ident> -- terminal
<const> -- terminal
'''

class Parser:
    
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.output = []

    def parse(self):
        return self.expression()

    def expression(self):
        '''
        <expression> -> <s-expression> <expression'>
        '''
        print('Parsing expression')
        self.s_expression()
        self.expression_prime()
    
    def expression_prime(self):
        '''
        <expression'> -> <relation op> <s-expression> | ε
        '''
        print('Parsing expression prime')
        if self.lexer.current_token.type == 'RELATION_OP':
            op = self.relation_operation()
            self.s_expression()
            self.output.append(op.value)


    def s_expression(self):
        '''
        <s-expression> -> 
                |   <term> <term rest> 
                |   <sign> <term> <term rest>
        '''
        print('Parsing simple expression')
        if self.lexer.current_token.value in ['+', '-']:
            sign = self.sign_operation()
            self.term()
            self.term_rest()
            self.output.append(sign.value)
        else:
            self.term()
            self.term_rest()

    def term_rest(self):
        '''
        <term rest> -> <s-expression'> | ε
        '''
        print('Parsing term rest')
        self.s_expression_prime()

    def s_expression_prime(self):
        '''
        <s-expression'> -> <add op> <term> <s-expression'> | ε
        '''
        print('Parsing simple expression prime')
        if self.lexer.current_token.type == 'ADD_OP':
            op = self.addition_operation()
            self.term()
            self.output.append(op.value)
            self.s_expression_prime()

    def term(self):
        '''
        <term> -> <factor> <term'>
        '''
        print('Parsing term')
        self.factor()
        self.term_prime()
        
    
    def term_prime(self):
        '''
        <term'> -> <mult op> <factor> <term'> | ε
        '''
        print('Parsing term prime')
        if self.lexer.current_token.type == 'MULT_OP':
            op = self.multiplication_operation()
            self.factor()
            self.output.append(op.value)
            self.term_prime()

    def factor(self):
        '''
        <factor> -> 
                |   <ident> 
                |   <const> 
                |   ( <s-expression> ) 
                |   not <factor>
        '''
        print('Parsing factor')
        if self.lexer.current_token.type == 'IDENT':
            self.output.append(self.identifier().value)
        elif self.lexer.current_token.type == 'CONST':
            self.output.append(self.constant().value)
        elif self.lexer.current_token.type == 'LPAREN':
            self.lexer.advance()
            self.s_expression()
            self.lexer.expect('RPAREN')
        elif self.lexer.current_token.type == 'NOT':
            kw = self.keyword()
            self.factor()
            self.output.append(kw.value)
    
    def relation_operation(self) -> TreeNode:
        '''
        <relation op> -> = | <> | < | <= | > | >=
        '''
        # FIXME
        rel_op = TreeNode('<операция отношения>')
        terminal = self.lexer.expect('RELATION_OP')
        print(f'Matched relation operation: {terminal.value}')
        rel_op.add_child(TreeNode.from_token(terminal))
        return rel_op

    def addition_operation(self) -> TreeNode:
        '''
        <add op> -> + | - | or
        '''
        terminal = self.lexer.expect('ADD_OP')
        print(f'Matched addition operation: {terminal.value}')
        return terminal

    def multiplication_operation(self) -> TreeNode:
        '''
        <mult op> -> * | / | div | mod | and
        '''
        terminal = self.lexer.expect('MULT_OP')
        print(f'Matched operation: {terminal.value}')
        return terminal

    def keyword(self) -> TreeNode:
        terminal = self.lexer.expect('KEYWORD')
        print(f'Matched keyword: {terminal.value}')
        return terminal

    def constant(self) -> TreeNode:
        terminal = self.lexer.expect('CONST')
        print(f'Matched constant: {terminal.value}')
        return terminal

    def identifier(self) -> TreeNode:
        terminal = self.lexer.expect('IDENT')
        print(f'Matched identifier: {terminal.value}')
        return terminal




def main():
#     text = """
#     1 + 2 + 3 - 2
# """
    text = """
    a + (b + c) * d - e
"""
#     text = """
# {
#     a = b + 1
# }
# """
    lex = Lexer(text)
    print([token.value for token in lex.tokens])
    print([token.type for token in lex.tokens])
    parser = Parser(lex)
    parser.parse()
    print(' '.join(parser.output))
    
if __name__ == '__main__':
    main()