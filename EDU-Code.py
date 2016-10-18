# -----------------------------------------------------------------------------
# EDU-Code.py
#
# Parser
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

from scanner import *
import cuadruplos as cuadruplos
import ply.yacc as yacc

#Function pointer variable
function_ptr = "GLOBAL"

# Global Variables
globalVars = {}

# Functions Directory
functionsDir = {}

# Constants
ERROR = -1
INT = 0
FLOAT = 1
STRING = 2
BOOL = 3

PLUS = 0
MINUS = 1
MULT = 2
DIVIDE = 8
AND = 3
OR = 3
LESS = 4
GREATER = 4
# LESSEQUAL = 5
# GREATEREQUAL = 5
DOUBLE_EQUAL = 6
DIFF = 6
EQUALS = 7

# Function to parse token type values to equivalent numeric constant
def parseTypeIndex(type):
	if type == 'int':
		return INT
	elif type == 'float':
		return FLOAT
	elif type == 'bool':
		return BOOL
	else:
		return STRING

def parseType(type):
	if type == INT:
		return 'INT'
	elif type == FLOAT:
		return 'FLOAT'
	elif type == BOOL:
		return 'BOOL'
	else:
		return 'STRING'

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
	'''var_declaracion1 : ID declareVar'''

def p_var_declaracion2(p):
	'''var_declaracion2 : ID declareVar2'''

def p_var_declaracion3(p):
	'''var_declaracion3 : epsilon
				| inicializacion'''

def p_var_declaracion4(p):
	'''var_declaracion4 : epsilon
				| inicializacion_vector'''

def p_declareVar(p):
	'''declareVar :'''
	if function_ptr == 'GLOBAL':
  		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		vartype = parseTypeIndex(p[-2])
  		globalVars[p[-1]] = [vartype, 'ValueNone']
	else:
		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		elif functionsDir[function_ptr][1].has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		vartype = parseTypeIndex(p[-2])
	  	functionsDir[function_ptr][1][p[-1]] = [vartype, 'ValueNone']
	p[0] = p[-1]

def p_declareVar2(p):
	'''declareVar2 :'''
	if function_ptr == 'GLOBAL':
  		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		vartype = parseTypeIndex(p[-2])
  		globalVars[p[-1]] = [vartype, 'ValueNone']
	else:
		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		elif functionsDir[function_ptr][1].has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], lexer.lineno))
  			exit(1)
  		vartype = parseTypeIndex(p[-2])
	  	functionsDir[function_ptr][1][p[-1]] = ['VECTOR ' + str(vartype), 'ValueNone']
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
			print("Variable %s is not declared! Line: %s" %(p[-1], lexer.lineno))
			exit(1)
	else:
		if functionsDir[function_ptr][1].has_key(p[-1]):
			functionsDir[function_ptr][1][p[-1]][1] = p[2]
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[-1], lexer.lineno))
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
	'exp 	: termino checkEXPPOper exp1'
	print "acabo exp"
	print("-----------------")
	print("tipos:")
	print(cuadruplos.pTipos)
	print("---")
	print("operandos:")
	print(cuadruplos.pOperandos)
	print("---")
	print("operadores:")
	print(cuadruplos.pOper)
	print("-----------------")
	print("")

def p_checkEXPPOper(p):
	'checkEXPPOper : '
	print "\ncheckEXPPOper"
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == PLUS) or (cuadruplos.pOper[-1] == MINUS)):
			print "CHECK POPER L201 %s " % str(cuadruplos.pOperandos)
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()
			print "CHECK POPER L207 %s " % str(cuadruplos.pOperandos)

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L212  " % (str(operator), str(operand1), str(operand2))
				if(operator == PLUS):
					#result = operand1+operand2
					cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				else:
					#result = operand1-operand2
					cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("index cuadruplos %d \n cuadruplos: %s\n" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_exp1(p):
	''' exp1 	: PLUS addOperator exp
				| MINUS addOperator exp
				| epsilon'''


def p_termino(p):
	'termino 	: factor checkTERMPOper termino1'

def p_checkTERMPOper(p):
	'checkTERMPOper : '

	print "\n checkTERMPOper"
	print "operadores: %s" % str(cuadruplos.pOper)
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == MULT) or (cuadruplos.pOper[-1] == DIVIDE)):
			print("operandos: %s" %(str(cuadruplos.pOper)))
			print("operadores: %s" %(str(cuadruplos.pOperandos)))
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			print("operadores con pop: %s" %(str(cuadruplos.pOperandos)))
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)
			if(operationType != ERROR):
				if(operator == PLUS):
					#result = operand1*operand2
					cuadruplos.dirCuadruplos.append( (operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				else:
					#result = operand1/operand2
					cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("index cuadruplos %d \n cuadruplos: %s" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_termino1(p):
	'''termino1 : TIMES addOperator termino
				| DIVIDE addOperator termino
				| epsilon'''

def p_addOperator(p):
	'''addOperator : '''
	if p[-1] == '*':
		cuadruplos.pOper.append(MULT)
	elif p[-1] == '/':
		cuadruplos.pOper.append(DIVIDE)
	elif p[-1] == '+':
		cuadruplos.pOper.append(PLUS)
	else:
		cuadruplos.pOper.append(MINUS)

def p_inicializacion_vector(p):
	'inicializacion_vector : EQUALS LBRACKET inicializacion_vector1 RBRACKET'
  	# Save ID key with typeTmp and value as tuple
	if function_ptr == 'GLOBAL':
		if globalVars.has_key(p[-1]):
			globalVars[p[-1]][1] = p[2] + str(p[3]) + p[4]
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[-1], lexer.lineno))
			exit(1)
	else:
		if functionsDir[function_ptr][1].has_key(p[-1]):
			functionsDir[function_ptr][1][p[-1]][1] = p[2] + str(p[3]) + p[4]
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[-1], lexer.lineno))
			exit(1)
	p[0] = p[1]

