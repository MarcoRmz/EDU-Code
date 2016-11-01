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
prev_Fuction_ptr = 'None'

# Global Variables
globalVars = {}

# Functions Directory
functionsDir = {}

# Pila Temp FROM
pTempFrom = []

# Contador de parametros
countParam = 0

### Constants
ERROR = -1

# TYPES
INT = 0
FLOAT = 1
STRING = 2
BOOL = 3
VOID = 23

# OPERATORS
PLUS = 0
MINUS = 1
MULT = 2
DIVIDE = 3
AND = 4
OR = 5
LESS = 6
GREATER = 7
LESSEQUAL = 8
GREATEREQUAL = 9
DOUBLE_EQUAL = 10
DIFF = 11
EQUALS = 12

# JUMPS
GOTO = 13
GOTOF = 14
GOTOT = 15
GOSUB = 16
RETURN = 17

# SYSTEM FUNCTIONS
PRINT = 18
INPUT = 19
ERA = 20
ENDPROC = 21
PARAM = 22

# Function to parse token type values to equivalent numeric constant
def parseTypeIndex(type):
	if type == 'int':
		return INT
	elif type == 'float':
		return FLOAT
	elif type == 'bool':
		return BOOL
	elif type == 'void':
		return VOID
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
	'programa 	: START gotoMAIN programa1 programa2 main END'
	#agregar cuadruplo de end of file
	cuadruplos.dirCuadruplos.append(("EOF", None, None, None))
	cuadruplos.indexCuadruplos += 1

def p_programa1(p):
	'''programa1 : var_declaracion programa1
				| epsilon'''

def p_programa2(p):
	'''programa2 : funcion programa2
				| epsilon'''

def p_gotoMAIN(p):
	'gotoMAIN : '
	# Generate GOTO MAIN
	cuadruplos.dirCuadruplos.append((GOTO, None, None, None))
	cuadruplos.indexCuadruplos += 1

def p_asignacion(p):
	'''asignacion : ID EQUALS asignacion1'''
	print "\nacabo asignacion L91"
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
			print("L106 pila operandos %s" %(str(cuadruplos.pOperandos)))
			asignacionType = cuadruplos.cubo.getResultType(functionsDir[function_ptr][1][p[1]][0], cuadruplos.pTipos[-1], EQUALS)
			if asignacionType != ERROR:
				print "L109 SI ENTRO"
				functionsDir[function_ptr][1][p[1]][0] = asignacionType
				functionsDir[function_ptr][1][p[1]][1] = cuadruplos.pOperandos.pop()
				cuadruplos.dirCuadruplos.append((EQUALS, functionsDir[function_ptr][1][p[1]][1], None, p[1]))
				cuadruplos.pTipos.pop()
				cuadruplos.indexCuadruplos += 1
				print "PILA DE OPERANDOS L115 %s" % str(cuadruplos.pOperandos)
			else:
				# Error
				print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], parseType(functionsDir[function_ptr][1][p[1]][0]), parseType(cuadruplos.pTipos[-1]),lexer.lineno))
				exit(1)
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[1], lexer.lineno))
			exit(1)

def p_asignacion1(p):
	'''asignacion1 : expresion_logica
				| asignacion_vector'''
	p[0] = p[1]

def p_asignacion_vector(p):
	'''asignacion_vector : LBRACKET inicializacion_vector1 RBRACKET'''
	p[0] = p[1] + p[2] + p[3]

def p_bloque(p):
	'bloque 	: LCURL estatuto bloque1 RCURL'

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''

def p_condicion(p):
	'condicion 	: IF LPAREN expresion_logica RPAREN checkEvaluacionLogica condicion1 checkPSaltos condicion2 condicion3'
	#rellenar goto's de condicion
	while(len(cuadruplos.pSaltos)!=0):
		gotoIndex = cuadruplos.pSaltos.pop()
		t = cuadruplos.dirCuadruplos[gotoIndex]
		t = t[:3] + (cuadruplos.indexCuadruplos,)
		cuadruplos.dirCuadruplos[gotoIndex] = t


def p_condicion1(p):
	'''condicion1	: bloque
                    | LCURL PASS RCURL'''

