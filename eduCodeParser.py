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
functionPtr = "GLOBAL"

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

# ERROR CODE
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

# Function to parse token type value to
# equivalent numeric constant
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

# Function to parse constant type to
# type string value
def parseType(type):
	if type == INT:
		return 'INT'
	elif type == FLOAT:
		return 'FLOAT'
	elif type == BOOL:
		return 'BOOL'
	else:
		return 'STRING'

# Function to parse constant operator to
# type string value
def parseOperator(operator):
	if operator == MULT:
		return 'MULT'
	elif operator == DIVIDE:
		return 'DIVIDE'
	elif operator == PLUS:
		return 'PLUS'
	elif operator == MINUS:
		return 'MINUS'
	elif operator == AND:
		return 'AND'
	elif operator == OR:
		return 'OR'
	elif operator == LESSEQUAL:
		return 'LESSEQUAL'
	elif operator == GREATEREQUAL:
		return 'GREATEREQUAL'
	elif operator == DOUBLE_EQUAL:
		return 'DOUBLE_EQUAL'
	elif operator == DIFF:
		return 'DIFF'
	elif operator == LESS:
		return 'LESS'
	elif operator == GREATER:
		return 'GREATER'

# Function to parse token operator value to
# equivalent numeric constant
def parseOperatorIndex(operator):
	if operator == '*':
		return MULT
	elif operator == '/':
		return DIVIDE
	elif operator == '+':
		return PLUS
	elif operator == 'and':
		return AND
	elif operator == 'or':
		return OR
	elif operator == '<=':
		return LESSEQUAL
	elif operator == '>=':
		return GREATEREQUAL
	elif operator == '==':
		return DOUBLE_EQUAL
	elif operator == '!=':
		return DIFF
	elif operator == '<':
		return LESS
	elif operator == '>':
		return GREATER
	else:
		return MINUS

#########################################
#										#
#		 	Grammar Rules				#
#										#
#########################################

def p_programa(p):
	'programa 	: START gotoMAIN programa1 programa2 main END'
	# Generate quadruple for END OF FILE
	quadruples.dirQuadruples.append((EOF, None, None, None))
	# Move quadruple index by 1
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
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Generate quadruple GOTO MAIN
	quadruples.dirQuadruples.append((GOTO, None, None, None))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

def p_asignacion(p):
	'''asignacion : ID asignacion1 EQUALS asignacion2'''
	# Get values to operate from stacks
	operand2 = quadruples.sOperands.pop()
	operandType2 = quadruples.sTypes.pop()
	operand1 = quadruples.sOperands.pop()
	operandType1 = quadruples.sTypes.pop()
	
	# Compare if operand1 type and operand2 are compatible given the operation
	asignacionType = quadruples.getResultType(operandType1, operandType2, EQUALS)

	# Check if operation is compatible
	if asignacionType != ERROR:
		# Generate quadruple EQUALS to asign value of operand2 to operand1
		quadruples.dirQuadruples.append((EQUALS, operand2, None, operand1))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Type mismatch in assignment to var: %s of type: %s with type %s, cannot assign value! Line: %s" %(p[1], parseType(operandType1), parseType(operandType2), p.lineno(1)))
		exit(1)

def p_asignacion1(p):
	'''asignacion1 : epsilon
				| LBRACKET expresion_logica RBRACKET'''
	# Get address for constant value 1
	varSize = setConstantAddress(INT, 1)

	# Check if ID exists in global Vars
	if globalVars.has_key(p[-1]):
		# If ID is a vector add index address to sOperands
		if len(p) == 4:
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Generate VER quadruple to verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1

				# Get local variable for addition
				newValueAddress = getLocalAddress(INT, varSize)

				# Generate quadruple PLUS_ADDR to add index to vector base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1

				# Add index address to sOperands as indirect address
				quadruples.sOperands.append([newValueAddress])
			else:
				# Error
				print("Cannot access vector variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
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
		if functionsDir[functionPtr][1].has_key(p[-1]):
			# If ID is a vector add index address to sOperands
			if len(p) == 4:
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Generate VER quadruple to verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[functionPtr][1][p[-1]][2]))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Get local variable for addition
					newValueAddress = getLocalAddress(INT, varSize)

					# Generate quadruple PLUS_ADDR to add index to vector base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[functionPtr][1][p[-1]][1], newValueAddress))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Add index address to sOperands as indirect address
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access vector variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)
			else:
				# Check id is not a vector
				if functionsDir[functionPtr][1][p[-1]][2] == varSize:
					# Add ID address to sOperands
					quadruples.sOperands.append(functionsDir[functionPtr][1][p[-1]][1])
				else:
					# ERROR
					print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

			# Add ID type to sTypes
			quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
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
	# Fill out GOTO's for each pending condition using the jump stack
	while(quadruples.sJumps[-1] != '('):
		# Get the index of the quadruple to fill
		gotoIndex = quadruples.sJumps.pop()
		# Save the quadruple in a temp variable
		t = quadruples.dirQuadruples[gotoIndex]
		# Append the current index to the quadruple
		t = t[:3] + (quadruples.indexQuadruples,)
		# Save the new qudruple back in the quadruples directory
		quadruples.dirQuadruples[gotoIndex] = t

	# Remove fake cover
	if quadruples.sJumps[-1] == '(':
		quadruples.sJumps.pop()

