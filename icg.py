import ply.lex as lex
import ply.yacc as yacc
import graphviz
import uuid
from graphviz import Digraph

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
)

t_ignore = ' \t\n\r' # ignore whitespace and tabs

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    keywords = {'if', 'else', 'print'}
    t.type = 'KEYWORD' if t.value in keywords else 'IDENTIFIER'
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_OPERATOR(t):
    r'[\+\-\*/=<>\!]=?|!='
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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Parser rules

def p_program(p):
    '''program : statement_list'''
    p[0] = ('PROGRAM', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement : expression_statement
                 | var_declaration
                 | if_statement
                 | print_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression DELIMITER'''
    p[0] = ('EXPRESSION_STATEMENT', p[1])

def p_expression(p):
    '''expression : primary_expression
                  | binary_expression'''
    p[0] = p[1]

def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                          | NUMBER'''
    p[0] = ('PRIMARY_EXPRESSION', p[1])

def p_binary_expression(p):
    '''binary_expression : expression OPERATOR expression'''
    p[0] = ('BINARY_EXPRESSION', p[1], p[2], p[3])

def p_var_declaration(p):
    '''var_declaration : IDENTIFIER DELIMITER'''
    p[0] = ('VAR_DECLARATION', p[1])

def p_if_statement(p):
    '''if_statement : IF expression block'''
    p[0] = ('IF_STATEMENT', p[2], p[3])

def p_if_else_statement(p):
    '''if_statement : IF expression block ELSE block'''
    p[0] = ('IF_ELSE_STATEMENT', p[2], p[3], p[5])

def p_block(p):
    '''block : DELIMITER statement_list DELIMITER'''
    p[0] = ('BLOCK', p[2])

def p_print_statement(p):
    '''print_statement : PRINT expression DELIMITER'''
    p[0] = ('PRINT_STATEMENT', p[2])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

# Build the parser
parser = yacc.yacc()

# Define graph
def add_node(node, parent):
    global count
    count += 1
    if isinstance(node, tuple):
        dot.node(str(count), node[0])
        dot.edge(parent, str(count))
        for n in node[1:]:
            add_node(n, str(count))
    else:
        dot.node(str(count), str(node))
        dot.edge(parent, str(count))


# Define a function that will create a unique filename for the graph
def get_uuid():
    return str(uuid.uuid4())

# Define a function that will create the graph
def create_graph(ast):
    global dot
    dot = Digraph(comment='Abstract Syntax Tree')
    dot.format = 'png'
    count = 0
    dot.node(str(count), 'PROGRAM')
    for node in ast[1]:
        add_node(node, '0')
    filename = get_uuid() + '.png'
    dot.render(filename, view=True)
    return filename


# Test the parser
if __name__ == '__main__':
    ast = parser.parse('''
        var x;
        x = 5;
        if (x == 5) {
            print "x is 5";
        } else {
            print "x is not 5";
        }
    ''')
    print(create_graph(ast))
