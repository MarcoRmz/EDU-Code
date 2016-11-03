# -----------------------------------------------------------------------------
# memoryHandler.py
#
# Memory Handler
#
# Marco Ramirez 	A01191344
# Andres Gutierrez	A01191581
# -----------------------------------------------------------------------------

import memory

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


#										#
#										#
#        Functions for Compiler         #
#										#
#										#






#										#
#										#
#    Functions for Virtual Machine      #
#										#
#										#

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

