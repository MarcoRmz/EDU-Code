# -----------------------------------------------------------------------------
# memoryHandler.py
#
# Memory Handler
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

import memory

#########################################
#										#
#         Variables for Memory          #
#										#
#########################################

# Starting Virtual addresses for memory spaces
# [INT, FLOAT, STRING, BOOL]
currentGlobalVirtualAddress = [0, 1000, 2000, 3000]
currentConstantVirtualAddress = [4000, 5000, 6000, 7000]

# Includes Local and Temporary Variable Addresses
currentLocalVirtualAddress = [10000, 20000, 30000, 40000]

# Memory for global variables
globalMemory = [[][][][]]

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
	availableAddress = currentGlobalVirtualAddress[varType]
	currentGlobalVirtualAddress[varType] += chunkSize
	return availableAddress

# Constants
def setConstantAddress(varType, varValue):
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

# Parse Virtual Address to Real Address and set new value
# Global
def setGlobalValue(virtualAddress, varValue):
	varType = virtualAddress // 1000
	realAddr = virtualAddress % 1000
	globalMemory[varType[realAddr]] = varValue

# Local
def setLocalValue(virtualAddress, varValue):
	varType = (virtualAddress // 1000) - 1
	realAddr = virtualAddress % 1000
	memoryStack[-1].memory[varType[realAddr]] = varValue

# Parse Virtual Address to Real Address and get value
# Global
def getGlobalValue(virtualAddress):
	varType = virtualAddress // 1000
	realAddr = virtualAddress % 1000
	return globalMemory[varType[realAddr]]

# Constants
def getConstantValue(virtualAddress):
	return constMemory[virtualAddress]

# Local
def getLocalValue(virtualAddress):
	varType = (virtualAddress // 1000) - 1
	realAddr = virtualAddress % 1000
	return memoryStack[-1].memory[varType[realAddr]]

