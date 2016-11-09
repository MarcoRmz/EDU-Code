#########################################################
#														#
# 	EDU-Code.py											#
#														#
# 	Parser												#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581       				#
#														#
#########################################################

#########################################
#										#
#         		Imports          		#
#										#
#########################################

from scanner import *
import quadruples
from memoryHandler import *
import ply.yacc as yacc

#########################################
#										#
#         		Pointers          		#
#										#
#########################################

# Current Function pointer
function_ptr = "GLOBAL"

# Previous Function pointer
prev_Fuction_ptr = 'None'

#########################################
#										#
#         		Directories          	#
#										#
#########################################

# Global Variables
globalVars = {}

# Functions Directory
functionsDir = {}

# FROM Temp STACK
fromTempStack = []

# Parameter counter
countParam = 0

#########################################
#										#
#        Constants for Quadruples       #
#										#
#########################################

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
EOF = 99

#########################################
#										#
#    	Constants Parse Functions    	#
#										#
#########################################

# Function to parse token type value to equivalent numeric constant
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

# Function to parse constant to type value
def parseType(type):
	if type == INT:
		return 'INT'
	elif type == FLOAT:
		return 'FLOAT'
	elif type == BOOL:
		return 'BOOL'
	else:
		return 'STRING'

#########################################
#										#
#         	Grammar Rules          		#
#										#
#########################################

def p_programa(p):
	'programa 	: START gotoMAIN programa1 programa2 main END'
	# Generate quadruple for END OF FILE
	quadruples.dirQuadruples.append((EOF, None, None, None))
	quadruples.indexQuadruples += 1

def p_programa1(p):
	'''programa1 : var_declaracion programa1
				| epsilon'''

def p_programa2(p):
	'''programa2 : funcion programa2
				| epsilon'''

def p_gotoMAIN(p):
	'gotoMAIN : '
	# Generate quadruple GOTO MAIN
	quadruples.dirQuadruples.append((GOTO, None, None, None))
	quadruples.indexQuadruples += 1

def p_asignacion(p):
	'''asignacion : ID EQUALS asignacion1'''
	# Check if ID is a declared global variable
	print "ASIGNACION PILA DE OPERANDOS %s" % str(quadruples.sOperands)
	if globalVars.has_key(p[1]):
		# Check if assignment is valid given the types of the operands
		asignacionType = quadruples.cubo.getResultType(globalVars[p[1]][0], quadruples.sTypes[-1], EQUALS)

		if asignacionType != ERROR:
			newValueAddress = quadruples.sOperands.pop()
			quadruples.dirQuadruples.append((EQUALS,newValueAddress, None, globalVars[p[1]][1]))
			quadruples.sTypes.pop()
			quadruples.indexQuadruples += 1
		else:
			# Error
			print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], parseType(globalVars[p[1]][0]), parseType(quadruples.sTypes[-1]), p.lineno(0)))
			exit(1)
	else:
		# Check if ID is a declared local variable
		if functionsDir[function_ptr][1].has_key(p[1]):
			# Check if assignment is valid given the types of the operands
			asignacionType = quadruples.cubo.getResultType(functionsDir[function_ptr][1][p[1]][0], quadruples.sTypes[-1], EQUALS)

			if asignacionType != ERROR:
				newValueAddress = quadruples.sOperands.pop()
				quadruples.dirQuadruples.append((EQUALS, newValueAddress, None, functionsDir[function_ptr][1][p[1]][1]))
				quadruples.sTypes.pop()
				quadruples.indexQuadruples += 1
			else:
				# Error
				print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], parseType(functionsDir[function_ptr][1][p[1]][0]), parseType(quadruples.sTypes[-1]),p.lineno(0)))
				exit(1)
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[1], p.lineno(0)))
			exit(1)
	print "ASIGNACION PILA DE OPERANDOS %s" % str(quadruples.sOperands)

def p_asignacion1(p):
	'''asignacion1 : expresion_logica
				| asignacion_vector'''

def p_asignacion_vector(p):
	'''asignacion_vector : LBRACKET expresion_logica RBRACKET'''
	p[0] = p[1] + p[2] + p[3]

def p_bloque(p):
	'bloque 	: LCURL estatuto bloque1 RCURL'

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''