def p_inicializacion_vector1(p):
	'''inicializacion_vector1 : varcte inicializacion_vector2
				| epsilon'''
	if len(p) > 2:
		p[0] = str(p[1]) + p[2]
	else:
		p[0] = p[1]

def p_inicializacion_vector2(p):
	'''inicializacion_vector2 : COMMA varcte inicializacion_vector2
				| epsilon'''
	if len(p) > 2:
		if p[3]:
			p[0] = p[1] + str(p[2]) + str(p[3])
		else:
			p[0] = p[1] + str(p[2])
	else:
		p[0] = p[1]

def p_main(p):
	'main : MAIN declareMain LCURL main1 estatuto main2 RCURL'

def p_declareMain(p):
	'''declareMain : '''
	global function_ptr
	function_ptr = p[-1]
	if functionsDir.has_key(p[-1]) == False:
		functionsDir[p[-1]] = ['main', {}]
	else:
		# Error
		print("Main %s already declared! Line: %s" %(p[-1], lexer.lineno))
		exit(1)

def p_main1(p):
	'''main1 : var_declaracion main1
				| epsilon'''

def p_main2(p):
	'''main2 : estatuto main2
				| epsilon'''

def p_while(p):
	'while : WHILE LPAREN expresion RPAREN bloque'

def p_factor(p):
	''' factor	: LPAREN factorAddFakeCover exp RPAREN
				| factor1'''
	if len(p) == 5:
		print("REMOVE COVER: " + str(cuadruplos.pOper[-1]))
		cuadruplos.pOper.pop()

def p_factorAddFakeCover(p):
	'factorAddFakeCover : '
	cuadruplos.pOper.append(p[-1])

def p_factor1(p):
	''' factor1 : PLUS varcte
				| MINUS varcte
				| varcte'''

	print "\n factor1"
	# Insert varcte to pOperandos
	if len(p) == 3:
		p[0] = p[1] + str(p[2])
		# Verify PLUS & MINUS are used only on INT & FLOATS
		if ((isinstance(p[2], int)) or (isinstance(p[2], float))):
			if (p[1] == '-'):
				cuadruplos.pOperandos.append(p[2]*-1)
			else:
				cuadruplos.pOperandos.append(p[2])

			# Insert Type of varcte to pTipos
			if isinstance(p[2], int):
				cuadruplos.pTipos.append(INT)
			elif isinstance(p[2], float):
				cuadruplos.pTipos.append(FLOAT)
		else:
			print("Operator mismatch you have a %s before a type: %s at line: %s" %(p[1], type(p[2]), lexer.lineno))
			exit(1)
	else:
		p[0] = p[1]
		print("VARCTE operando: %s" %(str(p[1])))
		cuadruplos.pOperandos.append(p[1])
		print("operadores VARCTE encontrada: %s" %(str(cuadruplos.pOperandos)))
		# Insert Type of varcte to pTipos
		if isinstance(p[1], int):
			cuadruplos.pTipos.append(INT)
		elif isinstance(p[1], float):
			cuadruplos.pTipos.append(FLOAT)
		elif isinstance(p[1], bool):
			cuadruplos.pTipos.append(BOOL)
		else:
			if globalVars.has_key(p[1]):
		  			cuadruplos.pTipos.append(globalVars[p[1]][0])
			elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[1]):
			  		cuadruplos.pTipos.append(functionsDir[function_ptr][1][p[1]][0])
			else:
				cuadruplos.pTipos.append(STRING)