def p_condicion2(p):
	'''condicion2 	: ELSEIF LPAREN expresion_logica RPAREN checkEvaluacionLogica condicion1 checkPSaltos condicion2
                    | epsilon'''

def p_condicion3(p):
	'''condicion3	: ELSE condicion1
					| epsilon'''

def p_checkEvaluacionLogica(p):
	'''checkEvaluacionLogica : '''
	aux = cuadruplos.pTipos.pop()
	if aux == BOOL:
		# generate GOTO
		cuadruplos.dirCuadruplos.append((GOTOF, cuadruplos.pOperandos.pop(), None, None))
		cuadruplos.pSaltos.append(cuadruplos.indexCuadruplos)
		cuadruplos.indexCuadruplos += 1
	else:
		# Error
		print("Evaluated expresion %s is not a bool! Line: %s" %(aux, lexer.lineno))
		exit(1)

def p_checkPSaltos(p):
	'''checkPSaltos : '''
	#generar goto
	cuadruplos.dirCuadruplos.append((GOTO, None, None, None))
	cuadruplos.indexCuadruplos += 1

	if (len(cuadruplos.pSaltos) != 0):
		gotoIndex = cuadruplos.pSaltos.pop()
		t = cuadruplos.dirCuadruplos[gotoIndex]
		t = t[:3] + (cuadruplos.indexCuadruplos,)
		cuadruplos.dirCuadruplos[gotoIndex] = t

	cuadruplos.pSaltos.append(cuadruplos.indexCuadruplos-1)



def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''
	p[0] = p[1]

def p_do_while(p):
	''' do_while : DO metePSaltos bloque WHILE LPAREN expresion_logica RPAREN '''
	#meter gotov
	aux = cuadruplos.pTipos.pop()
	if aux == BOOL:
		# generate GOTO
		cuadruplos.dirCuadruplos.append((GOTOT, cuadruplos.pOperandos.pop(), None, cuadruplos.pSaltos.pop()))
		cuadruplos.indexCuadruplos += 1
	else:
		# Error
		print("Evaluated expresion %s is not a bool! Line: %s" %(aux, lexer.lineno))
		exit(1)

def p_estatuto(p):
	'''estatuto : asignacion
				| llamada
				| condicion
				| switch
				| while
				| do_while
				| from'''

def p_exp(p):
	'exp 	: termino checkEXPPOper exp1'

