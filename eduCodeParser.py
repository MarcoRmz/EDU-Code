#########################################################
#														#
# 	eduCodeParser.py									#
#														#
# 	Parser												#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581						#
#														#
#########################################################

#########################################
#										#
#		 		Imports					#
#										#
#########################################

from scanner import *
import quadruples
from memoryHandler import *
import ply.yacc as yacc

#########################################
#										#
#		 		Pointers				#
#										#
#########################################

# Current Function pointer
function_ptr = "GLOBAL"

#########################################
#										#
#		 		Directories				#
#										#
#########################################

# Global Variables
globalVars = {}
globalVarsTypeCounts = [0,0,0,0]

# Functions Directory
functionsDir = {}

# FROM Temp STACK
fromTempStack = []

# List of variables to print
printList = []

# Parameter counter
countParam = 0

#########################################
#										#
#		Constants for Quadruples		#
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
VER = 23
PLUS_ADDR = 24
REFERENCE_PARAM = 25
EOF = 99

#########################################
#										#
#		Constants Parse Functions		#
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
#		 	Grammar Rules				#
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
	# Create memory for main
	quadruples.dirQuadruples.append((ERA, None, None, None))
	quadruples.indexQuadruples += 1

	# Generate quadruple GOTO MAIN
	quadruples.dirQuadruples.append((GOTO, None, None, None))
	quadruples.indexQuadruples += 1

def p_asignacion(p):
	'''asignacion : ID asignacion1 EQUALS asignacion2'''
	operand2 = quadruples.sOperands.pop()
	operandType2 = quadruples.sTypes.pop()
	operand1 = quadruples.sOperands.pop()
	operandType1 = quadruples.sTypes.pop()
	# Compare if operand1 type and operand2 are compatible
	asignacionType = quadruples.getResultType(operandType1, operandType2, EQUALS)

	if asignacionType != ERROR:
		quadruples.dirQuadruples.append((EQUALS, operand2, None, operand1))
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Type mismatch var: %s of type: %s and %s! Line: %s" %(p[1], operandType1, operandType2, p.lineno(0)))
		exit(1)

def p_asignacion1(p):
	'''asignacion1 : epsilon
				| LBRACKET expresion_logica RBRACKET'''
	# Check if ID exists in global Vars
	varSize = setConstantAddress(INT, 1)
	if globalVars.has_key(p[-1]):
		# If ID is a vector add index address to sOperands
		if len(p) == 4:
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				quadruples.indexQuadruples += 1

				# Get local variable for addition
				newValueAddress = getLocalAddress(INT, varSize)

				# Add index to vector base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				quadruples.indexQuadruples += 1

				# Add index address to sOperands
				quadruples.sOperands.append([newValueAddress])
			else:
				# Error
				print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)
		else:
			# Check id is not a vector
			if globalVars[p[-1]][2] == varSize:
				# Add ID address to sOperands
				quadruples.sOperands.append(globalVars[p[-1]][1])
			else:
				# ERROR
				print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)

		# Add ID type to sTypes
		quadruples.sTypes.append(globalVars[p[-1]][0])
	else:
		# Check if ID exists in local Vars
		if functionsDir[function_ptr][1].has_key(p[-1]):
			# If ID is a vector add index address to sOperands
			if len(p) == 4:
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[function_ptr][1][p[-1]][2]))
					quadruples.indexQuadruples += 1

					# Get local variable for addition
					newValueAddress = getLocalAddress(INT, varSize)

					# Add index to vector base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[function_ptr][1][p[-1]][1], newValueAddress))
					quadruples.indexQuadruples += 1

					# Add index address to sOperands
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)
			else:
				# Check id is not a vector
				if functionsDir[function_ptr][1][p[-1]][2] == varSize:
					# Add ID address to sOperands
					quadruples.sOperands.append(functionsDir[function_ptr][1][p[-1]][1])
				else:
					# ERROR
					print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

			# Add ID type to sTypes
			quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
		else:
			# Error
			print("Variable %s is not declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)

def p_asignacion2(p):
	'''asignacion2 : expresion_logica
				| input'''

def p_bloque(p):
	'bloque 	: LCURL estatuto bloque1 RCURL'

def p_bloque1(p):
	'''bloque1 	: estatuto bloque1
				| epsilon'''

def p_condicion(p):
	'condicion 	: IF addConditionFakeCover LPAREN expresion_logica RPAREN checkEvaluacionLogica condicion1 checkPSaltos condicion2 condicion3'
	# Fill out GOTO's for each condition
	while(quadruples.sJumps[-1] != '('):
		gotoIndex = quadruples.sJumps.pop()
		t = quadruples.dirQuadruples[gotoIndex]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[gotoIndex] = t

	# Remove cover
	if quadruples.sJumps[-1] == '(':
		quadruples.sJumps.pop()

def p_addConditionFakeCover(p):
	'addConditionFakeCover 	: '
	quadruples.sJumps.append('(')

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

			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(operationType, varSize)
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(operand1, operand2, operator, p.lineno(-1)))
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

			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(operationType, varSize)
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

			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(operationType, varSize)
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
	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)
	# Actualiza valor en fromTempStack
	newAddress = setConstantAddress(INT,p[10])
	tempAddress = getLocalAddress(INT,varSize)
	if p[9] == '+':
		quadruples.dirQuadruples.append((PLUS,fromTempStack[-1],newAddress,tempAddress))
	elif p[9] == '-':
		quadruples.dirQuadruples.append((MINUS,fromTempStack[-1],newAddress,tempAddress))
	elif p[9] == '*':
		quadruples.dirQuadruples.append((MULT,fromTempStack[-1],newAddress,tempAddress))
	elif p[9] == '/':
		quadruples.dirQuadruples.append((DIVIDE,fromTempStack[-1],newAddress,tempAddress))
	quadruples.indexQuadruples += 1

	quadruples.dirQuadruples.append((EQUALS,tempAddress, None, fromTempStack[-1]))
	quadruples.indexQuadruples += 1

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
	p[0] = p[1]

