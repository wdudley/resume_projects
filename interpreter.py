#!/usr/bin/env python
# coding: utf-8

# * Class:        CS 4308 Section 2
# * Term:         Spring 2020
# * Name:         Brandon Dudley, Giant Nguyen, Austin Bennett
# * Instructor:   Deepa Muralidhar
# * Project:      Deliverable 3 Executable - Python

# Libraries needed
# pip install sly
from sly import Lexer
from sly import Parser

# Lexer class
class LexerBasic(Lexer):
    # Initialize tokens, igrnoed characters and literals
    tokens = {LET, INPUT, IF, GOTO, END, NAME, STRING, LOGICALEQUALS, LOGICALNOTEQUALS, NUMBER, NEWLINE, INT, PRINT}
    ignore = ' \t,'
    literals = {'+', '-', '*', '/', '=', ':', ';',  '(', ')', '<', '>' }
    
    # Ignore comment lines and comment blocks
    @_(r'\d+ REM .*\n+')
    def COMMENT(self, t):
        pass
    
    @_(r'TEXT .*')
    def TEXT(self, t):
        pass
    
    # Define tokens
    LET = r'LET'
    INPUT = r'INPUT'
    IF = r'IF'
    GOTO = r'GOTO'
    END = r'END'
    INT = r'INT'
    PRINT = r'PRINT'
    LOGICALEQUALS = r'\=\='
    LOGICALNOTEQUALS = r'\<\>'
    STRING = r'\"([^\\\n]|(\\.))*?\"'
    NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    # Define a number and convert it to an integer
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    # Define a newline token to help keep track of line numbers for syntax error reporting
    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += len(t.value)
        return t
    
    # Print a message to indicate lexing errors
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

# Parser class
class ParserBasic(Parser):
    # Recieve the tokens list from the Lexer class
    tokens = LexerBasic.tokens
    
    # A simple function to print syntax errors and where they occured
    def print_error(self, line, index, msg):
        print("Syntax error at line " + str(line) + ' index ' + str(index), "\n", str(msg))

    # Define arithmetic precedence
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = {}
        
# GRAMMAR RULES
#  <lines> ::=      NUMBER statement NEWLINE lines
#                 | NUMBER statement NEWLINE
#                 | NUMBER statement
#                 | NUMBER END
#  <statement> ::=  IF ( condition ) statement
#                 | var_assign
#                 | PRINT expr
#                 | PRINT NAME NAME
#                 | expr
#  <condition> ::=  expr (</</<>/==) expr
#  <var_assign> ::= INPUT NAME;
#                 | LET NAME = expr
#  <expr>       ::= expr (+/-/*//) expr
#                 | INT ( expr )
#                 | ( expr )
#                 | -expr
#                 | (NUM / NAME / STRING)
            
 # Grammars
    #-----LINES------
    @_('NUMBER statement NEWLINE lines')
    def lines(self, p):
        return ('line', p.statement, p.lines)
    
    @_('NUMBER statement NEWLINE')
    def lines(self, p):
        return ('line', p.statement)
    
    @_('NUMBER statement')
    def lines(self, p):
        return ('line', p.statement)
    
    @_('NUMBER END NEWLINE')
    def lines(self, p):
        return 'end'
    
    @_('NUMBER END')
    def lines(self, p):
        return 'end'
    
    @_('NUMBER error statement NEWLINE')
    def lines(self, p):
        print("Expected line number 1" )
        
    @_('NAME error NEWLINE')
    def lines(self, p):
        print("Expected line number 2" )
        
    @_('NAME')
    def lines(self, p):
        self.print_error(p.lineno, p.index, "Invalid variable declaration " + '\'' + p.NAME + '\'')
        
    @_('NUMBER')
    def lines(self, p):
        self.print_error(p.lineno, p.index, "Invalid statement " + '\'' + str(p.NUMBER) + '\'')

    #-----STATEMENT------
    
    @_('IF "(" condition ")" statement')
    def statement(self, p):
        return ('if_stmt', p.condition, p.statement)
    
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
    
    @_('GOTO NUMBER')
    def statement(self, p):
        return('GOTO', p.NUMBER)
    
    @_('PRINT expr')
    def statement(self, p):
        return('print', p.expr)
    
    @_('PRINT NAME NAME')
    def statement(self, p):
        return('print', ('var', p.NAME0), ('print', ('var', p.NAME1)))
    
    @_('expr')
    def statement(self, p):
        return (p.expr)
    
    @_('IF "(" condition')
    def statement(self, p):
        self.print_error(p.lineno, p.index, "Missing ')'")
        
    @_('IF "(" condition ")"')
    def statement(self, p):
        self.print_error(p.lineno, p.index, "Missing conditional statement after IF")
        
    @_('IF error')
    def statement(self, p):
        print('Missing "("')
    
    #-----CONDITIONS------

    @_('expr "<" expr')
    def condition(self, p):
        return ('less_than', p.expr0, p.expr1)
    
    @_('expr ">" expr')
    def condition(self, p):
        return ('greater_than', p.expr0, p.expr1)
    
    @_('expr LOGICALNOTEQUALS expr')
    def condition(self, p):
        return ('logical_not', p.expr0, p.expr1)
    
    @_('expr LOGICALEQUALS expr')
    def condition(self, p):
        return ('logical_eq', p.expr0, p.expr1)
    
    #-----VAR ASSIGN------
    
    @_('INPUT NAME ";"')
    def var_assign(self, p):
        return ('inp', p.NAME, None)

    @_('LET NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
    
    @_('LET NAME "=" error')
    def var_assign(self, p):
        print('NAME "=" error')
        
    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
    
    @_('NAME "=" error')
    def var_assign(self, p):
        print('NAME "=" error')
    
    #-----EXPRESSION------
    
    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)
    
    @_('INT "(" expr ")" ')
    def expr(self, p):
        return('to_int', p.expr)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return ('paren', p.expr)
    
    @_('"(" expr error')
    def expr(self, p):
        print('Missing ")"')

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)
    
    @_('STRING')
    def expr(self, p):
        return ('string', p.STRING)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    
    # Function to handle general errors and check for end-of-file errors
    def error(self, p):
        if p:
            print('Syntax error at line ', p.lineno, 'index', p.index)
        else:
            print('Error: Unexpected end of file ')

