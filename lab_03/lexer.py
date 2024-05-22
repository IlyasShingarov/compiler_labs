class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.current_token = None
        self.tokenize()

    def tokenize(self):
        # This is a very simplified tokenizer for demonstration.
        tokens = []
        tokens = (self.input.replace('{', ' { ')  
                            .replace('}', ' } ') 
                            .replace(';', ' ; ')  
                            .replace('(', ' ( ')  
                            .replace(')', ' ) ')  
                            .split())
        
        self.tokens = [Token(self.identify_type(token), token)
                       for token in tokens]
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def identify_type(self, token):
        if token in {'==', '<>', '<', '<=', '>', '>='}:
            return 'RELATION_OP'
        elif token in {'+', '-', 'or'}:
            return 'ADD_OP'
        elif token in {'*', '/', 'div', 'mod', 'and'}:
            return 'MULT_OP'
        elif token in {'not'}:
            return 'KEYWORD'
        elif token == '{':
            return 'LBRACE'
        elif token == '}':
            return 'RBRACE'
        elif token == '(':
            return 'LPAREN'
        elif token == ')':
            return 'RPAREN'
        elif token == ';':
            return 'SEMICOLON'
        elif token == '=':
            return 'ASSIGN'
        elif token.isdigit():
            return 'CONST'
        elif token.isalpha():
            return 'IDENT'
        else:
            return 'UNKNOWN'

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def expect(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            print(f'Consumed token {self.current_token.value} of type {token_type}')
            token = self.current_token
            self.advance()
            return token
        else:
            raise Exception(f"Expected token {token_type}, but got {self.current_token.type if self.current_token else 'None'}")