def p_creaVarTemp(p):
	'creaVarTemp : '
	#add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])

	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)

	#create copy in temporal
	tempAddress = getLocalAddress(INT,varSize)
	quadruples.dirQuadruples.append((EQUALS,newAddress,None,tempAddress))
	quadruples.indexQuadruples += 1
	
	# Add to the tempStack
	fromTempStack.append(tempAddress)

	quadruples.sOperands.append(p[-1])

def p_crearComparacion(p):
	'crearComparacion : '

	#add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])

	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)

	#Gets bool memory address
	boolAddress = getLocalAddress(BOOL,varSize)

	#GOTO sJump
	quadruples.sJumps.append(quadruples.indexQuadruples)

	if quadruples.sOperands.pop() >= p[-1]:
		# comparacion >=
		quadruples.dirQuadruples.append((GREATEREQUAL, fromTempStack[-1], newAddress, boolAddress))
		quadruples.indexQuadruples += 1

	else:
		# comparacion <=
		quadruples.dirQuadruples.append((LESSEQUAL, fromTempStack[-1], newAddress, boolAddress))
		quadruples.indexQuadruples += 1

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
	# Check if there are any reference parameters
	paramList = functionsDir[p[1]][2]
	i = 0
	while(i < len(paramList)):
		if paramList[i][0]:
			# Add index for REFERENCE_PARAM quadruple to fill later
			quadruples.sPARAMS.append(quadruples.indexQuadruples)

			# Get var address using id
			varID = paramList[i][1]
			varAddress = functionsDir[p[1]][1][varID][1]

			# Generate REFERENCE_PARAM for var
			quadruples.dirQuadruples.append((REFERENCE_PARAM, varAddress, None, None))
			quadruples.indexQuadruples += 1
		i += 1

	# Generate ENDPROC
	quadruples.dirQuadruples.append((ENDPROC, None, None, None))
	quadruples.indexQuadruples += 1
	functionsDir[p[1]][5] = getLocalVarQty()

	while len(quadruples.sERA) != 0:
		# GET ERA index to fill
		tempERA = quadruples.sERA.pop()

		# GET ERA Quadruple
		t = quadruples.dirQuadruples[tempERA[1]]

		# Fill with needed memory from function
		t = t[:2] + (functionsDir[tempERA[0]][5],) + t[3:]
		quadruples.dirQuadruples[tempERA[1]] = t
	resetMemoryIndexes()

