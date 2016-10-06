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

#Function pointer variable
function_ptr = "GLOBAL"

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
	'''var_declaracion1 : ID declareVar var_declaracion3'''

def p_var_declaracion2(p):
	'''var_declaracion2 : ID declareVar
				| inicializacion_vector'''

def p_var_declaracion3(p):
	'''var_declaracion3 : epsilon
				| inicializacion'''

def p_declareVar(p):
	'''declareVar :'''
	if function_ptr == 'GLOBAL':
  		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared!" %(p[-1]))
  			exit(1)
  		globalVars[p[-1]] = [p[-2], 'ValueNone']
	else:
		if functionsDir.has_key(function_ptr) == False:
			functionsDir[function_ptr] = ['FunctTypeNone', {}]
		else:
			if globalVars.has_key(p[-1]):
	  			# Error
	  			print("Variable %s already declared!" %(p[-1]))
	  			exit(1)
	  		elif functionsDir[function_ptr][1].has_key(p[-1]):
	  			# Error
	  			print("Variable %s already declared!" %(p[-1]))
	  			exit(1)
	  	functionsDir[function_ptr][1][p[-1]] = [p[-2], 'ValueNone']
	p[0] = p[-1]

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
	'inicializacion : EQUALS exp'
  	# Save ID key with typeTmp and value as tuple
	if function_ptr == 'GLOBAL':
		if globalVars.has_key(p[-1]):
			globalVars[p[-1]][1] = p[2]
		else:
			# Error
			print("Variable %s is not declared!" %(p[-1]))
			exit(1)
	else:
		if functionsDir[function_ptr][1].has_key(p[-1]):
			functionsDir[function_ptr][1][p[-1]][1] = p[2]
		else:
			# Error
			print("Variable %s is not declared!" %(p[-1]))
			exit(1)

def p_tipo(p):
	'''tipo 	: INT
				| FLOAT
				| BOOL
				| STRING'''
	p[0] = p[1]

def p_bloque(p):
	'bloque 	: LCURL estatuto bloque1 RCURL'

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''

def p_exp(p):
	'exp 	: termino exp1'
	p[0] = p[2]
	
def p_exp1(p):
	''' exp1 	: PLUS exp
				| MINUS exp
				| epsilon'''
	if len(p) == 3:
		p[0] = str(p[-1]) + str(p[1]) + str(p[2])
	else:
		p[0] = str(p[-1])

def p_termino(p):
	'termino 	: factor termino1'
	p[0] = p[2]

def p_termino1(p):
	'''termino1 : TIMES termino
				| DIVIDE termino
				| epsilon'''
	if len(p) == 3:
		p[0] = str(p[-1]) + str(p[1]) + str(p[2])
	else:
		p[0] = str(p[-1])

def p_inicializacion_vector(p):
	'inicializacion_vector : ID declareVar EQUALS LBRACKET inicializacion_vector1 RBRACKET'
  # Save ID key with typeTmp and value as tuple
	p[0] = p[1]

def p_inicializacion_vector1(p):
	'''inicializacion_vector1 : varcte inicializacion_vector2
				| epsilon'''

def p_inicializacion_vector2(p):
	'''inicializacion_vector2 : COMMA varcte inicializacion_vector2
				| epsilon'''

def p_main(p):
	'main : MAIN LCURL main1 estatuto main2 RCURL'
	function_ptr = p[1]

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
				| factor1'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]

def p_factor1(p):
	''' factor1 : PLUS varcte
				| MINUS varcte
				| varcte'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]

def p_estatuto(p):
	'''estatuto : asignacion
				| llamada
				| condicion
				| switch
				| while
				| for'''

def p_asignacion(p):
	'''asignacion : ID EQUALS asignacion1'''
	if p[1] != 'print':
		if globalVars.has_key(p[1]):
			globalVars[p[1]][1] = p[3]
		else:
			if functionsDir[function_ptr][1].has_key(p[1]):
				functionsDir[function_ptr][1][p[1]][1] = p[3]
			else:
				# Error
				print("Variable %s is not declared!" %(p[1]))
				exit(1)

def p_asignacion1(p):
	'''asignacion1 : exp
				| llamada'''
	p[0] = p[1]

def p_expresion(p):
	'expresion 	: expresion1'
	p[0] = p[1]

def p_expresion1(p):
	'''expresion1 	: epsilon
					| expresion2 exp'''
	if len(p) == 3:
		p[0] = p[1] + p[2]

def p_expresion2(p):
	'''expresion2 	: LESS
					| GREATER
					| DOUBLE_EQUAL
					| DIFF'''
	p[0] = p[1]

def p_expresion_logica(p):
	'expresion_logica 	: exp expresion_logica1 expresion'

def p_expresion_logica1(p):
	'''expresion_logica1 	: AND exp
					| epsilon
					| OR exp'''

def p_llamada(p):
	'''llamada 	: ID LPAREN llamada1 RPAREN
				| print
				| input'''
	if len(p) > 2:
		function_ptr = p[1]
	p[0] = p[1]

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
        p[0] = p[1]

def p_varcte1(p):
	''' varcte1 	: epsilon
				| LPAREN exp varcte2 RPAREN
				| LBRACKET exp RBRACKET'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1] + p[2] + p[3] + p[4]

def p_varcte2(p):
	'''varcte2 	: epsilon
					| COMMA exp varcte2'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2] + p[3]

def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''
	p[0] = p[1]

def p_print(p):
	'print 		    : PRINT LPAREN print1 RPAREN'
	p[0] = p[1]

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
	'''input	: INPUT LPAREN input1 RPAREN'''
	p[0] = p[1]

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
	# Save function ID and type

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
	pass

def p_error(p):
	if p:
		print("Syntax error at token: '%s' with value: '%s' at line: %d in pos: %d" %(p.type, p.value, p.lineno, p.lexpos))
		# Discard the token
		parser.errok()
	else:
		print("Syntax error at EOF")
	exit(1)

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

	print("*****************************************")
	print("globalVars: ")
	print(globalVars)
	print("*****************************************")
	print("functionDir: ")
	print(functionsDir)
	print("*****************************************")
	print("Successful")