def p_condicion(p):
	'condicion 	: IF LPAREN expresion_logica RPAREN checkEvaluacionLogica condicion1 checkPSaltos condicion2 condicion3'
	# Fill out GOTO's for each condition
	while(len(quadruples.sJumps)!=0):
		gotoIndex = quadruples.sJumps.pop()
		t = quadruples.dirQuadruples[gotoIndex]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[gotoIndex] = t

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
	aux = quadruples.sTypes.pop()
	if aux == BOOL:
		# Generate GOTOF
		quadruples.dirQuadruples.append((GOTOF, quadruples.sOperands.pop(), None, None))
		quadruples.sJumps.append(quadruples.indexQuadruples)
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Evaluated expresion is type %s, not a bool! Line: %s" %(parseType(aux), p.lineno(-1)))
		exit(1)

def p_checkPSaltos(p):
	'''checkPSaltos : '''
	# Generate GOTO
	quadruples.dirQuadruples.append((GOTO, None, None, None))
	quadruples.indexQuadruples += 1

	if (len(quadruples.sJumps) != 0):
		gotoIndex = quadruples.sJumps.pop()
		t = quadruples.dirQuadruples[gotoIndex]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[gotoIndex] = t

	quadruples.sJumps.append(quadruples.indexQuadruples-1)

def p_do_while(p):
	''' do_while : DO metePSaltos bloque WHILE LPAREN expresion_logica RPAREN '''
	aux = quadruples.sTypes.pop()
	if aux == BOOL:
		# Generate GOTOT
		quadruples.dirQuadruples.append((GOTOT, quadruples.sOperands.pop(), None, quadruples.sJumps.pop()))
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Evaluated expresion is type %s, not a bool! Line: %s" %(parseType(aux), p.lineno(5)))
		exit(1)

def p_estatuto(p):
	'''estatuto : asignacion
				| llamada
				| return
				| condicion
				| switch
				| while
				| do_while
				| print
				| input
				| from'''

def p_exp(p):
	'exp 	: termino checkEXPPOper exp1'
	p[0] = p[1]

def p_checkEXPPOper(p):
	'checkEXPPOper : '
	if (len(quadruples.sOperators) != 0):
		if ((quadruples.sOperators[-1] == PLUS) or (quadruples.sOperators[-1] == MINUS)):
			
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			operationType = quadruples.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s   L211" % (str(operator), str(operand1), str(operand2))
				newValueAddress = getLocalAddress(operationType, 1)
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(operand1, operand2, operator, p.lineno(0)))
				exit(1)

def p_exp1(p):
	''' exp1 	: PLUS addOperator exp
				| MINUS addOperator exp
				| epsilon'''

def p_addOperator(p):
	'''addOperator : '''
	if p[-1] == '*':
		quadruples.sOperators.append(MULT)
	elif p[-1] == '/':
		quadruples.sOperators.append(DIVIDE)
	elif p[-1] == '+':
		quadruples.sOperators.append(PLUS)
	elif p[-1] == 'and':
		quadruples.sOperators.append(AND)
	elif p[-1] == 'or':
		quadruples.sOperators.append(OR)
	elif p[-1] == '<=':
		quadruples.sOperators.append(LESSEQUAL)
	elif p[-1] == '>=':
		quadruples.sOperators.append(GREATEREQUAL)
	elif p[-1] == '==':
		quadruples.sOperators.append(DOUBLE_EQUAL)
	elif p[-1] == '!=':
		quadruples.sOperators.append(DIFF)
	elif p[-1] == '<':
		quadruples.sOperators.append(LESS)
	elif p[-1] == '>':
		quadruples.sOperators.append(GREATER)
	else:
		quadruples.sOperators.append(MINUS)

def p_expresion(p):
	'expresion 	: exp checkEXPRESIONPOper expresion1'
	p[0] = p[1]

def p_checkEXPRESIONPOper(p):
	'checkEXPRESIONPOper : '
	if (len(quadruples.sOperators) != 0):
		if ((quadruples.sOperators[-1] == LESS) or (quadruples.sOperators[-1] == LESSEQUAL) or (quadruples.sOperators[-1] == GREATER) or (quadruples.sOperators[-1] == GREATEREQUAL) or (quadruples.sOperators[-1] == DOUBLE_EQUAL) or (quadruples.sOperators[-1] == DIFF)):
			
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			operationType = quadruples.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L273  " % (str(operator), str(operand1), str(operand2))
				newValueAddress = getLocalAddress(operationType, 1)
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, p.lineno(0)))
				exit(1)

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
	print("-----------------")
	print("tipos:")
	print(quadruples.sTypes)
	print("---")
	print("operandos:")
	print(quadruples.sOperands)
	print("---")
	print("operadores:")
	print(quadruples.sOperators)
	print ("quadruples:\n%s" %(str(quadruples.dirQuadruples)))
	print("-----------------\n")
	p[0] = p[1]

