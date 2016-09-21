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
   'list' : 'LIST',
   'by' : 'BY',
   'to' : 'TO',
   'pass' : 'PASS',
}

# List of tokens
tokens = [
	'INTVAL',
	'FLOATVAL',
	'STRINGVAL',
	'LISTVAL',
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
		print("Error at line " + str(t.lexer.lineno) + " Illegal character " + str(t.value[0]))
	else:
		print("Unexpected end of input")
	t.lexer.skip(1)

def t_eof(t):
    return None

# Lexer
import ply.lex as lex
lexer = lex.lex()

# Grammar
def p_programa(p):
	'programa 	: START programa1 programa2 main END'
	pass

def p_programa1(p):
	'''programa1 : var_declaracion programa1
				| epsilon'''
	pass

def p_programa2(p):
	'''programa2 : function programa2
				| epsilon'''
	pass

def p_var_declaracion(p):
	'''var_declaracion : tipo var_declaracion1
				| LIST var_declaracion2'''
	pass

def p_var_declaracion1(p):
	'''var_declaracion1 : ID
				| asignacion'''
	pass

def p_var_declaracion2(p):
	'''var_declaracion2 : ID
				| asignacion_list'''
	pass

def p_parametros(p):
	'''parametros : tipo parametros1 ID COMMA parametros2
				| LIST parametros1 ID COMMA parametros2'''
	pass

def p_parametros1(p):
	'''parametros1 : AMPERSON
				| epsilon'''
	pass

def p_parametros2(p):
	'''parametros2 : tipo parametros1 ID COMMA parametros2
				| LIST parametros1 ID COMMA parametros2
				| epsilon'''
	pass

def p_asignacion(p):
	'asignacion : ID EQUALS expresion'
	pass

def p_tipo(p):
	'''tipo 	: INT
				| FLOAT
				| BOOL
				| STRING'''
	pass

def p_bloque(p):
	'''bloque 	: LCURL bloque1 RCURL'''
	pass

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''
	pass

def p_exp(p):
	'exp 	: termino exp1'
	pass

def p_exp1(p):
	''' exp1 	: PLUS exp
				| MINUS exp
				| epsilon'''
	pass

def p_termino(p):
	'termino 	: factor termino1'
	pass

def p_termino1(p):
	'''termino1 : TIMES termino
				| DIVIDE termino
				| epsilon'''
	pass

def p_asignacion_list(p):
	'asignacion_list : LIST LPAREN asignacion_list1 RPAREN'
	pass

def p_asignacion_list1(p):
	'''asignacion_list1 : varcte asignacion_list2
				| epsilon'''
	pass

def p_asignacion_list2(p):
	'''asignacion_list2 : COMMA asignacion_list1
				| epsilon'''
	pass

def p_main(p):
	'main : FUNCTION VOID MAIN LPAREN RPAREN LCURL main1 estatuto main2 RCURL'
	pass

def p_main1(p):
	'''main1 : var_declaracion main1
				| epsilon'''
	pass

def p_main2(p):
	'''main2 : estatuto main2
				| epsilon'''
	pass

def p_while(p):
	'while : WHILE LPAREN expresion RPAREN bloque'
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

def p_estatuto(p):
	'''estatuto : asignacion
				| comentario
				| print
				| input
				| switch
				| while
				| for'''
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
					| AND
					| OR
					| DOUBLE_EQUAL
					| DIFF'''
	pass

def p_varcte(p):
	''' varcte 	: ID
				| CTE_INT
				| CTE_FLOAT
                | CTE_STRING
                | CTE_BOOL
                | CTE_LIST'''
	pass

def p_print(p):
	'print 		    : PRINT LPAREN print1 RPAREN'
	pass

def p_print1(p):
	'''print1 		: CTE_STRING print2
                    | ID print2'''
	pass

def p_print2(p):
	'''print2 		: epsilon
                    | PLUS print1'''
	pass

def p_condicion(p):
	'''condicion 	: IF LPAREN expresion RPAREN bloque condicion1'''
	pass

def p_condicion1(p):
	'''condicion1	: condicion2
                    | ELSEIF bloque condicion1
					| epsilon'''
	pass

def p_condicion2(p):
	'''condicion2	: ELSE bloque
					| epsilon'''
	pass

def p_comentario(p):
    '''comentario : POUND varcte comentario1
                  | DIVIDE TIMES comentario1 TIMES DIVIDE'''

def p_comentario1(p):
    '''comentario1 : varcte comentario1
                   | epsilon'''

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
		print("No file provided!")
		exit(1)

	f = open(fin, 'r')
	data = f.read()

	lexer.input(data)

	# Tokenize
	for tok in lexer:
		print(tok)

	parser.parse(data, tracking=True)

	print("Successful")
