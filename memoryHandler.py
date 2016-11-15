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

# Initial Local and Temporary Variable Addresses
initialtINTVarAddress = 10000
initialtFLOATVarAddress = 20000
initialtSTRINGVarAddress = 30000
initialtBOOLVarAddress = 40000
initialLocalVirtualAddresses = [10000, 20000, 30000, 40000]

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

	globalMemory = [[None]] * 4
	count = 0
	for i in range(0, 4):
		if SubTypeQty[i] != 0:
			globalMemory[count] = [None] * SubTypeQty[i]
		count += 1

	print("Init Global memory: %s, SubTypeQty: %s" %(str(globalMemory), str(SubTypeQty)))

#########################################
#										#
#        Functions for Compiler         #
#										#
#########################################
#Resets memory indexes
def resetMemoryIndexes():
	global currentLocalVirtualAddress
	print("\n\n\n\n LOCAL MEMORY BEFORE RESET \n%s" %str(currentLocalVirtualAddress))
	
	# Starting Virtual addresses for memory spaces
	# [INT, FLOAT, STRING, BOOL]
	currentLocalVirtualAddress = [initialtINTVarAddress, initialtFLOATVarAddress, initialtSTRINGVarAddress, initialtBOOLVarAddress]
	print("LOCAL MEMORY AFTER RESET \n%s\n\n\n" %str(currentLocalVirtualAddress))

#Checks if there is available memory for type and chunkSize for global memory
def globalAvailableMemory(varType, chunkSize):
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
	# Parse chunkSize if it's an Address
	if chunkSize > 1:
		chunkSize = getValue(chunkSize)
		if chunkSize == -1:
			return -1
	# Check if there's memory available for type with chunkSize
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
		# Check if there's memory available for type
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
	# Parse chunkSize if it's an Address
	if chunkSize > 1:
		chunkSize = getValue(chunkSize)
		if chunkSize == -1:
			return -1
	# Check if there's memory available for type with chunkSize
	if(localAvailableMemory(varType,chunkSize)):
		availableAddress = currentLocalVirtualAddress[varType]
		currentLocalVirtualAddress[varType] += chunkSize
		return availableAddress
	else:
		print("Segmentation fault: out of memory")
		exit(1)

def getLocalVarQty():
	totalVarQyt = [0,0,0,0]
	for x in xrange(0,4):
		totalVarQyt[x] = currentLocalVirtualAddress[x] - initialLocalVirtualAddresses[x]
	return totalVarQyt

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
	print("GET VALUE")
	if(virtualAddress < 4000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		print("Type: %d, rAddr: %d" %(varType, realAddr))
		varValue = globalMemory[varType][realAddr]
		print("Global mem: %s\n" %(str(globalMemory)))

	#constantes
	elif(virtualAddress < 10000):
		print("vAddr: %d" %(virtualAddress))
		varValue = constMemory[virtualAddress]
		print("Constants: %s\n" %(str(constMemory)))

	#locales
	else:
		varType = (virtualAddress // 10000) - 1
		realAddr = virtualAddress % 10000
		print("Type: %d, rAddr: %d" %(varType, realAddr))
		varValue = memoryStack[-1].memory[varType][realAddr]
		print("Local mem: %s\n" %(str(memoryStack[-1].memory)))

	if varValue == None:
		return -1
	else:
		return varValue


#set value from virtual address and value given by the virtual machine
def setValue(virtualAddress, varValue):
	#Global
	print("SET VALUE\nvirtual %d, value: %s" %(virtualAddress, str(varValue)))
	if(virtualAddress < 4000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		globalMemory[varType][realAddr] = varValue
		print("type: %s, addr: %s\nGlobal memory: %s" %(str(varType), str(realAddr), str(globalMemory)))

	#locales
	elif(virtualAddress >= 10000):
		varType = (virtualAddress // 10000) - 1
		realAddr = virtualAddress % 10000
		memoryStack[-1].memory[varType][realAddr] = varValue
		print("type: %s, addr: %s\nFunction memory: %s" %(str(varType), str(realAddr), str(memoryStack[-1].memory)))
