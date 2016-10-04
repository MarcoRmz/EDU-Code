# -----------------------------------------------------------------------------
# EDU-Code.py
#
# Scanner
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

import ply.lex as lex

# List of reserved words
reserved = {
   'start' : 'START',
   'main' : 'MAIN',
   'function' : 'FUNCTION',
   'int' : 'INT',
   'float' : 'FLOAT',
   'string' : 'STRING',
   'for' : 'FOR',
   'while' : 'WHILE',
   'else if' : 'ELSEIF',
   'if' : 'IF',
   'else' : 'ELSE',
   'switch' : 'SWITCH',
   'bool' : 'BOOL',
   'return' : 'RETURN',
   'void' : 'VOID',
   'true' : 'TRUE',
   'false' : 'FALSE',
   'case' : 'CASE',
   'end' : 'END',
   'and' : 'AND',
   'or' : 'OR',
   'input' : 'INPUT',
   'print' : 'PRINT',
   'vector' : 'VECTOR',
   'by' : 'BY',
   'to' : 'TO',
   'pass' : 'PASS',
   'default' : 'DEFAULT'
}

# List of tokens
tokens = [
	'CTE_INT',
	'CTE_FLOAT',
	'CTE_STRING',
	'ID',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'LPAREN',
	'RPAREN',
	'LCURL',
	'RCURL',
	'COLON',
	'COMMA',
	'EQUALS',
	'DOUBLE_EQUAL',
	'DIFF',
	'LESS',
	'GREATER',
	'AMPERSON',
	'LBRACKET',
	'RBRACKET',
	] + list(reserved.values())

# Regular Expresions for Tokens
t_PLUS 		= r'\+'
t_MINUS 	= r'-'
t_TIMES		= r'\*'
t_DIVIDE	= r'/'
t_LPAREN 	= r'\('
t_RPAREN	= r'\)'
t_LCURL		= r'{'
t_RCURL		= r'}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COLON 	= r':'
t_COMMA		= r','
t_DOUBLE_EQUAL = r'=='
t_EQUALS	= r'='
t_DIFF		= r'!='
t_LESS 		= r'<'
t_GREATER	= r'>'
t_AMPERSON	= r'&'
t_ignore    = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_CTE_FLOAT(t):
    r"\d+\.\d*"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %f", t.value)
        t.value = 0
    return t

def t_CTE_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CTE_STRING(t):
	r'\".*\"'
	# try:
	# 	t.value = string(t.value)
	# except ValueError:
	# 	print("String value invalid %d", t.value)
 #        t.value = ""
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	if t:
		print("Error at line " + str(t.lexer.lineno) + " Illegal character " + str(t.value[0]))
	else:
		print("Unexpected end of input")
	t.lexer.skip(1)

def t_eof(t):
    return None

lexer = lex.lex()