def p_declareFunc(p):
	'''declareFunc : '''
	global function_ptr
	function_ptr = p[-1]

	if functionsDir.has_key(function_ptr) == False:
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
		functionAddress = None
		if parseTypeIndex(p[-2]) != 23:
			varType = parseTypeIndex(p[-2])
			# Add cteint 1 for varSize for ID
			varSize = setConstantAddress(INT, 1)
			functionAddress =  getGlobalAddress(varType, varSize)
			globalVarsTypeCounts[varType] += 1
		functionsDir[function_ptr] = [parseTypeIndex(p[-2]), {}, [], quadruples.indexQuadruples, functionAddress, [0,0,0,0]]
	else:
		# Error
		print("Function %s already declared!" %(function_ptr))
		exit(1)

def p_return(p):
	'''return	: RETURN expresion_logica'''
	# Verify type of function
	if functionsDir[function_ptr][0] != VOID:
		# Generate RETURN with value to return and address to return it to
		varType = quadruples.sTypes.pop()
		if varType == functionsDir[function_ptr][0]:
			quadruples.dirQuadruples.append((RETURN, quadruples.sOperands.pop(), None, None))
			quadruples.indexQuadruples += 1
			# Generate ENDPROC
			quadruples.dirQuadruples.append((ENDPROC, None, None, None))
			quadruples.indexQuadruples += 1
		else:
			# Error
			print("Invalid RETURN type: %s with function type: %s! Line: %s" %(varType, functionsDir[function_ptr][0], p.lineno(1)))
			exit(1)
	else:
		# Error
		print("Invalid operation RETURN on VOID Function: %s! Line: %s" %(function_ptr, p.lineno(1)))
		exit(1)

def p_input(p):
	'''input	: INPUT LPAREN input1 RPAREN'''
	global printList

	# Invert list of print parameters if len(list) > 1
	if len(printList) > 1:
		printList.reverse()

	# Type of id to return input to
	varType = quadruples.sTypes[-1]

	# Add cteint 1 for varSize for return var
	varSize = setConstantAddress(INT, 1)

	newValueAddress = getLocalAddress(varType, varSize)

	# Generate Input quadruple [INPUT, vars to print, returnType, returnAddress]
	quadruples.dirQuadruples.append((INPUT, printList, varType, newValueAddress))
	quadruples.indexQuadruples += 1

	# Append input value to sOperands
	quadruples.sOperands.append(newValueAddress)
	quadruples.sTypes.append(varType)

	printList = []

	p[0] = p[1]

def p_input1(p):
	''' input1 : epsilon
				| varcte input2'''
	# Append varcte to print list
	if len(p) > 2:
		printList.append(quadruples.sOperands.pop())
		quadruples.sTypes.pop()

def p_input2(p):
	''' input2 : epsilon
				| PLUS varcte input2'''
	# Append varcte to print list
	if len(p) > 2:
		printList.append(quadruples.sOperands.pop())
		quadruples.sTypes.pop()

def p_llamada(p):
	'''llamada 	: ID LPAREN llamada1 RPAREN'''
	global countParam
	# Pedir memoria para funcion
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
	if functionsDir.has_key(p[1]):
		if functionsDir[p[1]][0] == 23:
			subTypeQty = functionsDir[p[1]][5]

			# Iterates subTypeQty to count how many types are used
			totalTypes = 0
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, None))

			if function_ptr != "main":
				# Save index to fill out ERA when function ends
				quadruples.sERA.append((p[1], quadruples.indexQuadruples))
			quadruples.indexQuadruples += 1

		else:
			# Error
			print("Function %s is not void, must be assigned for return value!" %(p[1]))
			exit(1)
	else:
		# Error
		print("Function %s is not declared!" %(p[1]))
		exit(1)

	# Function parameter list
	paramList = functionsDir[p[1]][2]

	# Verificar que countParam == len(parametros) de la funcion
	if len(paramList) == countParam:
		# Verifica que parametros recibidos sean del tipo que se espera en el mismo orden
		while (countParam > 0):
			varID = paramList[countParam-1][1]
			varType = functionsDir[p[1]][1][varID][0]
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s!" %(p[1], parseType(quadruples.sTypes[-1]), parseType(varType)))
				exit(1)
			else:
				# Get parameter to send
				varAddress = quadruples.sOperands.pop()
				
				# Verify function variable expects reference parameter
				if paramList[countParam-1][0]:
					# Verify parameters by reference are correct
					if type(varAddress) is not list:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference!" %(p[1], varID))
						exit(1)
					elif varAddress[0]:
						# Get Index to fill REFERENCE_PARAM for function
						referencePARAMIndex = quadruples.sPARAMS.pop()
						varAddress = varAddress[1]
						t = quadruples.dirQuadruples[referencePARAMIndex]
						t = t[:3] + (varAddress,)
						quadruples.dirQuadruples[referencePARAMIndex] = t
					else:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference!" %(p[1], varID))
						exit(1)
				elif varAddress[0]:
					# Error
					print("Function: '%s' in parameter '%s' isn't expecting a parameter by reference!" %(p[1], varID))
					exit(1)
				else:
					# remove reference flag and leave only addres in varAddress
					varAddress = varAddress[1]

				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), varAddress, functionsDir[p[1]][1][varID][1]))
				quadruples.indexQuadruples += 1
			countParam -= 1

		# Genera cuadruplo GOSUB
		quadruples.dirQuadruples.append((GOSUB, p[1], None, functionsDir[p[1]][3]))
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d!" %(p[1], len(paramList), countParam))
		exit(1)

	countParam = 0

	p[0] = 'Llamada ' + str(p[1])