def p_checkEXPRESIONLOGICAPOper(p):
	'checkEXPRESIONLOGICAPOper : '
	if (len(quadruples.sOperators) != 0):
		if ((quadruples.sOperators[-1] == AND) or (quadruples.sOperators[-1] == OR)):
			
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			operationType = quadruples.cubo.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				print "OPERATOR: %s OPERAND1: %s OPERAND2: %s L312  " % (str(operator), str(operand1), str(operand2))
				newValueAddress = getLocalAddress(operationType, 1)
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, p.lineno(0)))
				exit(1)
def p_expresion_logica1(p):
	'''expresion_logica1 	: AND addOperator expresion_logica
					| epsilon
					| OR addOperator expresion_logica'''

def p_factor(p):
	''' factor	: LPAREN factorAddFakeCover expresion_logica RPAREN
				| factor1'''
	if len(p) == 5:
		quadruples.sOperators.pop()
	p[0] = p[1]

def p_factorAddFakeCover(p):
	'factorAddFakeCover : '
	quadruples.sOperators.append('(')
	p[0] = p[-1]

def p_factor1(p):
	''' factor1 : varcte'''
	p[0] = p[1]

def p_cteFrom(p):
	''' cteFrom : PLUS CTE_INT
				| MINUS CTE_INT
				| CTE_INT'''
	if len(p) == 3:
		# Verify PLUS & MINUS is used only on INT
		if (isinstance(p[2], int)):
			if (p[1] == '-'):
				p[0] = p[2] * -1
			else:
				p[0] = p[2]
	else:
		p[0] = p[1]

def p_from(p):
	'from : FROM cteFrom creaVarTemp TO cteFrom crearComparacion BY LPAREN from1 cteFrom RPAREN bloque'
	# Actualiza valor en fromTempStack
	newAddress= setConstantAddress(INT,p[10])
	tempAddress= getLocalAddress(INT,1)
	if p[9] == '+':
		quadruples.dirQuadruples.append(PLUS,fromTempStack[-1],newAddress,tempAddress)
	elif p[9] == '-':
		quadruples.dirQuadruples.append(MINUS,fromTempStack[-1],newAddress,tempAddress)
	elif p[9] == '*':
		quadruples.dirQuadruples.append(MULT,fromTempStack[-1],newAddress,tempAddress)
	elif p[9] == '/':
		quadruples.dirQuadruples.append(DIVIDE,fromTempStack[-1],newAddress,tempAddress)

	# Genera GOTO
	gotoFIndex = quadruples.sJumps.pop()
	quadruples.dirQuadruples.append((GOTO, None, None, quadruples.sJumps.pop()))
	quadruples.indexQuadruples += 1
	t = quadruples.dirQuadruples[gotoFIndex]
	t = t[:3] + (quadruples.indexQuadruples,)
	quadruples.dirQuadruples[gotoFIndex] = t

	# Pop fromTempStack
	fromTempStack.pop()

def p_from1(p):
	'''from1	: PLUS
			| TIMES
			| DIVIDE
			| MINUS'''

def p_creaVarTemp(p):
	'creaVarTemp : '
	#add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])

	#create copy in temporal
	tempAddress = getLocalAddress(INT,1)
	quadruples.dirQuadruples.append((EQUALS,newAddress,None,tempAddress))
	quadruples.indexQuadruples += 1
	#add to the tempStack
	fromTempStack.append(tempAddress)

	quadruples.sOperands.append(p[-1])

def p_crearComparacion(p):
	'crearComparacion : '

	#add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])



	#Gets bool memory address
	boolAddress = getLocalAddress(BOOL,1)


	if quadruples.sOperands.pop() >= p[-1]:
		# comparacion >=
		quadruples.dirQuadruples.append((GREATEREQUAL, fromTempStack[-1], newAddress, boolAddress))
		quadruples.indexQuadruples += 1

	else:
		# comparacion <=
		quadruples.dirQuadruples.append((LESSEQUAL, fromTempStack[-1], newAddress, boolAddress))
		quadruples.indexQuadruples += 1

	#GOTO
	quadruples.sJumps.append(quadruples.indexQuadruples)

	quadruples.dirQuadruples.append((GOTOF, boolAddress, None, None))
	quadruples.sJumps.append(quadruples.indexQuadruples)
	quadruples.indexQuadruples += 1

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
	'''funcion5	: ID declareFunc LPAREN funcion3 RPAREN LCURL funcion1 estatuto funcion2 RCURL'''
	# Generate ENDPROC
	quadruples.dirQuadruples.append((ENDPROC, None, None, None))
	quadruples.indexQuadruples += 1