def p_addConditionFakeCover(p):
	'addConditionFakeCover 	: '
	# Add fake cover everytime a new condition is found
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
	# Get type of last evaluated variable
	aux = quadruples.sTypes.pop()
	
	# Verify type of condition evaluated is bool
	if aux == BOOL:
		# Generate GOTOF quadruple
		quadruples.dirQuadruples.append((GOTOF, quadruples.sOperands.pop(), None, None))
		# Append current index to jump stack to fill out index to jump to later
		quadruples.sJumps.append(quadruples.indexQuadruples)
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Evaluated expresion is type %s, not a bool! Line: %s" %(parseType(aux), p.lineno(-1)))
		exit(1)

def p_checkPSaltos(p):
	'''checkPSaltos : '''
	# Generate GOTO quadruple
	quadruples.dirQuadruples.append((GOTO, None, None, None))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Fill out GOTO for pending condition using the jump stack
	if (len(quadruples.sJumps) != 0):
		# Get the index of the quadruple to fill
		gotoIndex = quadruples.sJumps.pop()
		# Save the quadruple in a temp variable
		t = quadruples.dirQuadruples[gotoIndex]
		# Append the current index to the quadruple
		t = t[:3] + (quadruples.indexQuadruples,)
		# Save the new qudruple back in the quadruples directory
		quadruples.dirQuadruples[gotoIndex] = t

	# Append current index -1 to jump stack to fill out index to jump to later
	quadruples.sJumps.append(quadruples.indexQuadruples-1)

def p_do_while(p):
	''' do_while : DO metePSaltos bloque WHILE LPAREN expresion_logica RPAREN '''
	# Get type of last evaluated variable
	aux = quadruples.sTypes.pop()

	# Verify type of condition evaluated is bool
	if aux == BOOL:
		# Generate GOTOT quadruple
		quadruples.dirQuadruples.append((GOTOT, quadruples.sOperands.pop(), None, quadruples.sJumps.pop()))
		# Move quadruple index by 1
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
	# Verify operator stack is not empty
	if (len(quadruples.sOperators) != 0):
		# Check if operator is PLUS or MINUS
		if ((quadruples.sOperators[-1] == PLUS) or (quadruples.sOperators[-1] == MINUS)):
			# Get operator, operands and types from stacks
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			# Check if operation is possible given operands' types
			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			# Verify operation is not an ERROR
			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)

				# Get a temporary variable address for operation
				newValueAddress = getLocalAddress(operationType, varSize)

				# Generate quadruple with operator, operands and the temporary variable
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))

				# Append the temporary variable and type to the stacks
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(parseType(operandType1), parseType(operandType2), parseOperator(operator), p.lineno(-1)))
				exit(1)

def p_exp1(p):
	''' exp1 	: PLUS addOperator exp
				| MINUS addOperator exp
				| epsilon'''

def p_addOperator(p):
	'''addOperator : '''
	# Checks the previous operator token
	# to parse it and add it to the stack
	quadruples.sOperators.append(parseOperatorIndex(p[-1]))

def p_expresion(p):
	'expresion 	: exp checkEXPRESIONPOper expresion1'
	p[0] = p[1]

def p_checkEXPRESIONPOper(p):
	'checkEXPRESIONPOper : '
	# Verify operator stack is not empty
	if (len(quadruples.sOperators) != 0):
		# Check if operator is LESS, LESSEQUAL, GREATER,
		# GREATEREQUAL, DOUBLE_EQUAL or DIFF
		if ((quadruples.sOperators[-1] == LESS) or (quadruples.sOperators[-1] == LESSEQUAL) or (quadruples.sOperators[-1] == GREATER) or (quadruples.sOperators[-1] == GREATEREQUAL) or (quadruples.sOperators[-1] == DOUBLE_EQUAL) or (quadruples.sOperators[-1] == DIFF)):
			# Get operator, operands and types from stacks
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			# Check if operation is possible given operands' types
			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			# Verify operation is not an ERROR
			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)

				# Get a temporary variable address for operation
				newValueAddress = getLocalAddress(operationType, varSize)

				# Generate quadruple with operator, operands and the temporary variable
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))

				# Append the temporary variable and type to the stacks
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(parseType(operandType1), parseType(operandType2), parseOperator(operator), p.lineno(-1)))
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
	# Verify operator stack is not empty
	if (len(quadruples.sOperators) != 0):
		# Check if operator is AND or OR
		if ((quadruples.sOperators[-1] == AND) or (quadruples.sOperators[-1] == OR)):
			# Get operator, operands and types from stacks
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			# Check if operation is possible given operands' types
			operationType = quadruples.getResultType(operandType1, operandType2, operator)

			# Verify operation is not an ERROR
			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)

				# Get a temporary variable address for operation
				newValueAddress = getLocalAddress(operationType, varSize)

				# Generate quadruple with operator, operands and the temporary variable
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))

				# Append the temporary variable and type to the stacks
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(parseType(operandType1), parseType(operandType2), parseOperator(operator), p.lineno(-1)))
				exit(1)

def p_expresion_logica1(p):
	'''expresion_logica1 	: AND addOperator expresion_logica
					| epsilon
					| OR addOperator expresion_logica'''

