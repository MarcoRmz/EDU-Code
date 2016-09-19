# -----------------------------------------------------------------------------
# EDU-Code.py
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

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
   'list' : 'LIST',
   'by' : 'BY',
   'to' : 'TO',
   'pass' : 'PASS',
}

# List of tokens
tokens = (
	'INTVAL',
	'FLOATVAL',
	'STRINGVAL',
	'LISTVAL'
	'ID',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'LPAREN',
	'RPAREN',
	'LCURL',
	'RCURL',
	'SEMICOLON',
	'COLON',
	'COMMA',
	'EQUALS',
	'DIFF',
	'LESS',
	'GREATER',
	) + list(reserved.values())

# Regular Expresions for Tokens
t_ID        = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS 		= r'\+'
t_MINUS 	= r'-'
t_TIMES		= r'\*'
t_DIVIDE	= r'/'
t_LPAREN 	= r'\('
t_RPAREN	= r'\)'
t_SEMICOLON	= r';'
t_LCURL		= r'{'
t_RCURL		= r'}'
t_COLON 	= r':'
t_COMMA		= r','
t_EQUALS	= r'='
t_DIFF		= r'<>'
t_LESS 		= r'<'
t_GREATER	= r'>'
t_ignore    = ' \t'

def t_FLOATVAL(t):
    r"\d+\.\d*"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %f", t.value)
        t.value = 0
    return t

def t_INTVAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRINGVAL(t):	
	r'\"[a-zA-Z]([a-zA-Z0-9])*\"'
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	if t:
		print "Syntax error at line " + str(t.lexer.lineno) + " Illegal character " + str(t.value[0])
	else:
		print("Unexpected end of input")
	t.lexer.skip(1)

def t_eof(t):
    return None

# Lexer
import ply.lex as lex
lexer = lex.lex()

# Grammar
def p_start(p):
	'start 	: START ID SEMICOLON start1 bloque'
	pass

def p_start1(p):
	'''start1	: vars
				| epsilon'''
	pass

def p_vars(p):
	'vars 		: VAR ID vars1 COLON tipo SEMICOLON vars2'
	pass

def p_vars1(p):
	'''vars1	: COMMA ID vars1
				| epsilon'''
	pass

def p_vars2(p):
	'''vars2	: ID vars1 COLON tipo SEMICOLON vars2
				| epsilon'''
	pass

def p_tipo(p):
	'''tipo 	: INT
				| FLOAT
				| STRING'''
	pass

def p_bloque(p):
	'''bloque 	: LCURL bloque1 RCURL'''
	pass

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''
	pass

def p_estatuto(p):
	'''estatuto : asignacion
				| condicion
				| escritura'''
	pass

def p_asignacion(p):
	'asignacion : ID EQUALS expresion SEMICOLON'
	pass

def p_expresion(p):
	'expresion 	: exp expresion1'
	pass

def p_expresion1(p):
	'''expresion1 	: epsilon
					| expresion2 exp'''
	pass

def p_expresion2(p):
	'''expresion2 	: LESS
					| GREATER
					| DIFF'''
	pass

def p_escritura(p):
	'escritura 		: PRINT LPAREN escritura1 RPAREN SEMICOLON'
	pass

def p_escritura1(p):
	'''escritura1 	: expresion escritura2
					| STRING escritura2'''
	pass

def p_escritura2(p):
	'''escritura2 	: COMMA escritura1
					| epsilon'''
	pass

def p_exp(p):
	'exp 	: termino exp1'
	pass

def p_exp1(p):
	''' exp1 	: PLUS termino exp1
				| MINUS termino exp1
				| epsilon'''
	pass

def p_condicion(p):
	'''condicion 	: IF LPAREN expresion RPAREN bloque condicion1 SEMICOLON'''
	pass

def p_condicion1(p):
	'''condicion1	: ELSE bloque
					| epsilon'''
	pass

def p_termino(p):
	'''termino 	: factor termino1'''
	pass

def p_termino1(p):
	'''termino1 : TIMES factor termino1
				| DIVIDE factor termino1
				| epsilon'''
	pass

def p_factor(p):
	''' factor	: LPAREN expresion RPAREN
				| factor1 varcte'''
	pass 

def p_factor1(p):
	''' factor1 : PLUS
				| MINUS
				| epsilon'''
	pass

def p_varcte(p):
	''' varcte 	: FLOAT
				| INT
				| ID'''
	pass

def p_epsilon(p):
	'epsilon :'
	pass

def p_error(p):
	if p:
		print("Syntax error at token", p.type)
		# Discard the token
		parser.errok()
	else:
		print("Syntax error at EOF")
	sys.exit(0)

# Parser
import ply.yacc as yacc
parser = yacc.yacc()

import sys


if __name__ == '__main__':

	if (len(sys.argv) > 1):
		fin = sys.argv[1]
	else:
		fin = 'prueba1.txt'

	f = open(fin, 'r')
	data = f.read()

	lexer.input(data)

	# Tokenize
	for tok in lexer:
		print(tok)

	data = f.read()
	parser.parse(data, tracking=True)

	print("Successful")
