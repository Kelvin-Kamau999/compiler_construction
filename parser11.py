import ply.yacc as yacc

# Get the token map from the lexerfile

from lexering import tokens

# Define the grammar rules
def p_statement_assign(p):
    'statement : ID ASSIGN expression EOL'
    p[0] = ('ASSIGN', p[3], "to", p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = (p[1], p[2], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INT
                  | FLOAT
                  | ID'''
    p[0] = p[1]

def p_statement_if(p):
    'statement : IF expression LBRACE statements RBRACE'
    p[0] = ('IF', p[2], p[4])

def p_statement_else(p):
    'statement : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE'
    p[0] = ('ELSE', p[2], p[4], p[8])

def p_statement_while(p):
    'statement : WHILE expression LBRACE statements RBRACE'
    p[0] = ('WHILE', p[2], p[4])

def p_statement_print(p):
    'statement : PRINT expression EOL'
    p[0] = ('PRINT', p[2])

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_error(p):
    print(f"SyntaxError: Invalid syntax at line {p.lineno-1}")

# Build parser
parser = yacc.yacc()

# Test parser with sample input
data = '''
 IF (x < 10) {
    print("x is less than 10");
}

 else {
    print("x is greater than or equal to 10");
}
'''

# Parse the input
result = parser.parse(data)

# Print the result
print(result)