def p_factor(p):
	''' factor	: LPAREN factorAddFakeCover expresion_logica RPAREN
				| factor1'''
	if len(p) == 5:
		# Remove fake cover from operators
		quadruples.sOperators.pop()
	p[0] = p[1]

def p_factorAddFakeCover(p):
	'factorAddFakeCover : '
	# Add a fake cover to maintain order of operations
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
				# Multiply value by -1
				p[0] = p[2] * -1
			else:
				p[0] = p[2]
	else:
		p[0] = p[1]

def p_from(p):
	'from : FROM cteFrom creaVarTemp TO cteFrom crearComparacion BY LPAREN from1 cteFrom RPAREN bloque'
	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)

	# Get memory address for cte used to operate
	# on the from index
	newAddress = setConstantAddress(INT,p[10])

	# Get a temporary variable address for operation
	tempAddress = getLocalAddress(INT,varSize)

	# Generate quadruple corresponding to the operator
	# to manipulate the from index
	quadruples.dirQuadruples.append((parseOperatorIndex(p[9]),fromTempStack[-1],newAddress,tempAddress))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Generate quadruple to reassign new value to the index
	quadruples.dirQuadruples.append((EQUALS,tempAddress, None, fromTempStack[-1]))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Get the index for the false jump in the jump stack
	gotoFIndex = quadruples.sJumps.pop()

	# Generate GOTO for the quadruple index in the jump stack
	quadruples.dirQuadruples.append((GOTO, None, None, quadruples.sJumps.pop()))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Get the gotof quadruple with the gotoFIndex and
	# save it to a temporary variable
	t = quadruples.dirQuadruples[gotoFIndex]

	# Append the current index to the end of the quadruple
	t = t[:3] + (quadruples.indexQuadruples,)

	# Replace the old quadruple with the new one that includes the jump 
	quadruples.dirQuadruples[gotoFIndex] = t

	# Pop the operand in fromTempStack
	fromTempStack.pop()

def p_from1(p):
	'''from1	: PLUS
			| TIMES
			| DIVIDE
			| MINUS'''
	p[0] = p[1]

def p_creaVarTemp(p):
	'creaVarTemp : '
	# Add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])

	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)

	# Get temporal address to create copy of the index value
	tempAddress = getLocalAddress(INT,varSize)

	# Generate EQUALS quadruple to assign the index to the temporary address
	quadruples.dirQuadruples.append((EQUALS,newAddress,None,tempAddress))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1
	
	# Add the index to the tempStack
	fromTempStack.append(tempAddress)

	# Add the index to the operands stack
	quadruples.sOperands.append(p[-1])

def p_crearComparacion(p):
	'crearComparacion : '
	# Add constant to memory
	newAddress =  setConstantAddress(INT,p[-1])

	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)

	# Gets bool memory address
	boolAddress = getLocalAddress(BOOL,varSize)

	# Adds current index to jump stack to fill GOTO later
	quadruples.sJumps.append(quadruples.indexQuadruples)

	# Checks values given to generate corresponding comparison
	if quadruples.sOperands.pop() >= p[-1]:
		# Generates quadruple >= using index and second value
		quadruples.dirQuadruples.append((GREATEREQUAL, fromTempStack[-1], newAddress, boolAddress))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1

	else:
		# Generates quadruple <= using index and second value
		quadruples.dirQuadruples.append((LESSEQUAL, fromTempStack[-1], newAddress, boolAddress))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1

	# Generates GOTOF quadruple
	quadruples.dirQuadruples.append((GOTOF, boolAddress, None, None))

	# Adds current index to jump stack to fill out GOTOF jump later
	quadruples.sJumps.append(quadruples.indexQuadruples)
	# Move quadruple index by 1
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
	
	# Iterates through the parameter list
	i = 0
	while(i < len(paramList)):
		# Checks parameter flag to check if it's by reference
		if paramList[i][0]:
			# Add index for REFERENCE_PARAM quadruple to fill later
			quadruples.sPARAMS.append(quadruples.indexQuadruples)

			# Get var address using id
			varID = paramList[i][1]
			varAddress = functionsDir[p[1]][1][varID][1]

			# Generate REFERENCE_PARAM for var
			quadruples.dirQuadruples.append((REFERENCE_PARAM, varAddress, None, None))
			# Move quadruple index by 1
			quadruples.indexQuadruples += 1
		i += 1

	# Generate ENDPROC quadruple
	quadruples.dirQuadruples.append((ENDPROC, None, None, None))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Uses getLocalVarQty to count how many variables
	# per type the function used and add it to its table
	functionsDir[p[1]][5] = getLocalVarQty()

	# Iterates through the indexes with ERA quadruples
	while len(quadruples.sERA) != 0:
		# GET ERA index to fill
		tempERA = quadruples.sERA.pop()

		# GET ERA Quadruple in temporary variable
		t = quadruples.dirQuadruples[tempERA[1]]

		# Fill with needed memory from function
		t = t[:2] + (functionsDir[tempERA[0]][5],) + t[3:]

		# Replace old quadruple with new one
		quadruples.dirQuadruples[tempERA[1]] = t

	# Resets the local memory indexes for next function
	resetMemoryIndexes()