def p_checkEXPPOper(p):
	'checkEXPPOper : '
	print "\nL197 checkEXPPOper"
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == PLUS) or (cuadruplos.pOper[-1] == MINUS)):
			print "CHECK POPER L200 %s " % str(cuadruplos.pOperandos)
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()
			print "CHECK POPER L206 %s " % str(cuadruplos.pOperandos)

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L211  " % (str(operator), str(operand1), str(operand2))
				cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("L220 index cuadruplos %d \n cuadruplos: %s\n" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_exp1(p):
	''' exp1 	: PLUS addOperator exp
				| MINUS addOperator exp
				| epsilon'''

def p_addOperator(p):
	'''addOperator : '''
	if p[-1] == '*':
		cuadruplos.pOper.append(MULT)
	elif p[-1] == '/':
		cuadruplos.pOper.append(DIVIDE)
	elif p[-1] == '+':
		cuadruplos.pOper.append(PLUS)
	elif p[-1] == 'and':
		cuadruplos.pOper.append(AND)
	elif p[-1] == 'or':
		cuadruplos.pOper.append(OR)
	elif p[-1] == '<=':
		cuadruplos.pOper.append(LESSEQUAL)
	elif p[-1] == '>=':
		cuadruplos.pOper.append(GREATEREQUAL)
	elif p[-1] == '==':
		cuadruplos.pOper.append(DOUBLE_EQUAL)
	elif p[-1] == '!=':
		cuadruplos.pOper.append(DIFF)
	elif p[-1] == '<':
		cuadruplos.pOper.append(LESS)
	elif p[-1] == '>':
		cuadruplos.pOper.append(GREATER)
	else:
		cuadruplos.pOper.append(MINUS)

def p_expresion(p):
	'expresion 	: exp checkEXPRESIONPOper expresion1'

def p_checkEXPRESIONPOper(p):
	'checkEXPRESIONPOper : '
	print "\nL259 checkEXPRESIONPOper"
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == LESS) or (cuadruplos.pOper[-1] == LESSEQUAL) or (cuadruplos.pOper[-1] == GREATER) or (cuadruplos.pOper[-1] == GREATEREQUAL) or (cuadruplos.pOper[-1] == DOUBLE_EQUAL) or (cuadruplos.pOper[-1] == DIFF)):
			print "CHECK POPER L262 %s " % str(cuadruplos.pOperandos)
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()
			print "CHECK POPER L268 %s " % str(cuadruplos.pOperandos)

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L273  " % (str(operator), str(operand1), str(operand2))
				cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("L282 index cuadruplos %d \n cuadruplos: %s\n" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_expresion1(p):
	'''expresion1 	: LESS addOperator expresion
					| LESSEQUAL addOperator expresion
					| GREATER addOperator expresion
					| GREATEREQUAL addOperator expresion
					| DOUBLE_EQUAL addOperator expresion
					| epsilon
					| DIFF addOperator expresion'''

def p_expresion_logica(p):
	'expresion_logica 	: expresion checkEXPRESIONLOGICAPOper expresion_logica1'
	print "L284 acabo expresionlogica"
	print("-----------------")
	print("tipos:")
	print(cuadruplos.pTipos)
	print("---")
	print("operandos:")
	print(cuadruplos.pOperandos)
	print("---")
	print("operadores:")
	print(cuadruplos.pOper)
	print("-----------------\n")

def p_checkEXPRESIONLOGICAPOper(p):
	'checkEXPRESIONLOGICAPOper : '
	print "\nL298 checkEXPRESIONLOGICAPOper"
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == AND) or (cuadruplos.pOper[-1] == OR)):
			print "CHECK POPER L301 %s " % str(cuadruplos.pOperandos)
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()
			print "CHECK POPER L307 %s " % str(cuadruplos.pOperandos)

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L312  " % (str(operator), str(operand1), str(operand2))
				cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("L321 index cuadruplos %d \n cuadruplos: %s\n" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_expresion_logica1(p):
	'''expresion_logica1 	: AND addOperator expresion_logica
					| epsilon
					| OR addOperator expresion_logica'''

def p_factor(p):
	''' factor	: LPAREN factorAddFakeCover expresion_logica RPAREN
				| factor1'''
	if len(p) == 5:
		print("L332 REMOVE COVER: " + str(cuadruplos.pOper[-1]))
		cuadruplos.pOper.pop()

def p_factorAddFakeCover(p):
	'factorAddFakeCover : '
	cuadruplos.pOper.append(p[-1])

def p_factor1(p):
	''' factor1 : PLUS varcte
				| MINUS varcte
				| varcte'''

	print "\nfactor1 L344"
	# Insert varcte to pOperandos
	#CAMBIO: agregar cte al diccionario correspondiente y regresar en p[0] la direccion de la cte.
	#CAMBIO: mover de varcte el id varcte1 a factor1, checar si es un id no agregar a ctes.
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
		print("L365 VARCTE operando: %s" %(str(p[1])))
		cuadruplos.pOperandos.append(p[1])
		print("L367 operandos VARCTE encontrada: %s" %(str(cuadruplos.pOperandos)))
		# Insert Type of varcte to pTipos
		if isinstance(p[1], int):
			cuadruplos.pTipos.append(INT)
		elif isinstance(p[1], float):
			cuadruplos.pTipos.append(FLOAT)
		elif p[1] == 'true' or p[1] == 'false':
			cuadruplos.pTipos.append(BOOL)
		else:
			print("FUNCTION POINTER FOR ID FOUND: " + function_ptr)
			if globalVars.has_key(p[1]):
		  			cuadruplos.pTipos.append(globalVars[p[1]][0])
			elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[1]):
			  		cuadruplos.pTipos.append(functionsDir[function_ptr][1][p[1]][0])
			else:
				cuadruplos.pTipos.append(STRING)