def p_declareFunc(p):
	'''declareFunc : '''
	global function_ptr
	function_ptr = p[-1]
	#CAMBIO: Todo 2 y 3
	if functionsDir.has_key(p[-1]) == False:
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress]
		functionAddress = None
		if parseTypeIndex(p[-2]) != 23:
			functionAddress =  getGlobalAddress(parseTypeIndex(p[-2]), 1)
		functionsDir[p[-1]] = [parseTypeIndex(p[-2]), {}, [], quadruples.indexQuadruples, functionAddress]
	else:
		# Error
		print("Function %s already declared!" %(p[-1]))
		exit(1)

def p_return(p):
	'''return	: RETURN expresion_logica'''
	# Verify type of function
	if functionsDir[function_ptr][0] != VOID:
		# Generate RETURN with value to return and address to return it to
		quadruples.sTypes.pop()
		quadruples.dirQuadruples.append((RETURN, quadruples.sOperands.pop(), None, functionsDir[function_ptr][4]))
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Invalid operation RETURN on VOID Function: %s! Line: %s" %(function_ptr, p.lineno(1)))
		exit(1)

def p_input(p):
	'''input	: INPUT LPAREN input1 RPAREN'''
	# METE mensaje a memoria
	quadruples.sTypes.pop()
	quadruples.countT += 1
	quadruples.dirQuadruples.append((INPUT, quadruples.sOperands.pop(), None, "t"+str(quadruples.countT)))
	quadruples.indexQuadruples += 1
	# METE input a memoria
	quadruples.sOperands.append("t"+str(quadruples.countT))
	quadruples.sTypes.append(STRING)
	quadruples.countT += 1
	p[0] = 'input'

def p_input1(p):
	'''input1	: expresion_logica
				| epsilon'''

def p_llamada(p):
	'''llamada 	: ID LPAREN llamada1 RPAREN'''
	# Pedir memoria para funcion
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress]
	print("************* FUNCTION CALL FOR: " + str(p[1]))
	if functionsDir.has_key(p[1]):
		if functionsDir[p[1]][0] == 23:
			intCounter = 0
			floatCounter = 0
			stringCounter = 0
			boolCounter = 0

			# Iterates function dictionary to count how many variables per type
			for value in functionsDir[p[1]][1].values():
				if value[0] == INT:
					intCounter += 1
				elif value[0] == FLOAT:
					floatCounter += 1
				elif value[0] == STRING:
					stringCounter += 1
				elif value[0] == BOOL:
					boolCounter += 1

			subTypeQty = (intCounter, floatCounter, stringCounter, boolCounter)
			totalTypes = 0

			# Iterates subTypeQty to count how many types are used
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, functionsDir[p[1]][4]))
			quadruples.indexQuadruples += 1
			global function_ptr
			function_ptr = p[1]
		else:
			# Error
			print("Function %s is not void, must be assigned for return value!" %(p[1]))
			exit(1)
	else:
		# Error
		print("Function %s is not declared!" %(p[1]))
		exit(1)

	print("@@@@@@@@@@@@@@@@ countParam: " + str(countParam))
	# Verificar que countParam == len(parametros) de la funcion
	print('################ %s' %str(functionsDir[function_ptr]))
	if len(functionsDir[function_ptr][2]) == countParam:
		# Verifica que parametros recibidos sean del tipo que se espera en el mismo orden
		while (countParam > 0):
			varID = functionsDir[function_ptr][2][countParam-1]
			varType = functionsDir[function_ptr][1][varID][0]
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s!" %(p[1], parseType(quadruples.sTypes[-1]), parseType(varType)))
				exit(1)
			else:
				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), quadruples.sOperands.pop(), functionsDir[function_ptr][1][varID][1]))
				quadruples.indexQuadruples += 1
			global countParam
			countParam -= 1

		# Genera cuadruplo GOSUB
		quadruples.dirQuadruples.append((GOSUB, function_ptr, None, functionsDir[function_ptr][3]))
		quadruples.indexQuadruples += 1
		print("PILA OPERANDOS: %s   PILA TIPOS: %s   PILA OPERADORES: %s" %(str(quadruples.sOperands), str(quadruples.sTypes), str(quadruples.sOperators)))
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d!" %(p[1], len(functionsDir[function_ptr][2]), countParam))
		exit(1)

	global countParam
	countParam = 0
	global function_ptr
	function_ptr = prev_Fuction_ptr

	p[0] = 'Llamada ' + str(p[1])

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