def p_declareFunc(p):
	'''declareFunc : '''
	global functionPtr
	# Assign function ID as current function pointer
	functionPtr = p[-1]

	# Verifies function doesn't exist already
	if functionsDir.has_key(functionPtr) == False:
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
		# Initializes function address
		functionAddress = None

		# Checks if fucntion is different than type void
		if parseTypeIndex(p[-2]) != 23:
			# Parses the function type
			varType = parseTypeIndex(p[-2])

			# Add cteint 1 for varSize for ID
			varSize = setConstantAddress(INT, 1)

			# Gets global address for function and moves index for global vars
			functionAddress = getGlobalAddress(varType, varSize)
			globalVarsTypeCounts[varType] += 1

		# Adds function data to table
		functionsDir[functionPtr] = [parseTypeIndex(p[-2]), {}, [], quadruples.indexQuadruples, functionAddress, [0,0,0,0]]
	else:
		# Error
		print("Function %s already declared! Line: %s" %(functionPtr, p.lineno(-1)))
		exit(1)

def p_return(p):
	'''return	: RETURN expresion_logica'''
	# Verify type of function is not void
	if functionsDir[functionPtr][0] != VOID:
		# Get return variable type from stack
		varType = quadruples.sTypes.pop()

		# Verify return variable type corresponds to the function's type
		if varType == functionsDir[functionPtr][0]:
			# Generate RETURN with value to return and address to return it to
			quadruples.dirQuadruples.append((RETURN, quadruples.sOperands.pop(), None, None))
			# Move quadruple index by 1
			quadruples.indexQuadruples += 1

			# Generate ENDPROC quadruple
			quadruples.dirQuadruples.append((ENDPROC, None, None, None))
			# Move quadruple index by 1
			quadruples.indexQuadruples += 1
		else:
			# Error
			print("Invalid RETURN type: %s with function type: %s! Line: %s" %(parseType(varType), parseType(functionsDir[functionPtr][0]), p.lineno(1)))
			exit(1)
	else:
		# Error
		print("Invalid operation RETURN on VOID Function: %s! Line: %s" %(functionPtr, p.lineno(1)))
		exit(1)

def p_input(p):
	'''input	: INPUT LPAREN input1 RPAREN'''
	global printList

	# Invert list of print parameters if len(list) > 1
	if len(printList) > 1:
		printList.reverse()

	# Get type of id to return input to
	varType = quadruples.sTypes[-1]

	# Add cteint 1 for varSize for return var
	varSize = setConstantAddress(INT, 1)

	# Get local address for variable that will get the input value
	newValueAddress = getLocalAddress(varType, varSize)

	# Generate Input quadruple [INPUT, vars to print, returnType, returnAddress]
	quadruples.dirQuadruples.append((INPUT, printList, varType, newValueAddress))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Append input value and type to stacks
	quadruples.sOperands.append(newValueAddress)
	quadruples.sTypes.append(varType)

	# Reset print list
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

	# Function structure
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]

	# Verify function exists
	if functionsDir.has_key(p[1]):
		# Verify function is of type void
		if functionsDir[p[1]][0] == 23:
			# Get total variables per type used in function
			subTypeQty = functionsDir[p[1]][5]

			# Iterates subTypeQty to count how many types are used
			totalTypes = 0
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			# Generate ERA quadruple
			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, None))

			# Checks if function is not main
			if functionPtr != "main":
				# Save index to fill out ERA when function ends
				quadruples.sERA.append((p[1], quadruples.indexQuadruples))
			# Move quadruple index by 1
			quadruples.indexQuadruples += 1

		else:
			# Error
			print("Function %s is void, it can't be assigned! Line: %s" %(p[1], p.lineno(1)))
			exit(1)
	else:
		# Error
		print("Function %s is not declared! Line: %s" %(p[1], p.lineno(1)))
		exit(1)

	# Function parameter list
	paramList = functionsDir[p[1]][2]

	# Verify number of parameters in call match
	# number of parameter in function
	if len(paramList) == countParam:
		# Verify parameters sent match type of parameters expected in order
		while (countParam > 0):
			# Get id and type of parameter from function
			varID = paramList[countParam-1][1]
			varType = functionsDir[p[1]][1][varID][0]

			# Verify function parameter type matches call parameter type
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s! Line: %s" %(p[1], parseType(quadruples.sTypes[-1]), parseType(varType)), p.lineno(1))
				exit(1)
			else:
				# Get parameter to send
				varAddress = quadruples.sOperands.pop()
				
				# Verify function variable expects reference parameter
				if paramList[countParam-1][0]:
					# Verify parameters by reference are correct
					if type(varAddress) is not list:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference! Line: %s" %(p[1], varID, p.lineno(1)))
						exit(1)
					elif varAddress[0]:
						# Get index to fill REFERENCE_PARAM for function
						referencePARAMIndex = quadruples.sPARAMS.pop()
						
						# Remove reference flag and leave only addres in varAddress
						varAddress = varAddress[1]
						
						# Get quadurple with index and save it to a temporary variable
						t = quadruples.dirQuadruples[referencePARAMIndex]

						# Append address to quadruple
						t = t[:3] + (varAddress,)

						# Replace old quadruple with new one
						quadruples.dirQuadruples[referencePARAMIndex] = t
					else:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference! Line: %s" %(p[1], varID, p.lineno(1)))
						exit(1)
				elif varAddress[0]:
					# Error
					print("Function: '%s' in parameter '%s' isn't expecting a parameter by reference! Line: %s" %(p[1], varID, p.lineno(1)))
					exit(1)
				else:
					# Remove reference flag and leave only addres in varAddress
					varAddress = varAddress[1]

				# Generate PARAM quadruple
				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), varAddress, functionsDir[p[1]][1][varID][1]))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			# Move index to next parameter in list
			countParam -= 1

		# Generate quadruple GOSUB
		quadruples.dirQuadruples.append((GOSUB, p[1], None, functionsDir[p[1]][3]))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d! Line: %s" %(p[1], len(paramList), countParam, p.lineno(1)))
		exit(1)

	# Reset count for parameters
	countParam = 0

	p[0] = p[1]

