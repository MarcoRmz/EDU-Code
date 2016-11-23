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

#########################################
#										#
#		 		Imports					#
#										#
#########################################

from memoryHandler import *
from quadruples import *
from eduCodeParser import *
import sys

#########################################
#										#
#		Quadruple Execution Stack		#
#										#
#########################################
executionStack = []

#########################################
#										#
#		 	Virtual Machine				#
#		 	Helper Functions			#
#										#
#########################################

# Function evaluates the input of type BOOL
# given a string it looks up the options
# available for a bool = true or a bool = false
def evaluateSTR2BOOL(value):
	# Looks up string in options for True
	if (value.lower() in ("yes", "true", "t", "v", "verdadero")):
		return True;
	# Looks up string in options for False
	elif (value.lower() in ("no", "false", "f", "falso")):
		return False;
	else:
		# if there's no match an error is raised
		# ERROR
		print("Expected input type BOOL not STRING!")
		exit(1)

# Function that prints all program info:
#	Constant and Global memory
#	Functions & Main declaration
#	Generated quadruples
def programInfo():
	print("*****************************************")
	print("")
	# Prints constant memory
	print("Constant Vars: %s\n" %str(constMemory))

	# Prints global memory
	print("Global Vars: %s\n" %str(globalVars))

	# Iterates and prints every function declared including main
	i = 0
	tempFunct = functionsDir.items()
	while(i < len(functionsDir)):
		print("function: %s, type: %s\nVars: %s\n" %(tempFunct[i][0], str(tempFunct[i][1][0]), str(tempFunct[i][1][1])))
		i += 1

	print("*****************************************")
	print("quadruples: ")
	# Iterates and prints every generated quadruple
	i = 0
	while(quadruples.dirQuadruples[i][0] != 99):
		print("%d) %s" %(i, str(quadruples.dirQuadruples[i])))
		i += 1
	print("%d) %s" %(i, str(quadruples.dirQuadruples[i])))

	print("*****************************************")