def p_llamada3(p):
	'''llamada3 : LPAREN llamada1 RPAREN'''
	# Pedir memoria para funcion
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress]
	print("************* FUNCTION CALL FOR: " + str(p[-1]))
	if functionsDir.has_key(p[-1]):
		if functionsDir[p[-1]][0] != 23:
			intCounter = 0
			floatCounter = 0
			stringCounter = 0
			boolCounter = 0

			# Iterates function dictionary to count how many variables per type
			for value in functionsDir[p[-1]][1].iteritems():
				if value[0] == INT:
					intCounter += 1
				elif value[0] == FLOAT:
					floatCounter += 1
				elif value[0] == STRING:
					stringCounter += 1
				elif value[0] == BOOL:
					boolCounter += 1

			# Iterates function parameter list to count how many variables per type
			for value in functionsDir[p[-1]][2]:
				if value == INT:
					intCounter += 1
				elif value == FLOAT:
					floatCounter += 1
				elif value == STRING:
					stringCounter += 1
				elif value == BOOL:
					boolCounter += 1

			subTypeQty = (intCounter, floatCounter, stringCounter, boolCounter)
			totalTypes = 0

			# Iterates subTypeQty to count how many types are used
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, functionsDir[p[-1]][4]))
			quadruples.indexQuadruples += 1
			global function_ptr
			function_ptr = p[-1]
		else:
			# Error
			print("Function %s is void, it can't be assigned!" %(p[-1]))
			exit(1)
	else:
		# Error
		print("Function %s is not declared!" %(p[-1]))
		exit(1)
	print("@@@@@@@@@@@@@@@@ countParam: " + str(countParam))
	# Verificar que countParam == len(parametros) de la funcion
	print('################ %s' %str(functionsDir[function_ptr]))
	if len(functionsDir[function_ptr][2]) == countParam:
		# Verifica que parametros recibidos sean del tipo que se espera en el mismo orden
		while (countParam > 0):
			varID = functionsDir[function_ptr][2][countParam-1]
			varType = functionsDir[function_ptr][1][varID][0]
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s!" %(p[-1], parseType(quadruples.sTypes[-1]), parseType(varType)))
				exit(1)
			else:
				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), quadruples.sOperands.pop(), functionsDir[function_ptr][1][varID][1]))
				quadruples.indexQuadruples += 1
			global countParam
			countParam -= 1

		# Genera cuadruplo GOSUB
		quadruples.dirQuadruples.append((GOSUB, function_ptr, None, functionsDir[function_ptr][3]))
		quadruples.indexQuadruples += 1
		print("PILA OPERANDOS: %s   PILA TIPOS: %s   PILA OPERADORES: %s" %(str(quadruples.sOperands), str(quadruples.sTypes), str(quadruples.sOperators)))
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d!" %(p[-1], len(functionsDir[function_ptr][2]), countParam))
		exit(1)

	global countParam
	countParam = 0
	global function_ptr
	function_ptr = prev_Fuction_ptr
	p[0] = 'Llamada ' + str(p[-1])

def p_main(p):
	'main : MAIN declareMain LCURL main1 estatuto main2 RCURL'