def p_llamada1(p):
	'''llamada1 : epsilon
				| llamada5 llamada2'''
	if len(p) > 2:
		# Found parameter add to count
		global countParam
		countParam += 1

def p_llamada2(p):
	'''llamada2 	: epsilon
					| COMMA llamada5 llamada2'''
	if len(p) > 2:
		# Found parameter add to count
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

	# Function structure
	# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
	
	# Get address for constant value 1
	varSize = setConstantAddress(INT, 1)

	# Initialize new value address for later use
	newValueAddress = ""

	# Verify function exists
	if functionsDir.has_key(p[-1]):
		# Verify function is not of type void
		if functionsDir[p[-1]][0] != 23:
			# Get total variables per type used in function
			subTypeQty = functionsDir[p[-1]][5]

			# Iterates subTypeQty to count how many types are used
			totalTypes = 0
			for x in range(0, len(subTypeQty)):
				if subTypeQty[x] > 0:
					totalTypes += 1

			# Get new address for return value
			newValueAddress = getLocalAddress(functionsDir[p[-1]][0], varSize)
			
			# Generate ERA quadruple
			quadruples.dirQuadruples.append((ERA, totalTypes, subTypeQty, newValueAddress))

			# Checks if function is not main
			if functionPtr != "main":
				# Save index to fill out ERA when function ends
				quadruples.sERA.append((p[-1], quadruples.indexQuadruples))
			# Move quadruple index by 1
			quadruples.indexQuadruples += 1
		else:
			# Error
			print("Function %s is not void, must be assigned for return value! Line: %s" %(p[-1], p.lineno(1)))
			exit(1)
	else:
		# Error
		print("Function %s is not declared! Line: %s" %(p[-1], p.lineno(1)))
		exit(1)

	# Function parameter list
	paramList = functionsDir[p[-1]][2]

	# Verify number of parameters in call match
	# number of parameter in function
	if len(paramList) == countParam:
		# Verify parameters sent match type of parameters expected in order
		while (countParam > 0):
			# Get id and type of parameter from function
			varID = paramList[countParam-1][1]
			varType = functionsDir[p[-1]][1][varID][0]

			# Verify function parameter type matches call parameter type
			if (varType != quadruples.sTypes[-1]):
				# Error
				print("Function: %s parameter %s type mismatch, expected %s! Line: %s" %(p[-1], parseType(quadruples.sTypes[-1]), parseType(varType), p.lineno(1)))
				exit(1)
			else:
				# Get parameter to send
				varAddress = quadruples.sOperands.pop()

				# Verify function variable expects reference parameter
				if paramList[countParam-1][0]:
					# Verify parameters by reference are correct
					if type(varAddress) is not list:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference! Line: %s" %(p[-1], varID, p.lineno(1)))
						exit(1)
					elif varAddress[0]:
						# Get index to fill REFERENCE_PARAM for function
						referencePARAMIndex = quadruples.sPARAMS.pop()
						
						# Remove reference flag and leave only addres in varAddress
						varAddress = varAddress[1]
						
						# Get quadurple with index and save it to a temporary variable
						t = quadruples.dirQuadruples[referencePARAMIndex]

						# Append address to quadruple
						t = t[:3] + (varAddress,)

						# Replace old quadruple with new one
						quadruples.dirQuadruples[referencePARAMIndex] = t
					else:
						# Error
						print("Function: '%s' in parameter: '%s' expected a parameter by reference! Line: %s" %(p[-1], varID, p.lineno(1)))
						exit(1)
				elif varAddress[0]:
					# Error
					print("Function: '%s' in parameter '%s' isn't expecting a parameter by reference! Line: %s" %(p[-1], varID, p.lineno(1)))
					exit(1)
				else:
					# Remove reference flag and leave only addres in varAddress
					varAddress = varAddress[1]
				
				# Generate PARAM quadruple
				quadruples.dirQuadruples.append((PARAM, quadruples.sTypes.pop(), varAddress, functionsDir[p[-1]][1][varID][1]))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			# Move index to next parameter in list
			countParam -= 1

		# Generate quadruple GOSUB
		quadruples.dirQuadruples.append((GOSUB, p[-1], None, functionsDir[p[-1]][3]))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1
	else:
		# Error
		print("Function: %s expected %d parameter(s), recieved %d! Line: %s" %(p[-1], len(paramList), countParam, p.lineno(1)))
		exit(1)

	# Reset count for parameters
	countParam = 0

	# Append variable and type to return in stacks
	quadruples.sOperands.append(newValueAddress)
	quadruples.sTypes.append(functionsDir[p[-1]][0])
	p[0] = p[-1]

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
	# Uses getLocalVarQty to count how many variables
	# per type the function used and add it to its table
	functionsDir[p[1]][5] = getLocalVarQty()

	# Get total variables per type used in function
	subTypeQty = functionsDir[p[1]][5]

	# Iterates subTypeQty to count how many types are used
	totalTypes = 0
	for x in range(0, len(subTypeQty)):
		if subTypeQty[x] > 0:
			totalTypes += 1

	# GET ERA Quadruple for main
	t = quadruples.dirQuadruples[0]

	# Fill with needed memory from function
	t = t[:1] + (totalTypes, subTypeQty, functionsDir[p[1]][4],)

	# Replace old quadruple with new one
	quadruples.dirQuadruples[0] = t

