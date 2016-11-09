#########################################################
#														#
# 	memoryHandler.py									#
#														#
# 	Memory Handler										#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581       				#
#														#
#########################################################

from memory import *

#########################################
#										#
#         Variables for Memory          #
#										#
#########################################

# Starting Virtual addresses for memory spaces
# [INT, FLOAT, STRING, BOOL]
currentGlobalVirtualAddress = [0, 1000, 2000, 3000]
currentConstantVirtualAddress = [5000, 6000, 7000, 8000]

# Includes Local and Temporary Variable Addresses
currentLocalVirtualAddress = [10000, 20000, 30000, 40000]

# Memory for global variables
globalMemory = []

# Dictionary Memory for constants for virtual machine (key: address, value: value)
constMemory = {}

# Inverted Dictionary Memory for constants for compiler (key: value, value: address)
invertedConstMemory = {}

# Execution stack for memory
memoryStack = []

#########################################
#										#
#         Functions for Memory          #
#										#
#########################################

def initGlobalMemory(SubTypeQty):
	global globalMemory

	globalMemory = [[None] * 4]
	count = 0
	for i in range(0, 4):
		if SubTypeQty[i] != 0:
			globalMemory[count] = [None for y in range(0, SubTypeQty[i])]
			count += 1

#########################################
#										#
#        Functions for Compiler         #
#										#
#########################################
#Resets memory indexes
def resetMemoryIndexes():
	global currentGlobalVirtualAddress
	global currentConstantVirtualAddress
	global currentLocalVirtualAddress
	
	# Starting Virtual addresses for memory spaces
	# [INT, FLOAT, STRING, BOOL]
	currentGlobalVirtualAddress = [0, 1000, 2000, 3000]
	currentConstantVirtualAddress = [5000, 6000, 7000, 8000]

	# Includes Local and Temporary Variable Addresses
	currentLocalVirtualAddress = [10000, 20000, 30000, 40000]

#Checks if there is available memory for type and chunkSize for global memory
def globalAvailableMemory(varType, chunkSize):
	if chunkSize != 1:
		chunkSize = getValue(chunkSize)
	if(varType == 0):
		if currentGlobalVirtualAddress[0] + chunkSize < 2000:
			return True
	elif(varType == 1):
		if currentGlobalVirtualAddress[1] + chunkSize < 3000:
			return True
	elif(varType == 2):
		if currentGlobalVirtualAddress[2] + chunkSize < 4000:
			return True
	elif(varType == 3):
		if currentGlobalVirtualAddress[3] + chunkSize < 5000:
			return True
	return False

#Checks if there is available memory for type and chunkSize for constants memory
def constantAvailableMemory(varType):
	if(varType == 0):
		if currentConstantVirtualAddress[0] + 1 < 6000:
			return True
	elif(varType == 1):
		if currentConstantVirtualAddress[1] + 1 < 7000:
			return True
	elif(varType == 2):
		if currentConstantVirtualAddress[2] + 1 < 8000:
			return True
	elif(varType == 3):
		if currentConstantVirtualAddress[3] + 1 < 9000:
			return True
	return False

#Checks if there is available memory for type and chunkSize for local memory
def localAvailableMemory(varType, chunkSize):
	if chunkSize != 1:
		chunkSize = getValue(chunkSize)
	if(varType == 0):
		if currentLocalVirtualAddress[0] + chunkSize < 20000:
			return True
	elif(varType == 1):
		if currentLocalVirtualAddress[1] + chunkSize < 30000:
			return True
	elif(varType == 2):
		if currentLocalVirtualAddress[2] + chunkSize < 40000:
			return True
	elif(varType == 3):
		if currentLocalVirtualAddress[3] + chunkSize < 50000:
			return True
	return False

# Ask for next available memory address
#Global
def getGlobalAddress(varType, chunkSize):
	if chunkSize != 1:
		chunkSize = getValue(chunkSize)
	if(globalAvailableMemory(varType,chunkSize)):
		availableAddress = currentGlobalVirtualAddress[varType] + 1000
		currentGlobalVirtualAddress[varType] += chunkSize
		return availableAddress
	else:
		print("Segmentation fault: out of memory")
		exit(1)

# Constants
def setConstantAddress(varType, varValue):
	if invertedConstMemory.has_key(varValue):
		return invertedConstMemory[varValue]
	else:
		if(constantAvailableMemory(varType)):
			availableAddress = currentConstantVirtualAddress[varType]
			currentConstantVirtualAddress[varType] += 1
			invertedConstMemory[varValue] = availableAddress
			constMemory[availableAddress] = varValue
			return availableAddress
		else:
			print("Segmentation fault: out of memory")
			exit(1)

# Local
def getLocalAddress(varType, chunkSize):
	if chunkSize != 1:
		chunkSize = getValue(chunkSize)
	if(localAvailableMemory(varType,chunkSize)):
		availableAddress = currentLocalVirtualAddress[varType]
		currentLocalVirtualAddress[varType] += chunkSize
		return availableAddress
	else:
		print("Segmentation fault: out of memory")
		exit(1)

#########################################
#										#
#    Functions for Virtual Machine      #
#										#
#########################################

# Function to Create Memory for process
def createMemory(SubTypeQty):
	memoryStack.append(Memory(SubTypeQty))

# Function to Delete process Memory
def deleteMemory():
	del memoryStack[-1]


# Get value from virtual address
def getValue(virtualAddress):
	#Global
	if(virtualAddress < 4000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		return globalMemory[varType][realAddr]

	#constantes
	elif(virtualAddress < 10000):
		return constMemory[virtualAddress]

	#locales
	else:
		varType = (virtualAddress // 10000) - 1
		realAddr = virtualAddress % 10000
		return memoryStack[-1].memory[varType][realAddr]

#set value from virtual address and value given by the virtual machine
def setValue(virtualAddress, varValue):
	#Global
	print("virtual %d, value: %s" %(virtualAddress, str(varValue)))
	if(virtualAddress < 4000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		globalMemory[varType][realAddr] = varValue

	#locales
	elif(virtualAddress >= 10000):
		varType = (virtualAddress // 10000) - 1
		realAddr = virtualAddress % 10000
		print("type: %s, addr: %s\nmemory: %s" %(str(varType), str(realAddr), str(memoryStack[-1].memory)))
		memoryStack[-1].memory[varType][realAddr] = varValue
