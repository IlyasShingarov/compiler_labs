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

    def parse(self) -> TreeNode:
        return self.program()
    
    def program(self) -> TreeNode:
        '''
        <program> -> <block>
        '''
        print('Parsing program')
        tree = TreeNode('<программа>')
        tree.add_child(self.block())
        return tree
    
    def block(self) -> TreeNode:
        '''
        <block> -> { <operator list> }
        '''
        print('Parsing block')
        block = TreeNode('<блок>')
        
        lbrace = self.lexer.expect('LBRACE')
        block.add_child(TreeNode.from_token(lbrace))
        
        ops = self.operator_list()
        block.add_child(ops)
        
        rbrace = self.lexer.expect('RBRACE')
        block.add_child(TreeNode.from_token(rbrace))
        
        return block

    def operator_list(self) -> TreeNode:
        '''
        <operator list> -> <operator> <tail>
        '''
        print('Parsing operator list')
        oplist = TreeNode('<список операторов>')
        
        operator = self.operator()
        oplist.add_child(operator)
        
        tail = self.tail()
        if tail: oplist.add_child(tail)
        
        return oplist

    def operator(self) -> TreeNode:
        '''
        <operator> -> <identifier> = <expression> | <block>
        '''
        print('Parsing operator')
        operator = TreeNode('оператор')
        if self.lexer.current_token.type == 'IDENT':
            ident = self.identifier()
            operator.add_child(ident)
            
            assign = self.lexer.expect('ASSIGN')
            operator.add_child(TreeNode.from_token(assign))
            
            expression = self.expression()
            operator.add_child(expression)
            return operator
        elif self.lexer.current_token.type == 'LBRACE':
            print('Matched block')
            return self.block()
        else:
            raise Exception(f'Unexpected token: {self.lexer.current_token.type}')
    
    def tail(self) -> TreeNode | None:
        '''
        <tail> -> ; <operator> <tail> | ε | ;
        '''
        tail = TreeNode('<хвост>')
        if self.lexer.current_token.type == 'SEMICOLON':
            semicolon = self.lexer.expect('SEMICOLON')
            tail.add_child(TreeNode.from_token(semicolon))

            if self.lexer.current_token.type == 'RBRACE':
                return tail

            operator = self.operator()
            tail.add_child(operator)

            rec_tail = self.tail()
            if rec_tail: tail.add_child(rec_tail)

            return tail

    def expression(self) -> TreeNode:
        '''
        <expression> -> <s-expression> <expression'>
        '''
        print('Parsing expression')
        expression = TreeNode('<выражение>')
        s_expression = self.s_expression()
        expression.add_child(s_expression)
        expression_prime = self.expression_prime()
        if expression_prime: expression.add_child(expression_prime)
        return expression
    
    def expression_prime(self) -> TreeNode | None:
        '''
        <expression'> -> <relation op> <s-expression> | ε
        '''
        print('Parsing expression prime')
        expression_prime = TreeNode("<выражение'>")
        if self.lexer.current_token.type == 'RELATION_OP':
            rel_op = self.relation_operation()
            expression_prime.add_child(rel_op)

            s_expression = self.s_expression()
            expression_prime.add_child(s_expression)

            return expression_prime

    def s_expression(self) -> TreeNode:
        '''
        <s-expression> -> 
                |   <term> <term rest> 
                |   <sign> <term> <term rest>
        '''
        print('Parsing simple expression')
        s_expression = TreeNode('<простое выражение>')
        if self.lexer.current_token.value in ['+', '-']:
            sign = self.lexer.current_token.value
            self.lexer.advance()
        
        term = self.term()
        s_expression.add_child(term)
        term_rest = self.term_rest()
        if term_rest: s_expression.add_child(term_rest)
        return s_expression

    def term_rest(self) -> TreeNode | None:
        '''
        <term rest> -> <s-expression'> | ε
        '''
        print('Parsing term rest')
        term_rest = TreeNode('<терм хвост>')
        s_expression_prime = self.s_expression_prime()
        if s_expression_prime: 
            term_rest.add_child(s_expression_prime)
            return term_rest

    def s_expression_prime(self) -> TreeNode | None:
        '''
        <s-expression'> -> <add op> <term> <s-expression'> | ε
        '''
        print('Parsing simple expression prime')
        s_expression_prime = TreeNode("<простое выражение'>")
        if self.lexer.current_token.type == 'ADD_OP':
            add_op = self.lexer.expect(self.lexer.current_token.type)
            s_expression_prime.add_child(TreeNode.from_token(add_op))
            
            term = self.term()
            s_expression_prime.add_child(term)
            
            rec_s_expression = self.s_expression_prime()
            if rec_s_expression: s_expression_prime.add_child(rec_s_expression)

            return s_expression_prime

    def term(self) -> TreeNode:
        '''
        <term> -> <factor> <term'>
        '''
        print('Parsing term')
        term = TreeNode('<терм>')
        
        factor = self.factor()
        term.add_child(factor)
        
        term_prime = self.term_prime()
        if term_prime: term.add_child(term_prime)
        
        return term
    
    def term_prime(self) -> TreeNode | None:
        '''
        <term'> -> <mult op> <factor> <term'> | ε
        '''
        print('Parsing term prime')
        term_prime = TreeNode("<терм'>")
        if self.lexer.current_token.type == 'MULT_OP':
            mult_op = self.multiplication_operation()
            term_prime.add_child(mult_op)

            factor = self.factor()
            term_prime.add_child(factor)

            rec_term_prime = self.term_prime()
            if rec_term_prime: term_prime.add_child(rec_term_prime)

    def factor(self) -> TreeNode:
        '''
        <factor> -> 
                |   <ident> 
                |   <const> 
                |   ( <s-expression> ) 
                |   not <factor>
        '''
        print('Parsing factor')
        factor = TreeNode('<фактор>')
        if self.lexer.current_token.type == 'IDENT':
            ident = self.identifier()
            factor.add_child(ident)
            return factor
        elif self.lexer.current_token.type == 'CONST':
            const = self.constant()
            factor.add_child(const)
        elif self.lexer.current_token.type == 'LPAREN':
            lparen = self.lexer.expect(self.lexer.current_token.type)
            factor.add_child(TreeNode.from_token(lparen))

            s_expression = self.s_expression()
            factor.add_child(s_expression)

            rparen = self.lexer.expect('RPAREN')
            factor.add_child(TreeNode.from_token(rparen))
        elif self.lexer.current_token.type == 'KEYWORD':
            nt = self.keyword()
            factor.add_child(nt)

            rec_factor = self.factor()
            if rec_factor: factor.add_child(rec_factor)
        
        return factor
    
    def relation_operation(self) -> TreeNode:
        '''
        <relation op> -> = | <> | < | <= | > | >=
        '''
        rel_op = TreeNode('<операция отношения>')
        terminal = self.lexer.expect('RELATION_OP')
        print(f'Matched relation operation: {terminal.value}')
        rel_op.add_child(TreeNode.from_token(terminal))
        return rel_op

    def addition_operation(self) -> TreeNode:
        '''
        <add op> -> + | - | or
        '''
        add_op = TreeNode('<операция типа сложения>')
        terminal = self.lexer.expect('ADD_OP')
        print(f'Matched addition operation: {terminal.value}')
        add_op.add_child(TreeNode.from_token(terminal))
        return add_op

    def multiplication_operation(self) -> TreeNode:
        '''
        <mult op> -> * | / | div | mod | and
        '''
        mult_op = TreeNode('<операция типа умножения>')
        terminal = self.lexer.expect('MULT_OP')
        print(f'Matched operation: {terminal.value}')
        mult_op.add_child(TreeNode.from_token(terminal))
        return mult_op

    def keyword(self) -> TreeNode:
        terminal = self.lexer.expect('KEYWORD')
        print(f'Matched keyword: {terminal.value}')
        return TreeNode(terminal.value)

    def constant(self) -> TreeNode:
        const = TreeNode('<константа>')
        terminal = self.lexer.expect('CONST')
        print(f'Matched constant: {terminal.value}')
        const.add_child(TreeNode.from_token(terminal))
        return const

    def identifier(self) -> TreeNode:
        ident = TreeNode('<идентификатор>')
        terminal = self.lexer.expect('IDENT')
        print(f'Matched identifier: {terminal.value}')
        ident.add_child(TreeNode.from_token(terminal))
        return ident




def main():
    # test_list = [
    #     # '{ x = 10; y = x + 20 }',
    #     # '{ a = 5; { b = a + 10 }; c = b * 2 }',
        
    #     # '{ x = 100; y = 200; z = (x < y) or not (x = 200) }',
    #     # '{ x = ( 1 + 2 ) }',
    #     # '{ x = 10 / 0; y = (x + 100) and (x - 200) }',

    #     # '{ a = 5 + 3; b = a - 2; c = b * 4; d = c / 2; e = d mod 2; f = 20 div 3; g = (a + b) and (c - d); h = not e == 0 }',
    #     # '{ x = - y + 5; z = (x * (y - 2)) div 3; w = not (z + 10) or (x - 0) }',
    # ]

    # for test in test_list:
    #     print(test)
    #     lex = Lexer(test)
    #     tkns = [f'{token.value} : {token.type}' for token in lex.tokens]
    #     for tkn in tkns: print(tkn)
    #     parser = Parser(lex)
    #     parser.parse()

    text = """
{ 
    a = 2 + 3;
    c = 4;
}
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
    tree = parser.parse()
    tree.print().render()
    



if __name__ == '__main__':
    main()