def p_llamada1(p):
	'''llamada1 : epsilon
				| llamada5 llamada2'''
	if len(p) > 2:
		global countParam
		countParam += 1

def p_llamada2(p):
	'''llamada2 	: epsilon
					| COMMA llamada5 llamada2'''
	if len(p) > 2:
		global countParam
		countParam += 1

def p_addReferenceFlag(p):
	'''addReferenceFlag : '''
	# Add false flag to variable
	varAddress = quadruples.sOperands.pop()
	# Append variable back to stack with flag to know it's not by reference
	quadruples.sOperands.append([False, varAddress])

def p_llamada3(p):
	'''llamada3 : LPAREN llamada1 RPAREN'''
	global countParam

	# Pedir memoria para funcion
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
	varSize = setConstantAddress(INT, 1)
	newValueAddress = ""
	if functionsDir.has_key(p[-1]):
		if functionsDir[p[-1]][0] != 23:
			subTypeQty = functionsDir[p[-1]][5]

			# Iterates subTypeQty to count how many types are used
			totalTypes = 0
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			newValueAddress = getLocalAddress(functionsDir[p[-1]][0], varSize)
			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, newValueAddress))

			if function_ptr != "main":
				# Save index to fill out ERA when function ends
				quadruples.sERA.append((p[-1], quadruples.indexQuadruples))
			quadruples.indexQuadruples += 1
		else:
			# Error
			print("Function %s is void, it can't be assigned!" %(p[-1]))
			exit(1)
	else:
		# Error
		print("Function %s is not declared!" %(p[-1]))
		exit(1)

	# Function parameter list
	paramList = functionsDir[p[-1]][2]

	# Verificar que countParam == len(parametros) de la funcion
	if len(paramList) == countParam:
		# Verifica que parametros recibidos sean del tipo que se espera en el mismo orden
		while (countParam > 0):
			varID = paramList[countParam-1][1]
			varType = functionsDir[p[-1]][1][varID][0]
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s!" %(p[-1], parseType(quadruples.sTypes[-1]), parseType(varType)))
				exit(1)
			else:
				# Get parameter to send
				varAddress = quadruples.sOperands.pop()

				# Verify function variable expects reference parameter
				if paramList[countParam-1][0]:
					# Verify parameters by reference are correct
					if type(varAddress) is not list:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference!" %(p[-1], varID))
						exit(1)
					elif varAddress[0]:
						# Get Index to fill REFERENCE_PARAM for function
						referencePARAMIndex = quadruples.sPARAMS.pop()
						varAddress = varAddress[1]
						t = quadruples.dirQuadruples[referencePARAMIndex]
						t = t[:3] + (varAddress,)
						quadruples.dirQuadruples[referencePARAMIndex] = t
					else:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference!" %(p[-1], varID))
						exit(1)
				elif varAddress[0]:
					# Error
					print("Function: '%s' in parameter '%s' isn't expecting a parameter by reference!" %(p[-1], varID))
					exit(1)
				else:
					# remove reference flag and leave only addres in varAddress
					varAddress = varAddress[1]
				
				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), varAddress, functionsDir[p[-1]][1][varID][1]))
				quadruples.indexQuadruples += 1
			countParam -= 1

		# Genera cuadruplo GOSUB
		quadruples.dirQuadruples.append((GOSUB, p[-1], None, functionsDir[p[-1]][3]))
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d!" %(p[-1], len(paramList), countParam))
		exit(1)

	countParam = 0

	quadruples.sOperands.append(newValueAddress)
	quadruples.sTypes.append(functionsDir[p[-1]][0])
	p[0] = 'Llamada ' + str(p[-1])

