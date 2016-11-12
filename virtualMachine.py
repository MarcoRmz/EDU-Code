#########################################################
#                                                       #
#   virtualMachine.py                                   #
#                                                       #
#   Virtual Machine                                     #
#                                                       #
#   Marco Ramirez       A01191344                       #
#   Andres Gutierrez    A01191581                       #
#                                                       #
#########################################################

from memoryHandler import *
from quadruples import *
from EDUCode import *

executionStack = []

def startMachine():
	#Count variable for quadruples
	i = 0

    #While the quadruple holds no EOF operation
	while(quadruples.dirQuadruples[i][0] != 99):
		print "index %d" % i
    	#conditions to determine actions on quadruples
        #case for PLUS (+)
		if(quadruples.dirQuadruples[i][0] == 0):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply sum operation to operands
			result = operand1 + operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for MINUS (-)
		elif(quadruples.dirQuadruples[i][0] == 1):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply substraction operation to operands
			result = operand1 - operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for MULT (*)
		elif(quadruples.dirQuadruples[i][0] == 2):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply multiplication operation to operands
			result = operand1 * operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for DIVIDE (/)
		elif(quadruples.dirQuadruples[i][0] == 3):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply divide operation to operands
			result = operand1 / operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for AND
		elif(quadruples.dirQuadruples[i][0] == 4):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply and operation to operands
			result = operand1 and operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)

            #case for OR
		elif(quadruples.dirQuadruples[i][0] == 5):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply or operation to operands
			result = operand1 or operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for LESS than (<)
		elif(quadruples.dirQuadruples[i][0] == 6):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply less than to operands
			result = operand1 < operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for  GREATER than (>)
		elif(quadruples.dirQuadruples[i][0] == 7):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply greater than to operands
			result = operand1 > operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for LESS THAN OR EQUALS (<=)
		elif(quadruples.dirQuadruples[i][0] == 8):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			##apply less than equals to operands
			result = operand1 <= operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for GREATER THAN OR EQUALS (>=)
		elif(quadruples.dirQuadruples[i][0] == 9):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply greater than equals to operands
			result = operand1 >= operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for DOUBLE EQUALS (==)
		elif(quadruples.dirQuadruples[i][0] == 10):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply double equals to operands
			result = operand1 == operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for DIFFERENT (!=)
		elif(quadruples.dirQuadruples[i][0] == 11):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			operand2 = getValue(quadruples.dirQuadruples[i][2])

			#apply not equals to operands
			result = operand1 != operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


            #case for EQUALS (=)
		elif(quadruples.dirQuadruples[i][0] == 12):
			#get operands from the memory
			operand1 = getValue(quadruples.dirQuadruples[i][1])
			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],operand1)


            #case for GOTO
		elif(quadruples.dirQuadruples[i][0] == 13):
			#obtain the index of the quadruple and jump to it
			i = quadruples.dirQuadruples[i][3] - 1

            #case for GOTOF
		elif(quadruples.dirQuadruples[i][0] == 14):
			#if the temporal is false jump to the specified quadruple
			if(quadruples.dirQuadruples[i][1] == False):
				i = quadruples.dirQuadruples[i][3] - 1

            #case for GOTOT
		elif(quadruples.dirQuadruples[i][0] == 15):
			#if the temporal holds a True jump to the specified quadruple
			if(quadruples.dirQuadruples[i][1] == True):
				i = quadruples.dirQuadruples[i][3] - 1

            #case for GOSUB
		elif(quadruples.dirQuadruples[i][0] == 16):
			#append next quadruple to the executionStack
			executionStack.append(i+1)

			#jump to function quadruple
			i = quadruples.dirQuadruples[i][3] - 1

            #case for RETURN
		elif(quadruples.dirQuadruples[i][0] == 17):

			#get return value from quadruple
			rtn = memoryStack[-1].returnAddress
			rtn_value = getValue(quadruples.dirQuadruples[1])

			#temporally pop memoryStack to assign return value to previous function
			memory_aux = memoryStack.pop()

			#assign return value to the return address of the function
			setValue(rtn, rtn_value)

			#return current fucntion memory to the memory stack
			memoryStack.append(memory_aux)

            #case for PRINT
		elif(quadruples.dirQuadruples[i][0] == 18):
			pass

            #case for INPUT
		elif(quadruples.dirQuadruples[i][0] == 19):
			pass

            #case for ERA
		elif(quadruples.dirQuadruples[i][0] == 20):
			#creates memory for a specific function createMemory(SubTypeQty)
			createMemory(quadruples.dirQuadruples[i][2])
			#assigns return address to memory
			memoryStack[-1].returnAddress = quadruples.dirQuadruples[i][3]
			print("Created Function memory: %s" %str(memoryStack[-1].memory))

            #case for ENDPROC
		elif(quadruples.dirQuadruples[i][0] == 21):
			#Returns to the next instruction after the function call
			print ("Delete Function MEMORY: %s" % memoryStack[-1].memory)
			i = executionStack.pop() - 1
			deleteMemory()

            #case for PARAM
		elif(quadruples.dirQuadruples[i][0] == 22):
			#get param types
			param_type = quadruples.dirQuadruples[i][1]
			#get param virtual memory addresses
			param_vaddress = quadruples.dirQuadruples[i][2]

			#Global
			if(param_vaddress < 4000):
				param_realAddr = param_vaddress % 1000
				#gets value from previous function (memory object)
				paramValue = memoryStack[-2].memory[param_type][param_realAddr]


			#constantes
			elif(param_vaddress < 10000):
				param_realAddr = param_vaddress
				paramValue = constMemory[param_realAddr]

			#locales
			else:
				param_realAddr = param_vaddress % 10000
				#gets value from previous function (memory object)
				paramValue = memoryStack[-2].memory[param_type][param_realAddr]

			#gets real address
			realAddr = quadruples.dirQuadruples[i][3]
			#Global
			if(param_vaddress < 4000):
				realAddr = realAddr % 1000

			#locales
			else:
				realAddr = realAddr % 10000

			#assigns paramValue to corresponding memory address
			memoryStack[-1].memory[param_type][realAddr] = paramValue
		i += 1
		print("")

	print ("FINAL MEMORY: %s" % memoryStack[-1].memory)

#########################################
#                                       #
#         Logging Object Rules          #
#                                       #
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
#                                       #
#               Main                    #
#                                       #
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
	#   print(tok)

	# Parse tokens read
	parser.parse(data, tracking=True, debug=log)

	# Create Memory for global vars
	initGlobalMemory(globalVarsTypeCounts)

	# Start machine
	startMachine()

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