# File names of the programs to be interpreted
f_name_1 = r'Sample Program-1.txt'
f_name_2 = r'Sample Program-2.txt'

# Function to import program files raw text
def import_file(f_name):
    with open(f_name, 'r') as file:
        fileData = file.read()
    
    return fileData

# Some test programs for debugging
test_program = '10 LET A = 5 \n 20 LET B = A - INT(A/2) * 2 \n 30 END' 
test_program2 = '60 INPUT A; \n 80 PRINT A'
test_program3 = '60 LET A = 3 + 5 * (4 - 1) \n 70 PRINT(A) \n 80 IF(A < 30) PRINT("A is less than 30") \n 90 A = 2 \n 100 PRINT(A)'

# Import both test files
fileData1 = import_file(f_name_1)
fileData2 = import_file(f_name_2)

# Variable to easily change which file to parse
# Useful for debugging
file_used = fileData2

# Create a lexer instance
# Lex the desired program file
lexer = LexerBasic()
lex = lexer.tokenize(file_used)

# Tokenizes the same program file to print for debugging
# Values get popped off when called, so we need another lexed copy
lex2 = lexer.tokenize(file_used)
for tok in lex2:
     print(tok)

# Parser instance
# Tree variable stored the tuple 'tree'
# Print statement to view the tuple for debugging
parser = ParserBasic()
tree = parser.parse(lex)
for tok in tree:
    print(tok)

# List of important node ids
arith_list = ['add', 'sub', 'mul', 'div']
conditional_list = ['less_than', 'greater_than', 'logical_not']
pass_list = ['line', 'stmnts', 'stmt', 'HOME', 'END']
literals_list = ['num', 'string']

# Table of enviroment variables
# Even indicies are variable names, index above is the corresponding value
env = []

# Recursive definition to iterrate over the AST
# Tree structure is a python tuple (node_id, left_branch, right_branch)
def interpreter(tup):
    node_id = tup[0]
    
    # End of file reached
    if node_id == 'end':
        return
    
    # If node_id is a line or statement, return nothing and run branches if they exist
    if node_id in pass_list:
        if len(tup) == 2: # If the tuple length is 2, there is only a left branch
            interpreter(tup[1])
        else:
            interpreter(tup[1])
            interpreter(tup[2])
            
    # Return literals
    if node_id in literals_list:
        return tup[1]
    
    # Run and return the parenthetical operation
    if node_id == 'paren':
        return interpreter(tup[1])
    
    # Looks up and returns the varible value from the enviroment table
    if node_id == 'var':
        try:
            get_var_index = env.index(tup[1])
            return env[get_var_index + 1]
        except:
            print("Error: variable ", node_id, " not defined.")
    
    # Creating, assigning and changing variables
    # Checks if the variable exists in the enviroment table
    # If true, find the variable index and change the value at index + 1
    # If false, append the variable name then append the value to the enviroment table
    if node_id =='var_assign':
        if tup[1] in env:
            index = env.index(tup[1])
            env[index + 1] = interpreter(tup[2])
        else:
            env.append(tup[1])
            env.append(interpreter(tup[2]))
    
    # Creating, assigning and changing variables through user input
    if node_id == 'inp':
        user_inp = input(">> ")
        if tup[1] in env:
            index = env.index(tup[1])
            env[index + 1] = user_inp
        else:
            env.append(tup[1])
            env.append(user_inp)
        
    # If conditional: the conditional block will always be a right branch
    # If the condition fails, do not run the right branch and return
    if node_id == 'if_stmt':
        bool_run_id_stmt = interpreter(tup[1])
        if bool_run_id_stmt:
            return interpreter(tup[2])
    
    # Type cast to integer
    if node_id == 'to_int':
        return int(interpreter(tup[1]))
    
    # Console print
    if node_id =='print':
        print(interpreter(tup[1]))
        if len(tup) == 3:
            interpreter(tup[2])
        
    # Ruturns the output of arithmetic trees
    if node_id in arith_list:
        if node_id == 'add':
            return interpreter(tup[1]) + interpreter(tup[2])
        elif node_id == 'sub':
            return interpreter(tup[1]) - interpreter(tup[2])
        elif node_id == 'mul':
            return interpreter(tup[1]) * interpreter(tup[2])
        elif node_id == 'div':
            return interpreter(tup[1]) / interpreter(tup[2])
    
    # Returns boolean values for "if" conditionals
    if node_id in conditional_list:
        if node_id == 'less_than':
            return bool(interpreter(tup[1]) < interpreter(tup[2]))
        elif node_id == 'greater_than':
            return bool(interpreter(tup[1]) > interpreter(tup[2]))
        elif node_id == 'logical_not':
            return bool(interpreter(tup[1]) != interpreter(tup[2]))
        elif node_id == 'logical_eq':
            return bool(interpreter(tup[1]) == interpreter(tup[2]))

print("Test program:\n", file_used)
print("Runtime output: ")
interpreter(tree)

# Enviroment table
print(env)