def p_estatuto(p):
	'''estatuto : asignacion
				| llamada
				| condicion
				| switch
				| while
				| for'''

def p_asignacion(p):
	'''asignacion : ID EQUALS asignacion1'''
	print "\nacabo asignacion"
	if globalVars.has_key(p[1]):
		asignacionType = cuadruplos.cubo.getResultType(globalVars[p[1]][0], cuadruplos.pTipos[-1], EQUALS)
		if asignacionType != ERROR:
			globalVars[p[1]][0] = asignacionType
			globalVars[p[1]][1] = cuadruplos.pOperandos.pop()
			cuadruplos.dirCuadruplos.append((EQUALS, globalVars[p[1]][1], None, p[1]))
			cuadruplos.pTipos.pop()
			cuadruplos.indexCuadruplos += 1
		else:
			# Error
			print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], parseType(globalVars[p[1]][0]), parseType(cuadruplos.pTipos[-1]),lexer.lineno))
			exit(1)
	else:
		if functionsDir[function_ptr][1].has_key(p[1]):
			print("asdjlfhasdljfh %s" %(str(cuadruplos.pOperandos)))
			asignacionType = cuadruplos.cubo.getResultType(functionsDir[function_ptr][1][p[1]][0], cuadruplos.pTipos[-1], EQUALS)
			if asignacionType != ERROR:
				print "SI ENTRO"
				functionsDir[function_ptr][1][p[1]][0] = asignacionType
				functionsDir[function_ptr][1][p[1]][1] = cuadruplos.pOperandos.pop()
				cuadruplos.dirCuadruplos.append((EQUALS, functionsDir[function_ptr][1][p[1]][1], None, p[1]))
				cuadruplos.pTipos.pop()
				cuadruplos.indexCuadruplos += 1
				print "PILA DE OPERANDOS L430 %s" % str(cuadruplos.pOperandos)
			else:
				# Error
				print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], parseType(functionsDir[function_ptr][1][p[1]][0]), parseType(cuadruplos.pTipos[-1]),lexer.lineno))
				exit(1)
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[1], lexer.lineno))
			exit(1)

def p_asignacion1(p):
	'''asignacion1 : exp
				| llamada
				| asignacion_vector'''
	p[0] = p[1]

def p_asignacion_vector(p):
	'''asignacion_vector : LBRACKET inicializacion_vector1 RBRACKET'''
	p[0] = p[1] + p[2] + p[3]

def p_expresion(p):
	'expresion 	: expresion1'
	p[0] = p[1]

def p_expresion1(p):
	'''expresion1 	: epsilon
					| expresion2 exp'''
	if len(p) == 3:
		p[0] = p[1]

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
		if functionsDir.has_key(p[1]):
			global function_ptr
			function_ptr = p[1]
		else:
			# Error
			print("Function %s is not declared!" %(p[1]))
			exit(1)
	p[0] = p[1]

def p_llamada1(p):
	'''llamada1 	: epsilon
					| exp llamada2'''

def p_llamada2(p):
	'''llamada2 	: epsilon
					| COMMA exp llamada2'''

def p_varcte(p):
	''' varcte 	: ID varcte1
				| CTE_INT tipoINT
				| CTE_FLOAT tipoFLOAT
                | CTE_STRING tipoSTRING
                | cte_bool'''
        p[0] = p[1]

def p_tipoINT(p):
	'tipoINT : '
	#cuadruplos.pTipos.append(INT)

def p_tipoFLOAT(p):
	'tipoFLOAT : '
	#cuadruplos.pTipos.append(FLOAT)

def p_tipoSTRING(p):
	'tipoSTRING : '
	#cuadruplos.pTipos.append(STRING)

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
	#cuadruplos.pTipos.append(BOOL)

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
	'''funcion4	: VOID funcion5
				| tipo funcion5'''

def p_funcion5(p):
	'''funcion5	: ID declareFunc LPAREN funcion3 RPAREN LCURL funcion1 estatuto funcion2 funcion6'''

def p_declareFunc(p):
	'''declareFunc : '''
	global function_ptr
	function_ptr = p[-1]
	if functionsDir.has_key(p[-1]) == False:
		functionsDir[p[-1]] = [p[-2], {}]
	else:
		# Error
		print("Function %s already declared!" %(p[-1]))
		exit(1)

def p_funcion6(p):
	'''funcion6	: RCURL
				| RETURN ID RCURL'''

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
	print("cuadruplos: ")
	print(cuadruplos.dirCuadruplos)
	print("operadores: ")
	print(cuadruplos.pOper)
	print("operandos: ")
	print(cuadruplos.pOperandos)
	print("*****************************************")
	print("Num cuadruplos: " + str(cuadruplos.indexCuadruplos))
	print("*****************************************")
	print("\nSuccessful")
