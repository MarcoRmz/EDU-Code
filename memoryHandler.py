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
#        Functions for Compiler         #
#										#
#########################################

# Ask for next available memory address
#Global
def getGlobalAddress(varType, chunkSize):
	availableAddress = currentGlobalVirtualAddress[varType] + 1000
	currentGlobalVirtualAddress[varType] += chunkSize
	return availableAddress

# Constants
def setConstantAddress(varType, varValue):
	if invertedConstMemory.has_key(varValue):
		return invertedConstMemory[varValue]
	else:
		availableAddress = currentConstantVirtualAddress[varType]
		currentConstantVirtualAddress[varType] += 1
		invertedConstMemory[varValue] = availableAddress
		constMemory[availableAddress] = varValue
		return availableAddress

# Local
def getLocalAddress(varType, chunkSize):
	availableAddress = currentLocalVirtualAddress[varType]
	currentLocalVirtualAddress[varType] += chunkSize
	return availableAddress

#########################################
#										#
#    Functions for Virtual Machine      #
#										#
#########################################

# Function to Create Memory for process
def createMemory(TotalTypes, SubTypeQty):
	memoryStack.append(Memory(TotalTypes, SubTypeQty))

# Function to Delete process Memory
def deleteMemory():
	del memoryStack[-1]


# Get value from virtual address
def getValue(virtualAddress):
	#Global
	if(virtualAddress < 4000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		return globalMemory[varType[realAddr]]
	#constantes
	elif(virtualAddress < 10000):
		return constMemory[virtualAddress]

	#locales
	else:
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		return memoryStack[-1].memory[varType[realAddr]]

#set value from virtual address and value given by the virtual machine
def setValue(virtualAddress, varValue):
	#Global
	if(virtualAddress < 4000):
		varType = virtualAddress // 1000
		realAddr = virtualAddress % 1000
		globalMemory[varType[realAddr]] = varValue
	#locales
	elif(virtualAddress >= 10000):
		varType = (virtualAddress // 1000) - 1
		realAddr = virtualAddress % 1000
		memoryStack[-1].memory[varType[realAddr]] = varValue
