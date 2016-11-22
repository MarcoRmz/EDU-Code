#########################################################
#														#
# 	memoryHandler.py									#
#														#
# 	Memory Handler										#
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

from memory import *

#########################################
#										#
#		 Variables for Memory			#
#										#
#########################################

# Starting Virtual addresses for memory spaces
# [INT, FLOAT, STRING, BOOL]
currentGlobalVirtualAddress = [0, 1000, 2000, 3000]
currentConstantVirtualAddress = [5000, 6000, 7000, 8000]

# Includes Local and Temporary Variable Addresses
currentLocalVirtualAddress = [10000, 20000, 30000, 40000]

# Initial Local and Temporary Variable Addresses
initialtINTVarAddress = 10000
initialtFLOATVarAddress = 20000
initialtSTRINGVarAddress = 30000
initialtBOOLVarAddress = 40000
initialLocalVirtualAddresses = [10000, 20000, 30000, 40000]

# Memory for global variables
globalMemory = []

# Dictionary Memory for constants for virtual machine
# (key: address, value: value)
constMemory = {}

# Inverted Dictionary Memory for constants for compiler
# (key: value, value: address)
invertedConstMemory = {}

# Execution stack for memory
memoryStack = []

#########################################
#										#
#		 Functions for Memory			#
#										#
#########################################

# Function that initializes the Global memory with the
# amount of global variables used in the program given
# by the SubTypeQty parameter
def initGlobalMemory(SubTypeQty):
	global globalMemory

	# Initializes the memory with a list for each type
	# [[INTs], [FLOATs], [STRINGs], [BOOLs]]
	globalMemory = [[None]] * 4

	# Adds a space for each variable used in its corresponding type
	count = 0
	for i in range(0, 4):
		if SubTypeQty[i] != 0:
			globalMemory[count] = [None] * SubTypeQty[i]
		count += 1

#########################################
#										#
#		Functions for Compiler		 	#
#										#
#########################################

# Function used to reset the memory indexes
# after a function is finished compiling
def resetMemoryIndexes():
	global currentLocalVirtualAddress

	# Starting Virtual addresses for memory spaces
	# [INT, FLOAT, STRING, BOOL]
	currentLocalVirtualAddress = [initialtINTVarAddress, initialtFLOATVarAddress, initialtSTRINGVarAddress, initialtBOOLVarAddress]

# Function that checks if there is available memory
# in the global memory for type and chunkSize given
def globalAvailableMemory(varType, chunkSize):
	# TYPE INT
	if(varType == 0):
		if currentGlobalVirtualAddress[0] + chunkSize < 1000:
			return True
	# TYPE FLOAT
	elif(varType == 1):
		if currentGlobalVirtualAddress[1] + chunkSize < 2000:
			return True
	# TYPE STRING
	elif(varType == 2):
		if currentGlobalVirtualAddress[2] + chunkSize < 3000:
			return True
	# TYPE BOOL
	elif(varType == 3):
		if currentGlobalVirtualAddress[3] + chunkSize < 4000:
			return True
	return False

# Function that checks if there is available memory
# in constant memory for type given
def constantAvailableMemory(varType):
	# TYPE INT
	if(varType == 0):
		if currentConstantVirtualAddress[0] + 1 < 6000:
			return True
	# TYPE FLOAT
	elif(varType == 1):
		if currentConstantVirtualAddress[1] + 1 < 7000:
			return True
	# TYPE STRING
	elif(varType == 2):
		if currentConstantVirtualAddress[2] + 1 < 8000:
			return True
	# TYPE BOOL
	elif(varType == 3):
		if currentConstantVirtualAddress[3] + 1 < 9000:
			return True
	return False

# Function that checks if there is available memory
# in the local memory for type and chunkSize given
def localAvailableMemory(varType, chunkSize):
	# TYPE INT
	if(varType == 0):
		if currentLocalVirtualAddress[0] + chunkSize < 20000:
			return True
	# TYPE FLOAT
	elif(varType == 1):
		if currentLocalVirtualAddress[1] + chunkSize < 30000:
			return True
	# TYPE STRING
	elif(varType == 2):
		if currentLocalVirtualAddress[2] + chunkSize < 40000:
			return True
	# TYPE BOOL
	elif(varType == 3):
		if currentLocalVirtualAddress[3] + chunkSize < 50000:
			return True
	return False

# Function that asks for next available memory address
# in the global memory given the type and size of the variable
def getGlobalAddress(varType, chunkSize):
	# Parse chunkSize to get value
	chunkSize = getValue(chunkSize)

	# Check if chunkSize contains a value
	if chunkSize == None:
		return None

	# Check if there's memory available for type with chunkSize
	if(globalAvailableMemory(varType,chunkSize)):
		# Fetch next available index
		availableAddress = currentGlobalVirtualAddress[varType] + 1000

		# Move index by the chunkSize used
		currentGlobalVirtualAddress[varType] += chunkSize

		# Return the available memory address
		return availableAddress
	else:
		# ERROR
		print("Segmentation fault: out of global memory")
		exit(1)

