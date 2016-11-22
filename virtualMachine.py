#########################################################
#														#
#	 virtualMachine.py									#
#														#
#	 Virtual Machine									#
#														#
#	 Marco Ramirez		A01191344						#
#	 Andres Gutierrez	A01191581						#
#														#
#########################################################

from memoryHandler import *
from quadruples import *
from eduCodeParser import *

executionStack = []

def evaluateSTR2BOOL(value):
	if (value.lower() in ("yes", "true", "t", "v", "verdadero")):
		return True;
	elif (value.lower() in ("no", "false", "f", "falso")):
		return False;
	else:
		# Error
		print("Expected input type BOOL not STRING!")
		exit(1)

# Prints all program info:
#	Constant and Global memory
#	Functions & Main
#	Quadruples
def programInfo():
	print("*****************************************")
	print("")
	print("Constant Vars: %s\n" %str(constMemory))
	
	print("Global Vars: %s\n" %str(globalVars))

	i = 0
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
	print("\nProgram Successful")

def startMachine():
	#Count variable for quadruples
	i = 0

	#While the quadruple holds no EOF operation
	while(quadruples.dirQuadruples[i][0] != 99):
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
			print_result = ""
			# get operands from the memory
			operand1 = quadruples.dirQuadruples[i][1]
			varType = quadruples.dirQuadruples[i][2]
			returnAddress = quadruples.dirQuadruples[i][3]

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

				# Print generated message & wait for input
				if (varType == INT) or (varType == FLOAT):
					# Evaluate input
					inputValue = eval(raw_input(print_result))

					# Validate input is of expected type
					if (varType == INT and type(inputValue) is int) or (varType == FLOAT and type(inputValue) is float):
						# Assign value to return address
						setValue(returnAddress, inputValue)
					else:
						# Error
						print("Expected input of type %s, not %s!" %(parseType(varType), str(type(inputValue))))
						exit(1)
				else:
					# Get raw input
					inputValue = raw_input(print_result)
					if (varType == STRING):
						inputValue = str(inputValue)
					elif (varType == BOOL):
						inputValue	= str(inputValue)
						inputValue = evaluateSTR2BOOL(inputValue)
					else:
						# Error
						print("Expected input of type %s, not %s!" %(parseType(varType), str(type(inputValue))))
						exit(1)
					# Assign value to return address
					setValue(returnAddress, inputValue)


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


		#########################################
		#										#
		#		Case for ENDPROC				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 21):
			#Returns to the next instruction after the function call
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

			# Gets function variable address
			functionVarAddress = quadruples.dirQuadruples[i][3]

			# If functionVarAddress is a list it links to an address, getValue of the address
			if type(functionVarAddress) is list:
				functionVarAddress = getValue(functionVarAddress[0])

			#Global
			if(functionVarAddress < 4000):
				functionVarAddress = functionVarAddress % 1000

			#locales
			else:
				functionVarAddress = functionVarAddress % 10000

			#assigns paramValue to corresponding memory address
			memoryStack[-1].memory[param_type][functionVarAddress] = paramValue


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


		#########################################
		#										#
		#		Case for REFERENCE_PARAM		#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 25):
			# Get variables from the quadraple
			varAddress = quadruples.dirQuadruples[i][1]

			# If var is a list get indirect address
			if type(varAddress) is list:
				varAddress = getValue(varAddress[0])

			varAddress = getValue(varAddress)

			returnAddress = quadruples.dirQuadruples[i][3]

			# Store current memory in temporary var
			memory_aux = memoryStack.pop()
			
			# If var is a list get indirect address
			if type(returnAddress) is list:
				returnAddress = getValue(returnAddress[0])

			if (varAddress == None) or (returnAddress == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			# Set varAddress value to reference parameter
			setValue(returnAddress, varAddress)

			# Restore current memory
			memoryStack.append(memory_aux)

		i += 1

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

	# Parse tokens read
	parser = yacc.yacc()
	parser.parse(data)

	# Create Memory for global vars
	initGlobalMemory(globalVarsTypeCounts)

	# Start machine
	startMachine()

	# Print program details: memory, modules, quadruples
	#programInfo()