def p_cteFrom(p):
	''' cteFrom : PLUS CTE_INT
				| MINUS CTE_INT
				| CTE_INT'''
	if len(p) == 3:
		# Verify PLUS & MINUS are used only on INT & FLOATS
		if ((isinstance(p[2], int)) or (isinstance(p[2], float))):
			if (p[1] == '-'):
				p[0] = p[2] * -1
			else:
				p[0] = p[2]
	else:
		p[0] = p[1]

def p_from(p):
	'from : FROM cteFrom creaVarTemp TO cteFrom crearComparacion BY LPAREN from1 cteFrom RPAREN bloque'
	# Actualiza valor en pTempFrom
	if p[9] == '+':
		pTempFrom[p[-1]] = pTempFrom[p[-1]] + p[10]
	elif p[9] == '-':
		pTempFrom[p[-1]] = pTempFrom[p[-1]] - p[10]
	elif p[9] == '*':
		pTempFrom[p[-1]] = pTempFrom[p[-1]] * p[10]
	elif p[9] == '/':
		pTempFrom[p[-1]] = pTempFrom[p[-1]] / p[10]

	# Genera GOTO
	gotoFIndex = cuadruplos.pSaltos.pop()
	cuadruplos.dirCuadruplos.append((GOTO, None, None, cuadruplos.pSaltos.pop()))
	cuadruplos.indexCuadruplos += 1
	t = cuadruplos.dirCuadruplos[gotoFIndex]
	t = t[:3] + (cuadruplos.indexCuadruplos,)
	cuadruplos.dirCuadruplos[gotoFIndex] = t

	# Pop pTempFrom
	pTempFrom.pop()

def p_from1(p):
	'''from1	: PLUS
			| TIMES
			| DIVIDE
			| MINUS'''

def p_creaVarTemp(p):
	'creaVarTemp : '
	pTempFrom.append(p[-1])

def p_crearComparacion(p):
	'crearComparacion : '
	cuadruplos.pSaltos.append(cuadruplos.indexCuadruplos)

	if pTempFrom[-1] >= p[-1]:
		# comparacion >=
		cuadruplos.dirCuadruplos.append((GREATEREQUAL, pTempFrom[-1], p[-1], "t"+str(cuadruplos.countT)))
		cuadruplos.indexCuadruplos += 1
		cuadruplos.countT += 1
	else:
		# comparacion <=
		cuadruplos.dirCuadruplos.append((LESSEQUAL, pTempFrom[-1], p[-1], "t"+str(cuadruplos.countT)))
		cuadruplos.indexCuadruplos += 1
		cuadruplos.countT += 1

	cuadruplos.dirCuadruplos.append((GOTOF, "t"+str(cuadruplos.countT-1), None, None))
	cuadruplos.pSaltos.append(cuadruplos.indexCuadruplos)
	cuadruplos.indexCuadruplos += 1

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
	#CAMBIO: Eliminar count t
	#CAMBIO: Partir el contador de variables temporales y poner uno para cada tipo, agregar cantidad de locales de cada tipo
	#CAMBIO: Contabilizar los parametros por tipo.
	#Todo 2 y 3:
	cuadruplos.countT = 0
	if functionsDir.has_key(p[-1]) == False:
		# [Tipo, DictVar, ListaParam, CantVarTemp, indexCuadruplo]
		functionsDir[p[-1]] = [parseTypeIndex(p[-2]), {}, [], 0, cuadruplos.indexCuadruplos]
	else:
		# Error
		print("Function %s already declared!" %(p[-1]))
		exit(1)

def p_funcion6(p):
	'''funcion6	: RCURL
				| RETURN expresion_logica RCURL'''
	# Verifica tipo de funcion
	if functionsDir[function_ptr][0] != VOID:
		# Generar RETURN
		cuadruplos.dirCuadruplos.append((RETURN, None, None, cuadruplos.pOperandos[-1]))
		cuadruplos.indexCuadruplos += 1
	# Asignar valores de referencias
	# Liberar Tabla de variables locales de memoria
	# Generar ENDPROC
	functionsDir[function_ptr][3] = cuadruplos.countT +1
	cuadruplos.dirCuadruplos.append((ENDPROC, None, None, None))
	cuadruplos.indexCuadruplos += 1
	print functionsDir