# Function that adds the given value from varValue to the constants
# memory dictionary in the corresponding type given by the varType
# and returns its address for its memory address
def setConstantAddress(varType, varValue):
	# Checks if value already exists in dictionary
	if invertedConstMemory.has_key(varValue):
		# If value exists it returns its address
		return invertedConstMemory[varValue]
	else:
		# Check if there's memory available for type
		if(constantAvailableMemory(varType)):
			# Fetch next available index
			availableAddress = currentConstantVirtualAddress[varType]

			# Move index by 1
			currentConstantVirtualAddress[varType] += 1

			# Add used address in inverted constant dictionary
			invertedConstMemory[varValue] = availableAddress

			# Add value in constant dictionary
			constMemory[availableAddress] = varValue

			# Return the used memory address
			return availableAddress
		else:
			# ERROR
			print("Segmentation fault: out of constant memory")
			exit(1)

# Function that asks for next available memory address
# in the local memory given the type and size of the variable
def getLocalAddress(varType, chunkSize):
	# Parse chunkSize to get value
	chunkSize = getValue(chunkSize)

	# Check if chunkSize contains a value
	if chunkSize == None:
		return None
	
	# Check if there's memory available for type with chunkSize
	if(localAvailableMemory(varType,chunkSize)):
		# Fetch next available index
		availableAddress = currentLocalVirtualAddress[varType]

		# Move index by the chunkSize used
		currentLocalVirtualAddress[varType] += chunkSize

		# Return the available memory address
		return availableAddress
	else:
		# ERROR
		print("Segmentation fault: out of local memory")
		exit(1)

# Function that gets the total amount of variables
# per type used in the local memory by substracting the
# current indexes by the initial indexes
def getLocalVarQty():
	# Initializes list with total amounts to return
	totalVarQty = [0,0,0,0]

	# Substracts the current index type in x by the initial index type in x
	for x in xrange(0,4):
		totalVarQty[x] = currentLocalVirtualAddress[x] - initialLocalVirtualAddresses[x]

	# Returns tha total amounts per type in the list totalVarQty
	return totalVarQty

#########################################
#										#
#	Functions for Virtual Machine		#
#										#
#########################################

# Function used by the quadruple ERA to create
# memory for a new function with the amount of space
# needed given the amount of variables used per type
# by the parameter SubTypeQty
def createMemory(SubTypeQty):
	# Initializes the memory and appends it to the memory stack
	memoryStack.append(Memory(SubTypeQty))

# Function used by the ENDPROC quadruple that
# deletes the function's Memory
def deleteMemory():
	del memoryStack[-1]

# Function used to parse the given virtualAddress
# to a real address and return the correct value
def getValue(virtualAddress):
	# Parse virtual address to int
	virtualAddress = int(virtualAddress)

	# Checks if virtual address is in the Global memory range
	if(virtualAddress < 4000):
		# Get the variable type by getting the first number
		# and substracting it by the offset
		varType = (virtualAddress // 1000) - 1

		# Get the real address by getting everything except the first number
		realAddr = virtualAddress % 1000

		# Use the type and the real address to fetch the value
		varValue = globalMemory[varType][realAddr]

	# Checks if virtual address is in the constants memory range
	elif(virtualAddress < 10000):
		# Uses the address to fetch the value
		varValue = constMemory[virtualAddress]

	# Checks if virtual address is in the local memory range
	else:
		# Get the variable type by getting the first number
		# and substracting it by the offset
		varType = (virtualAddress // 10000) - 1

		# Get the real address by getting everything except the first number
		realAddr = virtualAddress % 10000

		# Use the type and the real address to fetch the value
		varValue = memoryStack[-1].memory[varType][realAddr]

	# Verify that the address contained a value and return it
	if varValue == None:
		return None
	else:
		return varValue

# Function used to parse the given virtualAddress to a
# real address and set the given value in the real address
def setValue(virtualAddress, varValue):
	# Parse virtual address to int
	virtualAddress = int(virtualAddress)

	# Checks if virtual address is in the Global memory range
	if(virtualAddress < 4000):
		# Get the variable type by getting the first number
		# and substracting it by the offset
		varType = (virtualAddress // 1000) - 1

		# Get the real address by getting everything except the first number
		realAddr = virtualAddress % 1000

		# Use the type and the real address to set the value
		globalMemory[varType][realAddr] = varValue

	#locales
	elif(virtualAddress >= 10000):
		# Get the variable type by getting the first number
		# and substracting it by the offset
		varType = (virtualAddress // 10000) - 1

		# Get the real address by getting everything except the first number
		realAddr = virtualAddress % 10000

		# Use the type and the real address to set the value
		memoryStack[-1].memory[varType][realAddr] = varValue