def p_declareMain(p):
	'''declareMain : '''
	global functionPtr

	# Set function pointer to MAIN
	functionPtr = p[-1]

	# Check Main function is unique
	if functionsDir.has_key(p[-1]) == False:
		# Initialize Main function table with data
		# [Tipo, DictVar, ListaParam, indexCuadruplo, FunctionAddress, SubTypeQyt]
		functionsDir[p[-1]] = ['main', {}, [], quadruples.indexQuadruples, None, [0,0,0,0]]

		# Get GOTO quadruple for Main
		t = quadruples.dirQuadruples[1]

		# Fill with current index
		t = t[:3] + (quadruples.indexQuadruples,)

		# Replace old quadruple with new one
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
		functionsDir[functionPtr][2][-1][0] = True

def p_parametros2(p):
	'''parametros2 : COMMA parametros
				| epsilon'''

def p_meteParamTipo(p):
	'meteParamTipo : '
	# Append parameter to function's parameter list
	functionsDir[functionPtr][2].append([False, parseTypeIndex(p[-1])])

def p_meteParam(p):
	'meteParam : '
	# Check if ID exists
	if globalVars.has_key(p[-1]):
		# ERROR
		print("ID: %s is a global variable, can't be used as a parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	elif functionPtr != "GLOBAL" and functionsDir[functionPtr][1].has_key(p[-1]):
		# ERROR
		print("ID: %s is a duplicate parameter. Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)
	else:
		# All parameters are declared of size 1
		varSize = setConstantAddress(INT, 1)

		# Get type from top of parameters list in function -> functionsDir[functionPtr][2][-1]
		varType = functionsDir[functionPtr][2][-1][1]

		# Get address for local variable in function
		varAddress = getLocalAddress(varType, varSize)

		# Declare variable in function [Type, Address, Size]
		functionsDir[functionPtr][1][p[-1]] = [varType, varAddress, varSize]

		# Append parameter ID to parameter list in function
		functionsDir[functionPtr][2][-1][1] = p[-1]
	p[0] = varAddress

def p_print(p):
	'''print : PRINT LPAREN varcte print1 RPAREN'''
	global printList

	# Add previous variable to print list
	printList.append(quadruples.sOperands.pop())
	quadruples.sTypes.pop()

	# Reverse print list
	printList.reverse()

	# Generate PRINT quadruple
	quadruples.dirQuadruples.append((PRINT, None, None, printList))
	# Move quadruple index by 1
	quadruples.indexQuadruples += 1

	# Reset print list to empty
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
	'switch	 : SWITCH addConditionFakeCover ID meterIDPOper switch1 LCURL switch2 switch3 RCURL'
	# Pop additional variable from switch
	quadruples.sOperands.pop()
	quadruples.sTypes.pop()

	# Fill out GOTO's for each pending condition using the jump stack
	while(quadruples.sJumps[-1] != '('):
		# Get the index of the quadruple to fill
		gotoIndex = quadruples.sJumps.pop()
		# Save the quadruple in a temp variable
		t = quadruples.dirQuadruples[gotoIndex]
		# Append the current index to the quadruple
		t = t[:3] + (quadruples.indexQuadruples,)
		# Save the new qudruple back in the quadruples directory
		quadruples.dirQuadruples[gotoIndex] = t

	# Remove fake cover
	if quadruples.sJumps[-1] == '(':
		quadruples.sJumps.pop()

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
	# Get address for constant value 1
	varSize = setConstantAddress(INT, 1)

	# Check if ID exists in global vars
	if globalVars.has_key(p[-1]):
		# Get address for ID to use in comparisons
		newAddress = getGlobalAddress(globalVars[p[-1]][0], varSize)
		globalVarsTypeCounts[globalVars[p[-1]][0]] += 1

		# Add variable to stacks
		quadruples.sTypes.append(globalVars[p[-1]][0])
		quadruples.sOperands.append(newAddress)
	elif functionsDir[functionPtr][1].has_key(p[-1]):
		# Check if ID exists in function memory
		# Get address for ID to use in comparisons
		newAddress = getLocalAddress(functionsDir[functionPtr][1][p[-1]][0], varSize)

		# Add variable to stacks
		quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
		quadruples.sOperands.append(newAddress)
	else:
		# Error
		print("Variable %s isn't declared! Line: %s" %(p[-1], p.lineno(-1)))
		exit(1)

def p_compararConID(p):
	'compararConID : '
	# Get operands and types from stack
	operandType2 = quadruples.sTypes.pop()
	operand2 = quadruples.sOperands.pop()
	operator = DOUBLE_EQUAL
	operand1 = quadruples.sOperands[-1]
	operandType1 = quadruples.sTypes[-1]

	# Verify operation DOUBLE_EQUAL is valid given operands' types
	operationType = quadruples.getResultType(operandType1, operandType2, operator)

	# Check if operatoin is valid
	if(operationType == BOOL):
		# Add cteint 1 for varSize for simple IDs
		varSize = setConstantAddress(INT, 1)

		# Get address for comparison result
		newAddress = getLocalAddress(operationType, varSize)

		# Generate Quadruple for DOUBLE_EQUALS
		quadruples.dirQuadruples.append((operator, operand1, operand2, newAddress))

		# Appends variable result to stacks
		quadruples.sOperands.append(newAddress)
		quadruples.sTypes.append(operationType)
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1

	else:
		print("Type mismatch between operand type: %s and %s while checking if they were the same! Line: %s" %(parseType(operandType1), parseType(operandType2), parseOperator(operator), p.lineno(-1)))
		exit(1)

def p_termino(p):
	'termino 	: factor checkTERMPOper termino1'
	p[0] = p[1]

def p_checkTERMPOper(p):
	'checkTERMPOper : '
	# Verify operator stack is not empty
	if (len(quadruples.sOperators) != 0):
		# Check if operator is MULT or DIVIDE
		if ((quadruples.sOperators[-1] == MULT) or (quadruples.sOperators[-1] == DIVIDE)):
			# Get operator, operands and types from stacks
			operator = quadruples.sOperators.pop()
			operand2 = quadruples.sOperands.pop()
			operand1 = quadruples.sOperands.pop()
			operandType2 = quadruples.sTypes.pop()
			operandType1 = quadruples.sTypes.pop()

			# Check if operation is possible given operands' types
			operationType = quadruples.getResultType(operandType1, operandType2, operator)
			
			# Verify operation is not an ERROR
			if(operationType != ERROR):
				# Add cteint 1 for varSize for simple IDs
				varSize = setConstantAddress(INT, 1)

				# Get a temporary variable address for operation
				newValueAddress = getLocalAddress(operationType, varSize)
				
				# Generate quadruple with operator, operands and the temporary variable
				quadruples.dirQuadruples.append((operator, operand1, operand2, newValueAddress))
				
				# Append the temporary variable and type to the stacks
				quadruples.sOperands.append(newValueAddress)
				quadruples.sTypes.append(operationType)
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1
			else:
				print("Type mismatch between operand type: %s and %s while trying to %s at line: %d" %(parseType(operandType1), parseType(operandType2), parseOperator(operator), p.lineno(-1)))
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
				| factorAddFakeCover LBRACKET expresion_logica RBRACKET'''
	# Get local variable for addition
	varSize = setConstantAddress(INT, 1)

	# Case for ID
	if len(p) == 2:
		# Check if ID exists
		if globalVars.has_key(p[-1]):
			# Get address of constant 1

			# Check id is not a vector
			if globalVars[p[-1]][2] == varSize:
				# Get ID address and type
				varAddress = globalVars[p[-1]][1]
				quadruples.sTypes.append(globalVars[p[-1]][0])
			else:
				# ERROR
				print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)
		elif functionPtr != "GLOBAL" and functionsDir[functionPtr][1].has_key(p[-1]):
			# Check id is not a vector
			if functionsDir[functionPtr][1][p[-1]][2] == varSize:
				# Get ID address and type
				varAddress = functionsDir[functionPtr][1][p[-1]][1]
				quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
			else:
				# ERROR
				print("ID: %s is a vector must specify index! Line: %s" %(p[-1], p.lineno(-1)))
				exit(1)
		else:
			# ERROR
			print("ID: %s not declared at line: %s" %(p[-1], p.lineno(-1)))
			exit(1)

		# Add variable address to stack
		quadruples.sOperands.append(varAddress)
		
		p[0] = p[-1]
	
	# Case for Function call
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
		p[0] = p[-1]

	# Case for vectors
	else:
		# Verify Vector exists in global Vars
		if globalVars.has_key(p[-1]):
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Generate quadruple VER to verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1

				# Get memory address for temporary variable
				newValueAddress = getLocalAddress(INT, varSize)

				# Generate quadruple PLUS_ADDR to add index to vector
				# base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				# Move quadruple index by 1
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
			if functionsDir[functionPtr][1].has_key(p[-1]):
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Generate quadruple VER to verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[functionPtr][1][p[-1]][2]))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Get memory address for temporary variable
					newValueAddress = getLocalAddress(INT, varSize)

					# Generate quadruple PLUS_ADDR to add index to vector
					# base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[functionPtr][1][p[-1]][1], newValueAddress))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Add index address to sOperands
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

				# Add ID type to sTypes
				quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
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
				| factorAddFakeCover LBRACKET expresion_logica RBRACKET'''
	# Get Address for constant value 1
	varSize = setConstantAddress(INT, 1)

	if len(p) == 2:
		# Check if ID exists
		if globalVars.has_key(p[-1]):
			# Verify ID is not a vector
			if globalVars[p[-1]][2] == varSize:
				# Get variable address and type
				varAddress = globalVars[p[-1]][1]
				quadruples.sTypes.append(globalVars[p[-1]][0])
			else:
				# ERROR
				print("Cannot send a vector as a parameter, must indicate an index of the vector! Line: %s" %(p.lineno(-1)))
				exit(1)

		elif functionPtr != "GLOBAL" and functionsDir[functionPtr][1].has_key(p[-1]):
			# Verify ID is not a vector
			if functionsDir[functionPtr][1][p[-1]][2] == varSize:
				# Get variable address and type
				varAddress = functionsDir[functionPtr][1][p[-1]][1]
				quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
			else:
				# ERROR
				print("Cannot send a vector as a parameter, must indicate an index of the vector! Line: %s" %(p.lineno(-1)))
				exit(1)
		else:
			# ERROR
			print("ID: %s not declared at line: %s" %(p[-1], p.lineno(-1)))
			exit(1)

		# Add variable to sOperands
		quadruples.sOperands.append(varAddress)
		p[0] = p[-1]
	else:
		# Verify Vector exists in global Vars
		if globalVars.has_key(p[-1]):
			# Check if expresion_logica type is INT
			if quadruples.sTypes.pop() == INT:
				# Generate quadruple VER to verify index is within vector size
				quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, globalVars[p[-1]][2]))
				# Move quadruple index by 1
				quadruples.indexQuadruples += 1

				# Get local variable for addition
				newValueAddress = getLocalAddress(INT, varSize)

				# Generate quadruple PLUS_ADDR to add index to vector
				# base address to get index address
				quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), globalVars[p[-1]][1], newValueAddress))
				# Move quadruple index by 1
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
			if functionsDir[functionPtr][1].has_key(p[-1]):
				# Check if expresion_logica type is INT
				if quadruples.sTypes.pop() == INT:
					# Generate quadruple VER to verify index is within vector size
					quadruples.dirQuadruples.append((VER, quadruples.sOperands[-1], None, functionsDir[functionPtr][1][p[-1]][2]))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Get memory address for temporary variable
					newValueAddress = getLocalAddress(INT, varSize)

					# Generate quadruple PLUS_ADDR to add index to vector
					# base address to get index address
					quadruples.dirQuadruples.append((PLUS_ADDR, quadruples.sOperands.pop(), functionsDir[functionPtr][1][p[-1]][1], newValueAddress))
					# Move quadruple index by 1
					quadruples.indexQuadruples += 1

					# Add index address to sOperands
					quadruples.sOperands.append([newValueAddress])
				else:
					# Error
					print("Cannot access variable %s with index that's not an INT! Line: %s" %(p[-1], p.lineno(-1)))
					exit(1)

				# Add ID type to sTypes
				quadruples.sTypes.append(functionsDir[functionPtr][1][p[-1]][0])
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
	# Add type INT to sTypes
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
	# Add type FLOAT to sTypes
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
	# Add type STRING to sTypes
	quadruples.sTypes.append(STRING)

	# Insert Value to dictionary and add address to Operands
	newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
	quadruples.sOperands.append(newValueAddress)

	p[0] = p[1]