def p_inicializacion(p):
	'inicializacion : EQUALS expresion_logica'
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

def p_input(p):
	'''input	: INPUT LPAREN input1 RPAREN'''
	# METE mensaje a memoria
	cuadruplos.pTipos.pop()
	cuadruplos.countT += 1
	cuadruplos.dirCuadruplos.append((INPUT, cuadruplos.pOperandos.pop(), None, "t"+str(cuadruplos.countT)))
	cuadruplos.indexCuadruplos += 1
	# METE input a memoria
	cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
	cuadruplos.pTipos.append(STRING)
	cuadruplos.countT += 1
	p[0] = 'input'

def p_input1(p):
	'''input1	: expresion_logica
				| epsilon'''

def p_llamada(p):
	'''llamada 	: ID LPAREN llamada1 RPAREN
				| print
				| input'''
	if len(p) > 2:
		# Pedir memoria para funcion
		# [Tipo, DictVar, ListaParam, CantVarTemp, indexCuadruplo]
		print("*************MEMORY CREATED FOR FUNCTION: " + str(p[1]))
		if functionsDir.has_key(p[1]):
			cuadruplos.dirCuadruplos.append((ERA, len(functionsDir[p[1]][1]), functionsDir[p[1]][3], None))
			cuadruplos.indexCuadruplos += 1
			global function_ptr
			function_ptr = p[1]
		else:
			# Error
			print("Function %s is not declared!" %(p[-1]))
			exit(1)
		print("@@@@@@@@@@@@@@@@ countParam: " + str(countParam))
		# Verificar que countParam == len(parametros) de la funcion
		print('################ %s' %str(functionsDir[function_ptr]))
		if len(functionsDir[function_ptr][2]) == countParam:
			# Pila temporal para invertir orden de parametros
			pTempParam = []

			# Verifica que parametros recibidos sean del tipo que se espera en el mismo orden
			while (countParam > 0):
				if (functionsDir[function_ptr][2][countParam-1] != cuadruplos.pTipos[-1]):
					# Error
					print("Function: %s parameter %s type mismatch, expected %s!" %(p[1], parseType(cuadruplos.pTipos[-1]), parseType(functionsDir[function_ptr][2][countParam-1])))
					exit(1)
				else:
					pTempParam.append((cuadruplos.pTipos.pop(), cuadruplos.pOperandos.pop()))
				global countParam
				countParam -= 1

			# Genera cuadruplos de parametros
			while (len(pTempParam) > 0):
				cuadruplos.dirCuadruplos.append((PARAM, pTempParam[-1][1], pTempParam[-1][0], None))
				pTempParam.pop()
				cuadruplos.indexCuadruplos += 1

			# Genera cuadruplo GOSUB
			cuadruplos.dirCuadruplos.append((GOSUB, function_ptr, None, functionsDir[function_ptr][4]))
			cuadruplos.indexCuadruplos += 1
			print("PILA OPERANDOS: %s   PILA TIPOS: %s   PILA OPERADORES: %s" %(str(cuadruplos.pOperandos), str(cuadruplos.pTipos), str(cuadruplos.pOper)))
		else:
			# Error
			print("Function: %s expected %d parameter(s), recieved %d!" %(p[1], len(functionsDir[function_ptr][2]), countParam))
			exit(1)

		global countParam
		countParam = 0
		global function_ptr
		function_ptr = prev_Fuction_ptr
	p[0] = p[1]

def p_llamada1(p):
	'''llamada1 	: epsilon
					| expresion_logica llamada2'''
	if len(p) > 2:
		global countParam
		countParam += 1
	global prev_Fuction_ptr
	prev_Fuction_ptr = function_ptr

def p_llamada2(p):
	'''llamada2 	: epsilon
					| COMMA expresion_logica llamada2'''
	if len(p) > 2:
		global countParam
		countParam += 1

def p_main(p):
	'main : MAIN declareMain LCURL main1 estatuto main2 RCURL'
	functionsDir[p[1]][3] = cuadruplos.countT