def p_declareMain(p):
	'''declareMain : '''
	global function_ptr
	function_ptr = p[-1]

	# Check Main function is unique
	if functionsDir.has_key(p[-1]) == False:
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress]
		functionsDir[p[-1]] = ['main', {}, [], quadruples.indexQuadruples, None]
		t = quadruples.dirQuadruples[0]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[0] = t
	else:
		# Error
		print("Main %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)

def p_main1(p):
	'''main1 : var_declaracion main1
				| epsilon'''

def p_main2(p):
	'''main2 : estatuto main2
				| epsilon'''

def p_parametros(p):
	''' parametros : tipo meteParamTipo parametros1 ID meteParam parametros2
					| VECTOR tipo meteParamTipoVect parametros1 ID meteParamVect parametros2'''
	#CAMBIO: agregar sacaParam si parametros1 es por referencia y sacaParam mete el id a la pila de referencia de la funcion

def p_parametros1(p):
	'''parametros1 : AMPERSON
				| epsilon'''

def p_parametros2(p):
	'''parametros2 : COMMA parametros
				| epsilon'''

def p_meteParamTipo(p):
	'meteParamTipo : '
	print("ENTRO A meteParamTipo L762 con %s" %(str(p[-1])))
	# Mete parametro a lista de parametros de la funcion
	functionsDir[function_ptr][2].append(parseTypeIndex(p[-1]))
	print("PARAMETRO TIPO LISTAPARAM %s" %functionsDir[function_ptr][2])
	# Reserves memory space for parameter
	#varAddress = getLocalAddress(parseTypeIndex(p[-1]), 1)

def p_meteParamTipoVect(p):
	'meteParamTipoVect : '
	# Mete parametro vector a lista de parametros de la funcion
	functionsDir[function_ptr][2].append(parseTypeIndex(p[-1]))
	# CAMBIO: reservar memoria para parametro arreglo
	# Reserves memory space for vector parameter

def p_meteParam(p):
	'meteParam : '
	#CAMBIO: checar que el id del parametro no sea una var global.
	print("ENTRO A parametros2 con %s L760" %(str(p[-1])))
	# Check if ID exists
	print("FOUND PARAMETER DECLR AT FUNCTION: " + function_ptr)
	if globalVars.has_key(p[-1]):
		# ERROR
		print("ID: %s is a global variable, can't be used as a parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
		# ERROR
		print("ID: %s is a duplicate parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	else:
		varAddress = getLocalAddress(functionsDir[function_ptr][2][-1], 1)
		functionsDir[function_ptr][1][p[-1]] = [functionsDir[function_ptr][2].pop(), varAddress]
		functionsDir[function_ptr][2].append(p[-1])
	print("PARAMETRO ID LISTAPARAM %s" %functionsDir[function_ptr][2])
	p[0] = varAddress

def p_meteParamVect(p):
	'meteParamVect : '
	#CAMBIO: checar que el id del parametro no sea una var global.
	print("ENTRO A parametros2 con %s L760" %(str(p[-1])))
	# Check if ID exists
	print("FOUND PARAMETER DECLR AT FUNCTION: " + function_ptr)
	if globalVars.has_key(p[-1]):
		# ERROR
		print("ID: %s is a global variable, can't be used as a parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
		# ERROR
		print("ID: %s is a duplicate parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	else:
		varAddress = getLocalAddress(functionsDir[function_ptr][2][-1], 1)
		functionsDir[function_ptr][1][p[-1]] = [functionsDir[function_ptr][2][-1], varAddress]
	p[0] = varAddress

def p_print(p):
	'print : PRINT LPAREN expresion_logica RPAREN'
	printValue = quadruples.sOperands.pop()
	quadruples.dirQuadruples.append((PRINT, None, None, printValue))
	quadruples.indexQuadruples += 1
	p[0] = 'print'

def p_switch(p):
	'switch     : SWITCH ID meterIDPOper switch1 LCURL switch2 switch3 RCURL'
	quadruples.sOperands.pop()
	quadruples.sTypes.pop()

	#rellenar goto's de switch
	while(len(quadruples.sJumps)!=0):
		gotoIndex = quadruples.sJumps.pop()
		t = quadruples.dirQuadruples[gotoIndex]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[gotoIndex] = t

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
	# Si existe mete valor a sOperands y tipo a sTypes
	if globalVars.has_key(p[-1]):
		newAddress = getGlobalAddress(globalVars[p[-1]][0], 1)
		quadruples.sTypes.append(globalVars[p[-1]][0])
		quadruples.sOperands.append(newAddress)
	elif functionsDir[function_ptr][1].has_key(p[-1]):
		newAddress = getLocalAddress(functionsDir[function_ptr][1][p[-1]][0], 1)
		quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
		quadruples.sOperands.append(newAddress)
	else:
		# Error
		print("Variable %s isn't declared! Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)

def p_compararConID(p):
	'compararConID : '
	# Checa tipo de varcte
	if isinstance(p[-1], int):
		operandType2 = INT
		operand2 = setConstantAddress(operandType2, p[-1])
	elif isinstance(p[-1], float):
		operandType2 = FLOAT
		operand2 = setConstantAddress(operandType2, p[-1])
	elif p[-1] == 'true' or p[-1] == 'false':
		operandType2 = BOOL
		operand2 = setConstantAddress(operandType2, p[-1])
	else:
		if globalVars.has_key(p[-1]):
	  			operandType2 = globalVars[p[-1]][0]
	  			operand2 = globalVars[p[-1]][1]
		elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
		  		operandType2 = functionsDir[function_ptr][1][p[-1]][0]
		  		operand2 = functionsDir[function_ptr][1][p[-1]][1]
		else:
			operandType2 = STRING
			operand2 = getLocalAddress(STRING, 1)
			# SET VALUE FOR STRING
			setValue(newValueAddress, p[-1])

	operator = DOUBLE_EQUAL
	operand1 = quadruples.sOperands[-1]
	operandType1 = quadruples.sTypes[-1]

	operationType = quadruples.cubo.getResultType(operandType1, operandType2, operator)

	if(operationType == BOOL):
		newAddress = getLocalAddress(operationType, 1)
		quadruples.dirQuadruples.append((operator, operand1, operand2, newAddress))
		quadruples.sOperands.append(newAddress)
		quadruples.sTypes.append(operationType)
		quadruples.indexQuadruples += 1

	else:
		print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, p.lineno(-1)))
		exit(1)

def p_termino(p):
	'termino 	: factor checkTERMPOper termino1'
	p[0] = p[1]

def p_checkTERMPOper(p):
	'checkTERMPOper : '
	if (len(quadruples.sOperators) != 0):
		if ((quadruples.sOperators[-1] == MULT) or (quadruples.sOperators[-1] == DIVIDE)):
			
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			operationType = quadruples.cubo.getResultType(operandType1, operandType2, operator)
			if(operationType != ERROR):
				newValueAddress = getLocalAddress(operationType, 1)
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %s" %(operand1, operand2, operator, p.lineno(0)))
				exit(1)

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
				| cte_int1
				| cte_float1
                | varstring1
                | cte_bool'''
	p[0] = p[1]

def p_varcte1(p):
	''' varcte1 : ID varcte2'''
	p[0] = p[2]

def p_varcte2(p):
	''' varcte2 : epsilon
				| factorAddFakeCover llamada3
				| factorAddFakeCover LBRACKET expresion checarExpresion RBRACKET'''
	if len(p) == 2:
		# Check if ID exists
		print("FOUND ID: %s AT FUNCTION: %s" %(str(p[-1]), function_ptr))
		if globalVars.has_key(p[-1]):
			varAddress = globalVars[p[-1]][1]
	  		quadruples.sTypes.append(globalVars[p[-1]][0])
		elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
			varAddress = functionsDir[function_ptr][1][p[-1]][1]
		  	quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
		else:
			# ERROR
			print("ID: %s not declared at line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		quadruples.sOperands.append(varAddress)
		p[0] = varAddress
	elif len(p) == 3:
		# Verify function call exists
		print("FOUND CALL: %s AT FUNCTION: %s" %(str(p[-1]), function_ptr))
		if functionsDir.has_key(p[-1]):
			# Create local variable if function type is != VOID
			if functionsDir[p[-1]][0] != VOID:
				varAddress = getLocalAddress(functionsDir[p[-1]][0], 1)
				quadruples.sOperands.append(varAddress)
				quadruples.sTypes.append(functionsDir[p[-1]][0])
				p[0] = varAddress
				print("%s FUNCTION FOUND" %(parseType(functionsDir[p[-1]][0])))
			else:
				quadruples.sOperands.append(p[-1])
				quadruples.sTypes.append(functionsDir[p[-1]][0])
				p[0] = p[-1]
				print("VOID FUNCTION FOUND")
			print("PILA TIPOS DESPUES DE FUNCTION CALL: %s" %(str(quadruples.sTypes)))
		else:
			# ERROR
			print("Function: %s is not declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		# Remove fake cover
		quadruples.sOperators.pop()
	else:
		# Verify Vector exists
		# Remove fake cover
		quadruples.sOperators.pop()
		quadruples.sOperands.append(varAddress)
		quadruples.sTypes.append()
		p[0] = varAddress


def p_cte_int1(p):
	''' cte_int1 : PLUS CTE_INT
				| MINUS CTE_INT
				| CTE_INT'''
	quadruples.sTypes.append(INT)
	# Insert Value to dictionary and add address to Operands
	if len(p) == 3:
		if (p[1] == '-'):
			newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[2]*-1)
			quadruples.sOperands.append(newValueAddress)
		else:
			newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[2])
			quadruples.sOperands.append(newValueAddress)
	else:
		newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
		quadruples.sOperands.append(newValueAddress)
	p[0] = newValueAddress

def p_cte_float1(p):
	''' cte_float1 : PLUS CTE_FLOAT
				| MINUS CTE_FLOAT
				| CTE_FLOAT'''
	quadruples.sTypes.append(FLOAT)
	# Insert Value to dictionary and add address to Operands
	if len(p) == 3:
		if (p[1] == '-'):
			newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[2]*-1)
			quadruples.sOperands.append(newValueAddress)
		else:
			newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[2])
			quadruples.sOperands.append(newValueAddress)
	else:
		newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
		quadruples.sOperands.append(newValueAddress)
	p[0] = newValueAddress

def p_varstring1(p):
	''' varstring1 : VARSTRING'''
	quadruples.sTypes.append(STRING)
	# Insert Value to dictionary and add address to Operands
	newValueAddress = getLocalAddress(quadruples.sTypes[-1], 1)

	# SET VALUE FOR STRINGS
	setValue(newValueAddress, p[1])

	quadruples.sOperands.append(newValueAddress)
	p[0] = newValueAddress

def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''
	quadruples.sTypes.append(BOOL)
	# Insert Value to dictionary and add address to Operands
	newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
	quadruples.sOperands.append(newValueAddress)
	p[0] = newValueAddress

def p_checarExpresion(p):
	'''checarExpresion : '''
	# Checa si p[-1] es una CTE_INT

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
	# CAMBIO: cambiar sintaxis y diagrama para aceptar [tamano]

def p_declareVar(p):
	'''declareVar :'''
	if function_ptr == 'GLOBAL':
  		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
  		varType = parseTypeIndex(p[-2])
		varAddress = getGlobalAddress(varType, 1)
  		globalVars[p[-1]] = [varType, varAddress]
	else:
		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
  		elif functionsDir[function_ptr][1].has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
		varType = parseTypeIndex(p[-2])
		varAddress = getLocalAddress(varType, 1)
		functionsDir[function_ptr][1][p[-1]] = [varType, varAddress]
	p[0] = p[-1]

def p_declareVar2(p):
	'''declareVar2 :'''
	# CAMBIO: pedir direccion para vectores usando el tamano del arreglo para chunkSize
	if function_ptr == 'GLOBAL':
  		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
  		varType = parseTypeIndex(p[-2])
  		globalVars[p[-1]] = [varType, 'ValueNone']
	else:
		if globalVars.has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
  		elif functionsDir[function_ptr][1].has_key(p[-1]):
  			# Error
  			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
  			exit(1)
  		varType = parseTypeIndex(p[-2])
	  	functionsDir[function_ptr][1][p[-1]] = ['VECTOR ' + str(varType), 'ValueNone']
	p[0] = p[-1]

def p_while(p):
	'while : WHILE metePSaltos LPAREN expresion_logica RPAREN checkEvaluacionLogica bloque'
	if (len(quadruples.sJumps) != 0):
		gotoFIndex = quadruples.sJumps.pop()
		quadruples.dirQuadruples.append((GOTO, None, None, quadruples.sJumps.pop()))
		quadruples.indexQuadruples += 1
		t = quadruples.dirQuadruples[gotoFIndex]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[gotoFIndex] = t

def p_metePSaltos(p):
	'metePSaltos :'
	quadruples.sJumps.append(quadruples.indexQuadruples)


def p_epsilon(p):
	'epsilon :'
	pass

def p_error(p):
	if p:
		print("Syntax error at token: '%s' with value: '%s' at line: %d" %(p.type, p.value, p.lineno))
		# Discard the token
		parser.errok()
	else:
		print("Syntax error at EOF")
	exit(1)

#########################################
#										#
#         Logging Object Rules          #
#										#
#########################################

import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

parser = yacc.yacc(debug=True)

#########################################
#										#
#         		Main          			#
#										#
#########################################

import sys

if __name__ == '__main__':

	# Check for argument on file name to read
	if (len(sys.argv) > 1):
		fin = sys.argv[1]
	else:
		print("No file provided!")
		exit(1)

	# Open and read file
	f = open(fin, 'r')
	data = f.read()

	#Print Tokens
	# lexer.input(data)
	# from tok in lexer:
	# 	print(tok)

	# Parse tokens read
	parser.parse(data, tracking=True, debug=log)

	print("*****************************************")
	print("globalVars: ")
	print(globalVars)
	print("*****************************************")
	print("functionDir: ")
	print(functionsDir)
	print("*****************************************")
	print("quadruples: ")
	print(quadruples.dirQuadruples)
	print("operadores: ")
	print(quadruples.sOperators)
	print("operandos: ")
	print(quadruples.sOperands)
	print("*****************************************")
	print("Num quadruples: " + str(quadruples.indexQuadruples))
	print("*****************************************")
	print("\nSuccessful")