def p_llamada4(p):
	'''llamada4 : varcte3'''
	# Get reference parameter memory address
	varAddress = quadruples.sOperands.pop()

	# Append to stack in list with flag to know it's by reference
	quadruples.sOperands.append([True, varAddress])

def p_llamada5(p):
	'''llamada5 : expresion_logica addReferenceFlag 
				| AMPERSON llamada4'''

def p_main(p):
	'main : MAIN declareMain LCURL main1 estatuto main2 RCURL'
	functionsDir[p[1]][5] = getLocalVarQty()

	subTypeQty = functionsDir[p[1]][5]

	# Iterates subTypeQty to count how many types are used
	totalTypes = 0
	for x in range(0, len(subTypeQty)):
		if subTypeQty[x] > 0:
			totalTypes += 1

	t = quadruples.dirQuadruples[0]
	t = t[:1] + (totalTypes, subTypeQty, functionsDir[p[1]][4],)
	quadruples.dirQuadruples[0] = t

def p_declareMain(p):
	'''declareMain : '''
	global function_ptr
	function_ptr = p[-1]

	# Check Main function is unique
	if functionsDir.has_key(p[-1]) == False:
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
		functionsDir[p[-1]] = ['main', {}, [], quadruples.indexQuadruples, None, [0,0,0,0]]
		t = quadruples.dirQuadruples[1]
		t = t[:3] + (quadruples.indexQuadruples,)
		quadruples.dirQuadruples[1] = t
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
	''' parametros : tipo meteParamTipo parametros1 ID meteParam parametros2'''

def p_parametros1(p):
	'''parametros1 : AMPERSON
				| epsilon'''

	# Update reference flag for last parameter in parameter list
	if p[1] == '&':
		functionsDir[function_ptr][2][-1][0] = True

def p_parametros2(p):
	'''parametros2 : COMMA parametros
				| epsilon'''

def p_meteParamTipo(p):
	'meteParamTipo : '
	# Mete parametro a lista de parametros de la funcion
	functionsDir[function_ptr][2].append([False, parseTypeIndex(p[-1])])