def p_declareMain(p):
	'''declareMain : '''
	global function_ptr
	function_ptr = p[-1]
	cuadruplos.countT = 0
	if functionsDir.has_key(p[-1]) == False:
		# [Tipo, DictVar, ListaParam, CantVarTemp, indexCuadruplo]
		functionsDir[p[-1]] = ['main', {}, [], 0, cuadruplos.indexCuadruplos]
		t = cuadruplos.dirCuadruplos[0]
		t = t[:3] + (cuadruplos.indexCuadruplos,)
		cuadruplos.dirCuadruplos[0] = t
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

def p_parametros(p):
	'''parametros : tipo meteParam parametros1 ID parametros2
				| VECTOR tipo meteParamVect parametros1 ID parametros2'''

	#CAMBIO: agregar sacaParam si parametros 1 es por referencia y sacaParam mete el id a la pila de referencia de la funcion

def p_parametros1(p):
	'''parametros1 : AMPERSON
				| epsilon'''

def p_parametros2(p):
	'''parametros2 : COMMA parametros
				| epsilon'''
	#CAMBIO: checar que el id del parametro no sea una var global.

def p_meteParam(p):
	'meteParam : '
	# Mete parametro a lista de parametros de la funcion
	functionsDir[function_ptr][2].append(parseTypeIndex(p[-1]))


def p_meteParamVect(p):
	'meteParamVect : '
	# Mete parametro vector a lista de parametros de la funcion
	functionsDir[function_ptr][2].append(parseTypeIndex(p[-1]))

def p_print(p):
	'print : PRINT LPAREN expresion_logica RPAREN'
	printValue = cuadruplos.pOperandos.pop()
	if cuadruplos.pTipos.pop() == STRING and printValue[0] == '\"':
		# METE printValue a memoria
		cuadruplos.countT += 1
	cuadruplos.dirCuadruplos.append((PRINT, None, None, "t"+str(cuadruplos.countT)))
	cuadruplos.indexCuadruplos += 1
	p[0] = 'print'

def p_switch(p):
	'switch     : SWITCH ID meterIDPOper switch1 LCURL switch2 switch3 RCURL'
	cuadruplos.pOperandos.pop()
	cuadruplos.pTipos.pop()

	#rellenar goto's de switch
	while(len(cuadruplos.pSaltos)!=0):
		gotoIndex = cuadruplos.pSaltos.pop()
		t = cuadruplos.dirCuadruplos[gotoIndex]
		t = t[:3] + (cuadruplos.indexCuadruplos,)
		cuadruplos.dirCuadruplos[gotoIndex] = t


def p_switch1(p):
	'''switch1  : epsilon
	            | LBRACKET expresion_logica RBRACKET'''

def p_switch2(p):
	'''switch2  : epsilon
	            | CASE varcte compararConID checkEvaluacionLogica COLON switch4 checkPSaltos switch2'''

def p_switch3(p):
	'switch3  : DEFAULT COLON switch4'

def p_switch4(p):
	'''switch4  : LCURL PASS RCURL
				| bloque'''

def p_meterIDPOper(p):
	'meterIDPOper : '
	# Checa que ID exista y saca tipo de tabla de Var
	# Si existe mete valor a pOperandos y tipo a pTipos
	if globalVars.has_key(p[-1]):
		cuadruplos.pTipos.append(globalVars[p[-1]][0])
		cuadruplos.pOperandos.append(globalVars[p[-1]][1])
	elif functionsDir[function_ptr][1].has_key(p[-1]):
		cuadruplos.pTipos.append(functionsDir[function_ptr][1][p[-1]][0])
		cuadruplos.pOperandos.append(functionsDir[function_ptr][1][p[-1]][1])
	else:
		# Error
		print("Variable %s isn't declared! Line: %s" %(p[-1], lexer.lineno))
		exit(1)

