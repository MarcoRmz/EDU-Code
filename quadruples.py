#########################################################
#														#
# 	quadruples.py										#
#														#
# 	Quadruples											#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581			 			#
#														#
#########################################################

#########################################
#										#
#		 		Imports					#
#										#
#########################################

from semanticCube import *

#########################################
#										#
#		 		Variables				#
#										#
#########################################

# Stack for Operators
sOperators = []

# Stack for Operands
sOperands = []

# Stack for Types
sTypes = []

# Stack for Jumps
sJumps = []

# Stack for ERAs
sERA = []

# Stack for REFERENCE_PARAMS
sPARAMS = []

# Marks the index for the current quadruple
indexQuadruples = 0

# Directory for Quadruples
dirQuadruples = []