def p_meteParam(p):
	'meteParam : '
	# Check if ID exists
	if globalVars.has_key(p[-1]):
		# ERROR
		print("ID: %s is a global variable, can't be used as a parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
		# ERROR
		print("ID: %s is a duplicate parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	else:
		# All parameters are declared of size 1, vectors will be passed as reference
		varSize = setConstantAddress(INT, 1)

		# Get type from top of parameters list in function -> functionsDir[function_ptr][2][-1]
		varType = functionsDir[function_ptr][2][-1][1]

		# Get address for local variable in function
		varAddress = getLocalAddress(varType, varSize)

		# Declare variable in function [Type, Address, Size]
		functionsDir[function_ptr][1][p[-1]] = [varType, varAddress, varSize]

		# Append parameter ID to parameter list in function
		functionsDir[function_ptr][2][-1][1] = p[-1]
	p[0] = varAddress

def p_print(p):
	'''print : PRINT LPAREN varcte print1 RPAREN'''
	global printList

	# invert list of print parameters if len(list) > 1
	printList.append(quadruples.sOperands.pop())
	quadruples.sTypes.pop()

	printList.reverse()
	quadruples.dirQuadruples.append((PRINT, None, None, printList))
	quadruples.indexQuadruples += 1

	printList = []

	p[0] = p[1]

def p_print1(p):
	''' print1 : epsilon
				| PLUS varcte print1'''
	# Append varcte to print list
	if len(p) > 2:
		printList.append(quadruples.sOperands.pop())
		quadruples.sTypes.pop()

def p_switch(p):
	'switch	 : SWITCH ID meterIDPOper switch1 LCURL switch2 switch3 RCURL'
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
	varSize = setConstantAddress(INT, 1)
	if globalVars.has_key(p[-1]):
		# Add cteint 1 for varSize for ID
		newAddress = getGlobalAddress(globalVars[p[-1]][0], varSize)
		globalVarsTypeCounts[globalVars[p[-1]][0]] += 1
		quadruples.sTypes.append(globalVars[p[-1]][0])
		quadruples.sOperands.append(newAddress)
	elif functionsDir[function_ptr][1].has_key(p[-1]):
		newAddress = getLocalAddress(functionsDir[function_ptr][1][p[-1]][0], varSize)
		quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
		quadruples.sOperands.append(newAddress)
	else:
		# Error
		print("Variable %s isn't declared! Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)

def p_compararConID(p):
	'compararConID : '
	# Checa tipo de varcte
	operandType2 = quadruples.sTypes.pop()
	operand2 = quadruples.sOperands.pop()
	operator = DOUBLE_EQUAL
	operand1 = quadruples.sOperands[-1]
	operandType1 = quadruples.sTypes[-1]

	operationType = quadruples.getResultType(operandType1, operandType2, operator)

	if(operationType == BOOL):
		# Add cteint 1 for varSize for simple IDs
		varSize = setConstantAddress(INT, 1)
		newAddress = getLocalAddress(operationType, varSize)
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

			operationType = quadruples.getResultType(operandType1, operandType2, operator)
			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(operationType, varSize)
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
				| factorAddFakeCover LBRACKET expresion_logica checarExpresion RBRACKET'''
	if len(p) == 2:
		# Check if ID exists
		if globalVars.has_key(p[-1]):
			# Check id is not a vector
			varSize = setConstantAddress(INT, 1)
			if globalVars[p[-1]][2] == varSize:
				varAddress = globalVars[p[-1]][1]
				quadruples.sTypes.append(globalVars[p[-1]][0])
			else:
				# ERROR
				print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)
		elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
			# Check id is not a vector
			varSize = setConstantAddress(INT, 1)
			if functionsDir[function_ptr][1][p[-1]][2] == varSize:
				varAddress = functionsDir[function_ptr][1][p[-1]][1]
				quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
			else:
				# ERROR
				print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)
		else:
			# ERROR
			print("ID: %s not declared at line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		quadruples.sOperands.append(varAddress)
		p[0] = p[-1]
	elif len(p) == 3:
		# Verify function call exists
		if functionsDir.has_key(p[-1]):
			p[0] = quadruples.sOperands[-1]
		else:
			# ERROR
			print("Function: %s is not declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		# Remove fake cover
		quadruples.sOperators.pop()
	else:
		# Verify Vector exists in global Vars
		if globalVars.has_key(p[-1]):
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				quadruples.indexQuadruples += 1

				# Get local variable for addition
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(INT, varSize)

				# Add index to vector base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				quadruples.indexQuadruples += 1

				# Add index address to sOperands
				quadruples.sOperands.append([newValueAddress])
			else:
				# Error
				print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)

			# Add ID type to sTypes
			quadruples.sTypes.append(globalVars[p[-1]][0])
		else:
			# Check if ID exists in local Vars
			if functionsDir[function_ptr][1].has_key(p[-1]):
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[function_ptr][1][p[-1]][2]))
					quadruples.indexQuadruples += 1

					# Get local variable for addition
					varSize = setConstantAddress(INT, 1)
					newValueAddress = getLocalAddress(INT, varSize)

					# Add index to vector base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[function_ptr][1][p[-1]][1], newValueAddress))
					quadruples.indexQuadruples += 1

					# Add index address to sOperands
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

				# Add ID type to sTypes
				quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
			else:
				# Error
				print("Variable %s is not declared! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)

		# Remove fake cover
		quadruples.sOperators.pop()
		p[0] = p[-1]

def p_varcte3(p):
	''' varcte3 : ID varcte4'''
	p[0] = p[2]

def p_varcte4(p):
	''' varcte4 : epsilon
				| factorAddFakeCover LBRACKET expresion_logica checarExpresion RBRACKET'''
	if len(p) == 2:
		# Get Address for constant value 1
		varSize = setConstantAddress(INT, 1)
		
		# Check if ID exists
		if globalVars.has_key(p[-1]):
			# Verify ID is not a vector
			if globalVars[p[-1]][2] == varSize:
				varAddress = globalVars[p[-1]][1]
				quadruples.sTypes.append(globalVars[p[-1]][0])
			else:
				# ERROR
				print("Cannot send a vector as a parameter, must indicate an index of the vector! Line: %s" %(p.lineno(-1)))
				exit(1)

		elif function_ptr != "GLOBAL" and functionsDir[function_ptr][1].has_key(p[-1]):
			if functionsDir[function_ptr][1][p[-1]][2] == varSize:
				varAddress = functionsDir[function_ptr][1][p[-1]][1]
				quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
			else:
				# ERROR
				print("Cannot send a vector as a parameter, must indicate an index of the vector! Line: %s" %(p.lineno(-1)))
				exit(1)
		else:
			# ERROR
			print("ID: %s not declared at line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		quadruples.sOperands.append(varAddress)
		p[0] = p[-1]
	else:
		# Verify Vector exists in global Vars
		if globalVars.has_key(p[-1]):
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				quadruples.indexQuadruples += 1

				# Get local variable for addition
				varSize = setConstantAddress(INT, 1)
				newValueAddress = getLocalAddress(INT, varSize)

				# Add index to vector base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				quadruples.indexQuadruples += 1

				# Add index address to sOperands
				quadruples.sOperands.append([newValueAddress])
			else:
				# Error
				print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)

			# Add ID type to sTypes
			quadruples.sTypes.append(globalVars[p[-1]][0])
		else:
			# Check if ID exists in local Vars
			if functionsDir[function_ptr][1].has_key(p[-1]):
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[function_ptr][1][p[-1]][2]))
					quadruples.indexQuadruples += 1

					# Get local variable for addition
					varSize = setConstantAddress(INT, 1)
					newValueAddress = getLocalAddress(INT, varSize)

					# Add index to vector base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[function_ptr][1][p[-1]][1], newValueAddress))
					quadruples.indexQuadruples += 1

					# Add index address to sOperands
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

				# Add ID type to sTypes
				quadruples.sTypes.append(functionsDir[function_ptr][1][p[-1]][0])
			else:
				# Error
				print("Variable %s is not declared! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)

		# Remove fake cover
		quadruples.sOperators.pop()
		p[0] = p[-1]

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
		p[0] = p[2]
	else:
		newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
		quadruples.sOperands.append(newValueAddress)
		p[0] = p[1]

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
	p[0] = p[1]

def p_varstring1(p):
	''' varstring1 : VARSTRING'''
	quadruples.sTypes.append(STRING)
	# Insert Value to dictionary and add address to Operands
	newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])

	quadruples.sOperands.append(newValueAddress)
	p[0] = p[1]

def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''
	quadruples.sTypes.append(BOOL)
	# Insert Value to dictionary and add address to Operands
	newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
	quadruples.sOperands.append(newValueAddress)
	p[0] = p[1]

def p_checarExpresion(p):
	'''checarExpresion : '''
	# Checa si p[-1] es una CTE_INT

def p_var_declaracion(p):
	'''var_declaracion : tipo var_declaracion1'''

def p_var_declaracion1(p):
	'''var_declaracion1 : ID var_declaracion2'''

def p_var_declaracion2(p):
	'''var_declaracion2 : epsilon
						| LBRACKET cte_int1 RBRACKET'''
	# Declare ID if it doesn't exist
	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)
	if function_ptr == 'GLOBAL':
		if globalVars.has_key(p[-1]):
			# Error
			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)

		# Asign variable type
		varType = parseTypeIndex(p[-2])

		# Asign address to variable size for vector IDs
		if len(p) == 4:
			varSize = quadruples.sOperands.pop()
			quadruples.sTypes.pop()

		# Get address for variable given the type and size
		varAddress = getGlobalAddress(varType, varSize)

		# Add amount of space used for variable in type
		if len(p) == 4:
			globalVarsTypeCounts[varType] += p[2]
		else:
			globalVarsTypeCounts[varType] += 1

		# Add variable to globalVars table
		globalVars[p[-1]] = [varType, varAddress, varSize]
	else:
		if globalVars.has_key(p[-1]):
			# Error
			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		elif functionsDir[function_ptr][1].has_key(p[-1]):
			# Error
			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)

		# Asign variable type
		varType = parseTypeIndex(p[-2])

		# Asign address to variable size for vector IDs
		if len(p) == 4:
			varSize = quadruples.sOperands.pop()
			quadruples.sTypes.pop()

		# Get address for variable given the type and size
		varAddress = getLocalAddress(varType, varSize)

		# Add variable to globalVars table
		functionsDir[function_ptr][1][p[-1]] = [varType, varAddress, varSize]

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
	parser = yacc.yacc(debug=True)
	if p:
		print("Syntax error at token: '%s' with value: '%s' at line: %d" %(p.type, p.value, p.lineno))
		# Discard the token
		parser.errok()
	else:
		print("Syntax error at EOF")
	exit(1)
