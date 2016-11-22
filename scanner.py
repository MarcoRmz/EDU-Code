#########################################################
#														#
# 	scanner.py											#
#														#
# 	Scanner												#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581		 				#
#														#
#########################################################

import ply.lex as lex

# List of reserved words
reserved = {
	'start' : 'START',
	'main' : 'MAIN',
	'function' : 'FUNCTION',
	'int' : 'INT',
	'float' : 'FLOAT',
	'string' : 'STRING',
	'from' : 'FROM',
	'while' : 'WHILE',
	'elseif' : 'ELSEIF',
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
	'default' : 'DEFAULT',
	'do' :	'DO'
}

# List of tokens
tokens = [
	'CTE_INT',
	'CTE_FLOAT',
	'VARSTRING',
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
	'LESSEQUAL',
	'GREATEREQUAL',
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
t_LBRACKET	= r'\['
t_RBRACKET	= r'\]'
t_COLON 	= r':'
t_COMMA		= r','
t_DOUBLE_EQUAL = r'=='
t_DIFF		= r'!='
t_LESSEQUAL = r'<='
t_GREATEREQUAL	= r'>='
t_LESS 		= r'<'
t_GREATER	= r'>'
t_EQUALS	= r'='
t_AMPERSON	= r'&'
t_ignore	= ' \t'

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')
	return t

def t_CTE_FLOAT(t):
	r"\d+\.\d*"
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too large %f at line: %s" %(t.value), str(t.lexer.lineno))
		t.value = 0
	return t

def t_CTE_INT(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d at line: %s" %(t.value, str(t.lexer.lineno)))
		t.value = 0
	return t

def t_VARSTRING(t):
	r'\"[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':\|,.<>\/? X]*\"'
	# Remove quotes from strings
	t.value = t.value[1:-1]
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	if t:
		print("Illegal character: %s at line: %s" %(str(t.value[0]), str(t.lexer.lineno)))
	else:
		print("Unexpected end of input")
	t.lexer.skip(1)

def t_eof(t):
	return None

lexer = lex.lex()