def p_cte_bool(p):
	''' cte_bool : TRUE
				 | FALSE'''
	# Add type BOOL to sTypes
	quadruples.sTypes.append(BOOL)

	# Insert Value to dictionary and add address to Operands
	newValueAddress = setConstantAddress(quadruples.sTypes[-1], p[1])
	quadruples.sOperands.append(newValueAddress)

	p[0] = p[1]

def p_var_declaracion(p):
	'''var_declaracion : tipo var_declaracion1'''

def p_var_declaracion1(p):
	'''var_declaracion1 : ID var_declaracion2'''

def p_var_declaracion2(p):
	'''var_declaracion2 : epsilon
						| LBRACKET cte_int1 RBRACKET'''
	# Add cteint 1 for varSize for simple IDs
	varSize = setConstantAddress(INT, 1)


	if functionPtr == 'GLOBAL':
		# Checks if variable already exists
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
		# Checks if variable already exists
		if globalVars.has_key(p[-1]):
			# Error
			print("Variable %s already declared! Line: %s" %(p[-1], p.lineno(-1)))
			exit(1)
		elif functionsDir[functionPtr][1].has_key(p[-1]):
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
		functionsDir[functionPtr][1][p[-1]] = [varType, varAddress, varSize]

def p_while(p):
	'while : WHILE metePSaltos LPAREN expresion_logica RPAREN checkEvaluacionLogica bloque'
	# Fill out GOTOF for pending condition using the jump stack
	if (len(quadruples.sJumps) != 0):
		# Get the index of the quadruple to fill
		gotoFIndex = quadruples.sJumps.pop()
		
		# Generate GOTO quadruple
		quadruples.dirQuadruples.append((GOTO, None, None, quadruples.sJumps.pop()))
		# Move quadruple index by 1
		quadruples.indexQuadruples += 1

		# Save the quadruple in a temp variable
		t = quadruples.dirQuadruples[gotoFIndex]

		# Append the current index to the quadruple
		t = t[:3] + (quadruples.indexQuadruples,)

		# Save the new qudruple back in the quadruples directory
		quadruples.dirQuadruples[gotoFIndex] = t

def p_metePSaltos(p):
	'metePSaltos :'
	# Add current index to jump stack
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