def p_compararConID(p):
	'compararConID : '
	# Checa tipo de varcte
	if isinstance(p[-1], int):
		operandType2 = INT
		operand2 = p[-1]
	elif isinstance(p[-1], float):
		operandType2 = FLOAT
		operand2 = p[-1]
	elif p[-1] == 'true' or p[-1] == 'false':
		operandType2 = BOOL
		operand2 = p[-1]
	else:
		if globalVars.has_key(p[-1]):
	  			operandType2 = globalVars[p[-1]][0]
	  			operand2 = globalVars[p[-1]][1]
		elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
		  		operandType2 = functionsDir[function_ptr][1][p[-1]][0]
		  		operand2 = functionsDir[function_ptr][1][p[-1]][1]
		else:
			operandType2 = STRING
			operand2 = p[-1]
	operator = DOUBLE_EQUAL
	operand1 = cuadruplos.pOperandos[-1]
	operandType1 = cuadruplos.pTipos[-1]

	operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)

	if(operationType == BOOL):
		cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
		cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
		cuadruplos.pTipos.append(operationType)
		cuadruplos.indexCuadruplos += 1
		cuadruplos.countT += 1

	else:
		print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
		exit(1)

def p_termino(p):
	'termino 	: factor checkTERMPOper termino1'

def p_checkTERMPOper(p):
	'checkTERMPOper : '

	print "\n L590 checkTERMPOper"
	print "L591 operadores: %s" % str(cuadruplos.pOper)
	if (len(cuadruplos.pOper) != 0):
		if ((cuadruplos.pOper[-1] == MULT) or (cuadruplos.pOper[-1] == DIVIDE)):
			print("L594 operadores: %s" %(str(cuadruplos.pOper)))
			print("L595 operandos: %s" %(str(cuadruplos.pOperandos)))
			operator = cuadruplos.pOper.pop()
			operand2 = cuadruplos.pOperandos.pop()
			operand1 = cuadruplos.pOperandos.pop()
			print("L599 operandos con pop: %s" %(str(cuadruplos.pOperandos)))
			operandType2 = cuadruplos.pTipos.pop()
			operandType1 = cuadruplos.pTipos.pop()

			operationType = cuadruplos.cubo.getResultType(operandType1, operandType2, operator)
			if(operationType != ERROR):
				cuadruplos.dirCuadruplos.append((operator, operand1, operand2, "t"+str(cuadruplos.countT)))
				cuadruplos.pOperandos.append("t"+str(cuadruplos.countT))
				cuadruplos.pTipos.append(operationType)
				cuadruplos.indexCuadruplos += 1
				cuadruplos.countT += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, lexer.lineno))
				exit(1)
	print ("L613 index cuadruplos %d \n cuadruplos: %s" %(cuadruplos.indexCuadruplos, str(cuadruplos.dirCuadruplos)))

def p_termino1(p):
	'''termino1 : TIMES addOperator termino
				| DIVIDE addOperator termino
				| epsilon'''

def p_tipo(p):
	'''tipo 	: INT
				| FLOAT
				| BOOL
				| STRING'''
	p[0] = p[1]

def p_varcte(p):
	''' varcte 	: varcte1
				| CTE_INT
				| CTE_FLOAT
                | CTE_STRING
                | cte_bool'''
	p[0] = p[1]

def p_varcte1(p):
	''' varcte1 : ID checaID
				| llamada
				| cteVector'''
	p[0] = p[1]

def p_checaID(p):
	'''checaID : '''
	# Checa si ID existe

def p_cteVector(p):
	'''cteVector 	: ID LBRACKET expresion_logica RBRACKET'''
	# Evalua valor de vector y checa si existe vector
	p[0] = p[1]

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
		#CAMBIO: usar vartype para meter la direccion real a la tabla de variable.
		#todo: 1
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

def p_while(p):
	'while : WHILE metePSaltos LPAREN expresion_logica RPAREN checkEvaluacionLogica bloque'
	if (len(cuadruplos.pSaltos) != 0):
		gotoFIndex = cuadruplos.pSaltos.pop()
		cuadruplos.dirCuadruplos.append((GOTO, None, None, cuadruplos.pSaltos.pop()))
		cuadruplos.indexCuadruplos += 1
		t = cuadruplos.dirCuadruplos[gotoFIndex]
		t = t[:3] + (cuadruplos.indexCuadruplos,)
		cuadruplos.dirCuadruplos[gotoFIndex] = t

def p_metePSaltos(p):
	'metePSaltos :'
	cuadruplos.pSaltos.append(cuadruplos.indexCuadruplos)

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

	#Print Tokens
	# lexer.input(data)
	# from tok in lexer:
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
