#########################################################
#														#
#	 virtualMachine.py									#
#														#
#	 Virtual Machine									#
#														#
#	 Marco Ramirez		 A01191344						#
#	 Andres Gutierrez	A01191581						#
#														#
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
		# Conditions to determine actions on quadruples

		#########################################
		#										#
		#			Case for PLUS (+)			#
		#										#
		#########################################
		if(quadruples.dirQuadruples[i][0] == 0):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply sum operation to operands
			result = operand1 + operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for MINUS (-)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 1):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply substraction operation to operands
			result = operand1 - operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for MULT (*)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 2):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply multiplication operation to operands
			result = operand1 * operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for DIVIDE (/)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 3):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply divide operation to operands
			result = operand1 / operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for AND				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 4):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply and operation to operands
			result = operand1 and operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for OR					#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 5):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply or operation to operands
			result = operand1 or operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for LESS than (<)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 6):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply less than to operands
			result = operand1 < operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for GREATER than (>)		#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 7):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply greater than to operands
			result = operand1 > operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#	Case for LESS THAN OR EQUALS (<=)	#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 8):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			##apply less than equals to operands
			result = operand1 <= operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		# Case for GREATER THAN OR EQUALS (<=)	#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 9):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply greater than equals to operands
			result = operand1 >= operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for DOUBLE EQUALS (==)		#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 10):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply double equals to operands
			result = operand1 == operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for DIFFERENT (!=)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 11):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply not equals to operands
			result = operand1 != operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for EQUALS (=)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 12):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][3]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#save the new value for the specified address
			setValue(operand2, operand1)


		#########################################
		#										#
		#			Case for GOTO				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 13):
			#obtain the index of the quadruple and jump to it
			i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOTOF				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 14):
			#if the temporal is false jump to the specified quadruple
			var_Value = getValue(quadruples.dirQuadruples[i][1])

			if (var_Value == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			if(var_Value == False):
				i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOTOT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 15):
			#if the temporal holds a True jump to the specified quadruple
			var_Value = getValue(quadruples.dirQuadruples[i][1])

			if (var_Value == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			if(var_Value == True):
				i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOSUB				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 16):
			#append next quadruple to the executionStack
			executionStack.append(i+1)

			#jump to function quadruple
			i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for RETURN				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 17):
			#get return value from quadruple
			rtn = memoryStack[-1].returnAddress
			rtn_value = getValue(quadruples.dirQuadruples[i][1])

			# If value is a list it links to an address, getValue of the address
			if type(rtn_value) is list:
				rtn_value = getValue(rtn_value[0])

			if (rtn_value == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#temporally pop memoryStack to assign return value to previous function
			memory_aux = memoryStack.pop()

			#assign return value to the return address of the function
			setValue(rtn, rtn_value)

			#return current fucntion memory to the memory stack
			memoryStack.append(memory_aux)


		#########################################
		#										#
		#			Case for PRINT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 18):
			print_result = ""
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][3]
			print "ssss"+str(operand1)
			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				for x in range(0,len(operand1)):
					if(type(operand1[x])is list):
						arr_dir = getValue(operand1[x][0])
						value = getValue(arr_dir)
						#if var has value or not
						if (value == None):
							# Error no value in address
							print("Operation failed, variable(s) missing value!")
							exit(1)
						if type(value) is str:
							print_result += value
						else:
							print_result += str(value)
					else:
						value = getValue(operand1[x])
						if (value == None):
							# Error no value in address
							print("Operation failed, variable(s) missing value!")
							exit(1)
						if type(value) is str:
							print_result += value
						else:
							print_result += str(value)


				#curr_operand = getValue(operand1[0])



				print(print_result)



		#########################################
		#										#
		#			Case for INPUT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 19):
			pass


		#########################################
		#										#
		#			Case for ERA				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 20):
			#creates memory for a specific function createMemory(SubTypeQty)
			createMemory(quadruples.dirQuadruples[i][2])
			#assigns return address to memory
			memoryStack[-1].returnAddress = quadruples.dirQuadruples[i][3]
			print("Created Function memory: %s returnAd: %s" %(str(memoryStack[-1].memory), str(memoryStack[-1].returnAddress)))


		#########################################
		#										#
		#		Case for ENDPROC				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 21):
			#Returns to the next instruction after the function call
			print ("Delete Function MEMORY: %s" % memoryStack[-1].memory)
			i = executionStack.pop() - 1
			deleteMemory()


		#########################################
		#										#
		#			Case for PARAM				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 22):
			#get param types
			param_type = quadruples.dirQuadruples[i][1]

			#get param virtual memory addresses
			param_vaddress = quadruples.dirQuadruples[i][2]

			# If param_vaddress is a list it links to an address, getValue of the address
			if type(param_vaddress) is list:
				memory_aux = memoryStack.pop()
				param_vaddress = getValue(param_vaddress[0])
				memoryStack.append(memory_aux)

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

			# If realAddr is a list it links to an address, getValue of the address
			if type(realAddr) is list:
				realAddr = getValue(realAddr[0])

			#Global
			if(realAddr < 4000):
				realAddr = realAddr % 1000

			#locales
			else:
				realAddr = realAddr % 10000

			#assigns paramValue to corresponding memory address
			memoryStack[-1].memory[param_type][realAddr] = paramValue


		#########################################
		#										#
		#			Case for VER				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 23):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][3]

			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			operand2 = getValue(operand2)

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			# Verify operand1 is less than vector size
			if operand1 >= operand2:
				# Error
				print("Invalid index: %d is larger than vector size!" %operand1)
				exit(1)


		#########################################
		#										#
		#		Case for PLUS_ADDR				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 24):
			#get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]

			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			operand1 = getValue(operand1)

			operand2 = quadruples.dirQuadruples[i][2]

			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			#apply sum operation to operands
			result = operand1 + operand2

			#save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)

		i += 1
		print("")

#########################################
#										#
#		 Logging Object Rules			#
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
#				 Main					#
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
	#	 print(tok)

	# Parse tokens read
	parser.parse(data, tracking=True, debug=log)

	# Create Memory for global vars
	initGlobalMemory(globalVarsTypeCounts)
	print "SSSSS" + str(quadruples.dirQuadruples)
	# Start machine
	startMachine()

	print("*****************************************")
	print("")
	print("Constant Vars: %s\n" %str(constMemory))
	i = 0
	print("Global Vars: %s\n" %str(globalVars))
	tempFunct = functionsDir.items()
	while(i < len(functionsDir)):
		print("function: %s, type: %s\nVars: %s\n" %(tempFunct[i][0], str(tempFunct[i][1][0]), str(tempFunct[i][1][1])))
		i += 1

	print("*****************************************")
	print("quadruples: ")
	i = 0
	while(quadruples.dirQuadruples[i][0] != 99):
		print("%d) %s" %(i, str(quadruples.dirQuadruples[i])))
		i += 1
	print("%d) %s" %(i, str(quadruples.dirQuadruples[i])))

	print("*****************************************")
	print("Num quadruples: " + str(quadruples.indexQuadruples))
	print("*****************************************")
	print("\nProgram Successful")