# Function used to start the machine and execute
# the generated quadruples for the program
def startMachine():
	#Count variable for quadruples
	i = 0

	# While the quadruple holds no EOF operation
	# read and execute the quadruple
	while(quadruples.dirQuadruples[i][0] != 99):

		#########################################
		#										#
		#			Case for PLUS (+)			#
		#										#
		#########################################
		if(quadruples.dirQuadruples[i][0] == 0):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation PLUS failed, variable(s) missing value!")
				exit(1)

			# Apply sum operation to operands
			result = operand1 + operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for MINUS (-)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 1):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation MINUS failed, variable(s) missing value!")
				exit(1)

			# Apply substraction operation to operands
			result = operand1 - operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for MULT (*)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 2):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation MULT failed, variable(s) missing value!")
				exit(1)

			# Apply multiplication operation to operands
			result = operand1 * operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for DIVIDE (/)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 3):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation DIVIDE failed, variable(s) missing value!")
				exit(1)

			# Apply divide operation to operands
			result = operand1 / operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for AND				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 4):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation AND failed, variable(s) missing value!")
				exit(1)

			# Apply and operation to operands
			result = operand1 and operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for OR					#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 5):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation OR failed, variable(s) missing value!")
				exit(1)

			# Apply or operation to operands
			result = operand1 or operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for LESS than (<)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 6):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation LESS failed, variable(s) missing value!")
				exit(1)

			# Apply less than to operands
			result = operand1 < operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for GREATER than (>)		#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 7):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation GREATER failed, variable(s) missing value!")
				exit(1)

			# Apply greater than to operands
			result = operand1 > operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#	Case for LESS THAN OR EQUALS (<=)	#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 8):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation LESS THAN OR EQUAL failed, variable(s) missing value!")
				exit(1)

			## Apply less than equals to operands
			result = operand1 <= operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		# Case for GREATER THAN OR EQUALS (>=)	#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 9):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation GREATER THAN OR EQUAL failed, variable(s) missing value!")
				exit(1)

			# Apply greater than equals to operands
			result = operand1 >= operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for DOUBLE EQUALS (==)		#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 10):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation DOUBLE EQUALS failed, variable(s) missing value!")
				exit(1)

			# Apply double equals to operands
			result = operand1 == operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#		Case for DIFFERENT (!=)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 11):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation DIFFERENT failed, variable(s) missing value!")
				exit(1)

			# Apply not equals to operands
			result = operand1 != operand2

			# Save the new value for the specified address
			setValue(quadruples.dirQuadruples[i][3],result)


		#########################################
		#										#
		#			Case for EQUALS (=)			#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 12):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If value is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][3]

			# If value is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation EQUALS failed, variable(s) missing value!")
				exit(1)

			# Save the new value for the specified address
			setValue(operand2, operand1)


		#########################################
		#										#
		#			Case for GOTO				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 13):
			# Obtain the index of the quadruple and jump to it
			# Subtract one to take into account while i += 1
			i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOTOF				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 14):
			# Get value of address from quadruple
			varValue = getValue(quadruples.dirQuadruples[i][1])

			# Verify value is not None
			if (varValue == None):
				# Error no value in address
				print("Operation GOTOF failed, variable(s) missing value!")
				exit(1)

			# If the temporal is false jump to the specified quadruple
			if(varValue == False):
				# Obtain the index of the quadruple and jump to it
				# Subtract one to take into account while i += 1
				i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOTOT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 15):
			# Get value of address from quadruple
			varValue = getValue(quadruples.dirQuadruples[i][1])

			# Verify value is not None
			if (varValue == None):
				# Error no value in address
				print("Operation GOTOT failed, variable(s) missing value!")
				exit(1)

			# If the temporal holds a True jump to the specified quadruple
			if(varValue == True):
				# Obtain the index of the quadruple and jump to it
				# Subtract one to take into account while i += 1
				i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for GOSUB				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 16):
			# Append next quadruple to the executionStack
			executionStack.append(i+1)

			# Jump to function quadruple
			# Subtract one to take into account while i += 1
			i = quadruples.dirQuadruples[i][3] - 1


		#########################################
		#										#
		#			Case for RETURN				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 17):
			# Get return address from the function's memory object
			rtn = memoryStack[-1].returnAddress

			# Get the return value from the quadruple
			rtnValue = getValue(quadruples.dirQuadruples[i][1])

			# If value is a list it links to an address, getValue of the address
			if type(rtnValue) is list:
				rtnValue = getValue(rtnValue[0])

			# Verify that value is not None
			if (rtnValue == None):
				# Error no value in address
				print("Operation RETURN failed, variable(s) missing value!")
				exit(1)

			# Temporally pop memoryStack to assign return
			# value to previous function's memory
			memoryAux = memoryStack.pop()

			# Assign return value to the return address of
			# the function
			setValue(rtn, rtnValue)

			# Return current fucntion memory to the memory stack
			memoryStack.append(memoryAux)


		#########################################
		#										#
		#			Case for PRINT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 18):
			# Initialize print result empty
			printResult = ""

			# Get print list form quadruple
			printList = quadruples.dirQuadruples[i][3]

			# Verifies print list is a list
			if type(printList) is list:
				for x in range(0,len(printList)):
					# If value is a list it links to an address, getValue of the address
					if(type(printList[x])is list):
						# Gets value from indirect Address
						arr_dir = getValue(printList[x][0])
						value = getValue(arr_dir)
					else:
						# Get value from address
						value = getValue(printList[x])

					# Verifies that value is not None
					if (value == None):
						# Error no value in address
						print("Operation PRINT failed, variable(s) missing value!")
						exit(1)

					# Checks if value is already of type STRING
					# and appends to printResult
					if type(value) is str:
						printResult += value
					else:
						# Parse value to STRING and append to printResult
						printResult += str(value)

				# Prints result
				print(printResult)

			else:
				# ERROR
				print("Operation PRINT failed, print list has no values to print!")
				exit(1)


		#########################################
		#										#
		#			Case for INPUT				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 19):
			# Initialize print result empty
			printResult = ""

			# Get print list from the quadruple
			printList = quadruples.dirQuadruples[i][1]

			# Get expected var type from the quadruple
			varType = quadruples.dirQuadruples[i][2]

			# Get the return address from the quadruple
			returnAddress = quadruples.dirQuadruples[i][3]

			# Verifies print list is a list
			if type(printList) is list:
				for x in range(0,len(printList)):
					# If value is a list it links to an address, getValue of the address
					if(type(printList[x])is list):
						# Gets value from indirect Address
						arr_dir = getValue(printList[x][0])
						value = getValue(arr_dir)
					else:
						# Get value from address
						value = getValue(printList[x])

					# Verifies that value is not None
					if (value == None):
						# Error no value in address
						print("Operation INPUT failed, variable(s) missing value!")
						exit(1)

					# Checks if value is already of type STRING
					# and appends to printResult
					if type(value) is str:
						printResult += value
					else:
						# Parse value to STRING and append to printResult
						printResult += str(value)

				# Print generated message & wait for input
				if (varType == INT) or (varType == FLOAT):
					# Evaluate input for INTs and FLOATs
					inputValue = eval(raw_input(printResult))

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
					inputValue = raw_input(printResult)
					if (varType == STRING):
						# Parse input as string
						inputValue = str(inputValue)
					elif (varType == BOOL):
						# Parse input as string
						inputValue	= str(inputValue)

						# Evaluate input as bool
						inputValue = evaluateSTR2BOOL(inputValue)
					else:
						# Error
						print("Expected input of type %s, not %s!" %(parseType(varType), str(type(inputValue))))
						exit(1)

					# Assign value to return address
					setValue(returnAddress, inputValue)

			else:
				# ERROR
				print("Operation INPUT failed, print list has no values to print!")
				exit(1)


		#########################################
		#										#
		#			Case for ERA				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 20):
			# Calls function to create memory given the
			# SubTypeQty in the quadruple
			createMemory(quadruples.dirQuadruples[i][2])

			# Assigns the return address to the created memory
			# given by the quadruple
			memoryStack[-1].returnAddress = quadruples.dirQuadruples[i][3]


		#########################################
		#										#
		#		Case for ENDPROC				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 21):
			# Returns to the next instruction after the
			# function call was made
			i = executionStack.pop() - 1

			# Calls the function to delete the function's memory
			deleteMemory()


		#########################################
		#										#
		#			Case for PARAM				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 22):
			# Get the type of the parameter from the quadruple
			paramType = quadruples.dirQuadruples[i][1]

			# Get the virtual memory address for the parameter
			paramVAddress = quadruples.dirQuadruples[i][2]

			# Temporary pops current memory to access previous memory
			memoryAux = memoryStack.pop()

			# If paramVAddress is a list it links to an address, getValue of the address
			if type(paramVAddress) is list:
				paramVAddress = getValue(paramVAddress[0])

			# Get value of parameter
			paramVAddress = getValue(paramVAddress)

			# Reassigns current memory to stack
			memoryStack.append(memoryAux)

			# Gets function variable address
			functionVarAddress = quadruples.dirQuadruples[i][3]

			# If functionVarAddress is a list it links to an address, getValue of the address
			if type(functionVarAddress) is list:
				functionVarAddress = getValue(functionVarAddress[0])

			# Set the value of the parameter in the function's variable
			setValue(functionVarAddress, paramVAddress)


		#########################################
		#										#
		#			Case for VER				#
		#										#
		#########################################
		elif(quadruples.dirQuadruples[i][0] == 23):
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If operand1 is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][3]

			# If operand2 is a list it links to an address, getValue of the address
			if type(operand2) is list:
				operand2 = getValue(operand2[0])

			# Fetch the value from memory
			operand2 = getValue(operand2)

			# Verify that neither of the operands has the value missing
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
			# Get operand1 from the quadruple
			operand1 = quadruples.dirQuadruples[i][1]

			# If operand2 is a list it links to an address, getValue of the address
			if type(operand1) is list:
				operand1 = getValue(operand1[0])

			# Fetch the value from memory
			operand1 = getValue(operand1)

			# Get operand2 from the quadruple
			operand2 = quadruples.dirQuadruples[i][2]

			# Verify that neither of the operands has the value missing
			if (operand1 == None) or (operand2 == None):
				# Error no value in address
				print("Operation failed, variable(s) missing value!")
				exit(1)

			# Apply sum operation to operands
			result = operand1 + operand2

			# Save the new value for the specified address
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

			# Fetch value from address
			varAddress = getValue(varAddress)

			# Get return addres of parameter from quadruple
			returnAddress = quadruples.dirQuadruples[i][3]

			# Store current memory in temporary var
			memoryAux = memoryStack.pop()

			# If returnAddress is a list get indirect address
			if type(returnAddress) is list:
				returnAddress = getValue(returnAddress[0])

			# Verify that neither variables is None
			if (varAddress == None) or (returnAddress == None):
				# Error no value in address
				print("Operation REFERENCE_PARAM failed, variable(s) missing value!")
				exit(1)

			# Set varAddress value to reference parameter
			setValue(returnAddress, varAddress)

			# Restore current memory
			memoryStack.append(memoryAux)

		# Move to next quadruple
		i += 1

#########################################
#										#
#				 Main					#
#										#
#########################################

if __name__ == '__main__':
	# Check for argument on file name to read
	if (len(sys.argv) > 1):
		eduFile = sys.argv[1]
	else:
		print("No EDU-Code file provided!")
		exit(1)

	# Open and read file

	try:
		f = open(eduFile, 'r')
	except IOError:
		print "Error: File doesn't appear to exist!"
		exit(1)

	data = f.read()

	# clear all non ascii

	# Parse tokens from data
	parser = yacc.yacc()
	parser.parse(data)

	# Create Memory for global vars
	initGlobalMemory(globalVarsTypeCounts)

	# Start machine
	startMachine()

	# Print program details:
	#	memory, modules, quadruples
	#programInfo()
