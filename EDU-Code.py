# -----------------------------------------------------------------------------
# EDU-Code.py
#
# Parser
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

from scanner import *
import ply.yacc as yacc

# Global Variables
globalVars = {}

# Functions Directory
functionsDir = {}

# Parser
def p_programa(p):
	'programa 	: START programa1 programa2 main END'

def p_programa1(p):
	'''programa1 : var_declaracion programa1
				| epsilon'''

def p_programa2(p):
	'''programa2 : funcion programa2
				| epsilon'''

def p_var_declaracion(p):
	'''var_declaracion : tipo var_declaracion1
				| VECTOR tipo var_declaracion2'''

def p_var_declaracion1(p):
	'''var_declaracion1 : ID
				| inicializacion'''

def p_var_declaracion2(p):
	'''var_declaracion2 : ID
				| inicializacion_vector'''

def p_parametros(p):
	'''parametros : tipo parametros1 ID parametros2
				| VECTOR tipo parametros1 ID parametros2'''

def p_parametros1(p):
	'''parametros1 : AMPERSON
				| epsilon'''

def p_parametros2(p):
	'''parametros2 : COMMA parametros
				| epsilon'''

def p_inicializacion(p):
	'inicializacion : ID EQUALS exp'

def p_tipo(p):
	'''tipo 	: INT
				| FLOAT
				| BOOL
				| STRING'''

def p_bloque(p):
	'bloque 	: LCURL estatuto bloque1 RCURL'

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''

def p_exp(p):
	'exp 	: termino exp1'

def p_exp1(p):
	''' exp1 	: PLUS exp
				| MINUS exp
				| epsilon'''

def p_termino(p):
	'termino 	: factor termino1'

def p_termino1(p):
	'''termino1 : TIMES termino
				| DIVIDE termino
				| epsilon'''

def p_inicializacion_vector(p):
	'inicializacion_vector : ID EQUALS LBRACKET inicializacion_vector1 RBRACKET'

def p_inicializacion_vector1(p):
	'''inicializacion_vector1 : varcte inicializacion_vector2
				| epsilon'''

def p_inicializacion_vector2(p):
	'''inicializacion_vector2 : COMMA varcte inicializacion_vector2
				| epsilon'''

def p_main(p):
	'main : MAIN LCURL main1 estatuto main2 RCURL'

def p_main1(p):
	'''main1 : var_declaracion main1
				| epsilon'''

def p_main2(p):
	'''main2 : estatuto main2
				| epsilon'''

def p_while(p):
	'while : WHILE LPAREN expresion RPAREN bloque'

def p_factor(p):
	''' factor	: LPAREN expresion RPAREN
				| factor1 varcte'''

def p_factor1(p):
	''' factor1 : PLUS varcte
				| MINUS varcte
				| epsilon'''

def p_estatuto(p):
	'''estatuto : inicializacion
				| llamada
				| print
				| input
				| condicion
				| switch
				| while
				| for'''

def p_expresion(p):
	'expresion 	: expresion1'

def p_expresion1(p):
	'''expresion1 	: epsilon
					| expresion2 exp'''

def p_expresion2(p):
	'''expresion2 	: LESS
					| GREATER
					| DOUBLE_EQUAL
					| DIFF'''

def p_expresion_logica(p):
	'expresion_logica 	: exp expresion_logica1 expresion'

def p_expresion_logica1(p):
	'''expresion_logica1 	: AND exp
					| epsilon
					| OR exp'''

def p_llamada(p):
	'llamada 	: ID LPAREN llamada1 RPAREN'

def p_llamada1(p):
	'''llamada1 	: epsilon
					| exp llamada2'''

def p_llamada2(p):
	'''llamada2 	: epsilon
					| COMMA exp llamada2'''

def p_varcte(p):
	''' varcte 	: ID varcte1
				| CTE_INT
				| CTE_FLOAT
                | CTE_STRING
                | cte_bool'''

def p_varcte1(p):
	''' varcte1 	: epsilon
				| LPAREN exp varcte2 RPAREN
				| LBRACKET exp RBRACKET'''

def p_varcte2(p):
	'''varcte2 	: epsilon
					| COMMA exp varcte2'''

def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''

def p_print(p):
	'print 		    : PRINT LPAREN print1 RPAREN'

def p_print1(p):
	'''print1 		: CTE_STRING print2
                    | ID print2'''

def p_print2(p):
	'''print2 		: epsilon
                    | PLUS print1'''

def p_condicion(p):
	'condicion 	: IF LPAREN expresion_logica RPAREN condicion1 condicion2 condicion3'

def p_condicion1(p):
	'''condicion1	: bloque
                    | LCURL bloque RCURL'''

def p_condicion2(p):
	'''condicion2 	: ELSEIF condicion1 condicion2
                    | epsilon'''

def p_condicion3(p):
	'''condicion3	: ELSE condicion1
					| epsilon'''

def p_input(p):
	'''input	: tipo ID EQUALS INPUT LPAREN input1 RPAREN
				| ID EQUALS INPUT LPAREN input1 RPAREN'''

def p_input1(p):
	'''input1	: CTE_STRING
				| epsilon'''

def p_for(p):
	'for : FOR CTE_INT TO CTE_INT BY LPAREN for1 CTE_INT RPAREN bloque'

def p_for1(p):
	'''for1	: PLUS
			| TIMES
			| DIVIDE
			| MINUS'''

def p_funcion(p):
	'funcion	: FUNCTION funcion4'

def p_funcion1(p):
    '''funcion1 : epsilon
                | var_declaracion funcion1'''

def p_funcion2(p):
    '''funcion2 : epsilon
                | estatuto funcion2'''

def p_funcion3(p):
    '''funcion3 : parametros
                | epsilon'''

def p_funcion4(p):
	'''funcion4	: VOID ID LPAREN funcion3 RPAREN LCURL funcion1 estatuto funcion2 RCURL
				| tipo ID LPAREN funcion3 RPAREN LCURL funcion1 estatuto funcion2 RETURN ID RCURL'''

def p_switch(p):
    'switch     : SWITCH ID switch1 LCURL switch2 switch3 RCURL'

def p_switch1(p):
    '''switch1  : epsilon
                | LBRACKET exp RBRACKET'''

def p_switch2(p):
    '''switch2  : epsilon
                | CASE varcte COLON switch4 switch2'''

def p_switch3(p):
    'switch3  : DEFAULT COLON switch4'

def p_switch4(p):
    '''switch4  : LCURL PASS RCURL
    			| estatuto'''
  

def p_epsilon(p):
	'epsilon :'

def p_error(p):
	if p:
		print("Syntax error at token:", p.type, " line: ", p.lineno)
		# Discard the token
		parser.errok()
	else:
		print("Syntax error at EOF")
	sys.exit(0)

parser = yacc.yacc()


# Main
import sys

if __name__ == '__main__':

	if (len(sys.argv) > 1):
		fin = sys.argv[1]
	else:
		print("No file provided!")
		exit(1)

	f = open(fin, 'r')
	data = f.read()

	# Print Tokens
	# lexer.input(data)
	# for tok in lexer:
	# 	print(tok)

	parser.parse(data, tracking=True)

	print("Successful")
