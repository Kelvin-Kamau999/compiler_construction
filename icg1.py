import ply.lex as lex
import ply.yacc as yacc

# Define the tokens
tokens = (
    'IDENTIFIER',
    'KEYWORD',
    'NUMBER',
    'OPERATOR',
    'DELIMITER',
    'STRING',
    'IF',
    'ELSE',
    'PRINT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULO',
)

# Define the precedence of the operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
)

# Define the keywords
keywords = {
    'if', 'else', 'print', 'int', 'float', 'string', 'bool', 'true', 'false',
    'and', 'or', 'not'
}

# Define the tokens using regular expressions
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ignore = ' \t\n\r'  # Ignore whitespace and tabs


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'KEYWORD' if t.value in keywords else 'IDENTIFIER'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_OPERATOR(t):
    r'[\+\-\*/%=<>!]=?|\|\||&&'
    return t


def t_DELIMITER(t):
    r'[;,\(\)\[\]\{\}]'
    return t


def t_STRING(t):
    r'"[^"]*"'
    return t


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_PRINT(t):
    r'print'
    return t


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Define the AST nodes
class Node:
    def __init__(self, type, *args):
        self.type = type
        self.children = args


class BinOp(Node):
    def __init__(self, op, left, right):
        super().__init__('BIN_OP', left, right)
        self.op = op


class UnOp(Node):
    def __init__(self, op, expr):
        super().__init__('UN_OP', expr)
        self.op = op


class IntVal(Node):
    def __init__(self, value):
        super().__init__('INT_VAL')
        self.value = value


class FloatVal(Node):
    def __init__(self, value):
        super().__init__('FLOAT_VAL')
        self.value = value


class StrVal(Node):
    def __init__(self, value):
        super().__init__('STR_VAL')
        self.value = value


class BoolVal(Node):
    def __init__(self, value):
        super().__init__('BOOL_VAL')
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        super().__init__('IDENTIFIER')
        self.name = name


class VarDecl(Node):
    def __init__(self, var_type, identifier):
        super().__init__('VAR_DECL')
        self.var_type = var_type
        self.identifier = identifier


class Assignment(Node):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr

    def __repr__(self):
        return f"{self.identifier} = {self.expr}"

    def generate_code(self):
        code = ""
        code += self.expr.generate_code()
        code += f"STORE {self.identifier}\n"
        return code

# ***
class BinaryOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

    def generate_code(self):
        code = ""
        code += self.left.generate_code()
        code += self.right.generate_code()

        if self.operator == "+":
            code += "ADD\n"
        elif self.operator == "-":
            code += "SUBTRACT\n"
        elif self.operator == "*":
            code += "MULTIPLY\n"
        elif self.operator == "/":
            code += "DIVIDE\n"
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

        return code


# ****
class Number(Node):
    def init(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def generate_code(self):
        return f"PUSH {self.value}\n"



class Identifier(Node):
    def __init__(self, value):
        self.value = value

    # ***
    def __repr__(self):
        return self.value

    def generate_code(self):
        return f"LOAD {self.value}\n"


# ****
class Print(Node):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"print({self.expr})"
    
    def generate_code(self):
        code = ""
        code += self.expr.generate_code()
        code += "PRINT\n"
        return code

