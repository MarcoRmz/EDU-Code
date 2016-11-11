#########################################################
#                                                       #
#   semanticCube.py                                    #
#                                                       #
#   Cubo Semantico                                      #
#                                                       #
#   Marco Ramirez       A01191344                       #
#   Andres Gutierrez    A01191581                       #
#                                                       #
#########################################################

"""
Estructura de cubo
cubo_sem[tipo1,tipo2,operador] = tipo-resultado

Tipos
    -1 - ERROR
    0 - INT
    1 - FLOAT
    2 - STRING
    3 - BOOL

Operador
	+      0
    -      1
	*      2
    /      3
	and    4
    or     5
	<      6
    >      7
    <=     8
    >=     9
    ==    10
    !=    11
    =     12

"""

#Cubo Semantico
cubo_sem={}

#Entero Entero
cubo_sem[0,0,0] =  0
cubo_sem[0,0,1] =  0
cubo_sem[0,0,2] =  0
cubo_sem[0,0,3] =  0
cubo_sem[0,0,4] = -1
cubo_sem[0,0,5] = -1
cubo_sem[0,0,6] =  3
cubo_sem[0,0,7] =  3
cubo_sem[0,0,8] =  3
cubo_sem[0,0,9] =  3
cubo_sem[0,0,10] = 3
cubo_sem[0,0,11] = 3
cubo_sem[0,0,12] = 0

#Entero Float
cubo_sem[0,1,0] = -1
cubo_sem[0,1,1] = -1
cubo_sem[0,1,2] = -1
cubo_sem[0,1,3] = -1
cubo_sem[0,1,4] = -1
cubo_sem[0,1,5] = -1
cubo_sem[0,1,6] =  3
cubo_sem[0,1,7] =  3
cubo_sem[0,1,8] =  3
cubo_sem[0,1,9] =  3
cubo_sem[0,1,10] = 3
cubo_sem[0,1,11] = 3
cubo_sem[0,1,12] = -1

#Entero String
cubo_sem[0,2,0] = -1
cubo_sem[0,2,1] = -1
cubo_sem[0,2,2] = -1
cubo_sem[0,2,3] = -1
cubo_sem[0,2,4] = -1
cubo_sem[0,2,5] = -1
cubo_sem[0,2,6] = -1
cubo_sem[0,2,7] = -1
cubo_sem[0,2,8] = -1
cubo_sem[0,2,9] = -1
cubo_sem[0,2,10] = -1
cubo_sem[0,2,11] = -1
cubo_sem[0,2,12] = -1

#Entero Bool
cubo_sem[0,3,0] = -1
cubo_sem[0,3,1] = -1
cubo_sem[0,3,2] = -1
cubo_sem[0,3,3] = -1
cubo_sem[0,3,4] = -1
cubo_sem[0,3,5] = -1
cubo_sem[0,3,6] = -1
cubo_sem[0,3,7] = -1
cubo_sem[0,3,8] = -1
cubo_sem[0,3,9] = -1
cubo_sem[0,3,10] = -1
cubo_sem[0,3,11] = -1
cubo_sem[0,3,12] = -1

#Float int
cubo_sem[1,0,0] = -1
cubo_sem[1,0,1] = -1
cubo_sem[1,0,2] = -1
cubo_sem[1,0,3] = -1
cubo_sem[1,0,4] = -1
cubo_sem[1,0,5] = -1
cubo_sem[1,0,6] =  3
cubo_sem[1,0,7] =  3
cubo_sem[1,0,8] =  3
cubo_sem[1,0,9] =  3
cubo_sem[1,0,10] = 3
cubo_sem[1,0,11] = 3
cubo_sem[1,0,12] = -1

#Float Float
cubo_sem[1,1,0] =  1
cubo_sem[1,1,1] =  1
cubo_sem[1,1,2] =  1
cubo_sem[1,1,3] =  1
cubo_sem[1,1,4] = -1
cubo_sem[1,1,5] = -1
cubo_sem[1,1,6] =  3
cubo_sem[1,1,7] =  3
cubo_sem[1,1,8] =  3
cubo_sem[1,1,9] =  3
cubo_sem[1,1,10] = 3
cubo_sem[1,1,11] = 3
cubo_sem[1,1,12] = 1

#Float String
cubo_sem[1,2,0] = -1
cubo_sem[1,2,1] = -1
cubo_sem[1,2,2] = -1
cubo_sem[1,2,3] = -1
cubo_sem[1,2,4] = -1
cubo_sem[1,2,5] = -1
cubo_sem[1,2,6] = -1
cubo_sem[1,2,7] = -1
cubo_sem[1,2,8] = -1
cubo_sem[1,2,9] = -1
cubo_sem[1,2,10] = -1
cubo_sem[1,2,11] = -1
cubo_sem[1,2,12] = -1

#Float Bool
cubo_sem[1,3,0] = -1
cubo_sem[1,3,1] = -1
cubo_sem[1,3,2] = -1
cubo_sem[1,3,3] = -1
cubo_sem[1,3,4] = -1
cubo_sem[1,3,5] = -1
cubo_sem[1,3,6] = -1
cubo_sem[1,3,7] = -1
cubo_sem[1,3,8] = -1
cubo_sem[1,3,9] = -1
cubo_sem[1,3,10] = -1
cubo_sem[1,3,11] = -1
cubo_sem[1,3,12] = -1

#String Int
cubo_sem[2,0,0] = -1
cubo_sem[2,0,1] = -1
cubo_sem[2,0,2] = -1
cubo_sem[2,0,3] = -1
cubo_sem[2,0,4] = -1
cubo_sem[2,0,5] = -1
cubo_sem[2,0,6] = -1
cubo_sem[2,0,7] = -1
cubo_sem[2,0,8] = -1
cubo_sem[2,0,9] = -1
cubo_sem[2,0,10] = -1
cubo_sem[2,0,11] = -1
cubo_sem[2,0,12] = -1

#String Float
cubo_sem[2,1,0] = -1
cubo_sem[2,1,1] = -1
cubo_sem[2,1,2] = -1
cubo_sem[2,1,3] = -1
cubo_sem[2,1,4] = -1
cubo_sem[2,1,5] = -1
cubo_sem[2,1,6] = -1
cubo_sem[2,1,7] = -1
cubo_sem[2,1,8] = -1
cubo_sem[2,1,9] = -1
cubo_sem[2,1,10] = -1
cubo_sem[2,1,11] = -1
cubo_sem[2,1,12] = -1

#String String
cubo_sem[2,2,0] =  2
cubo_sem[2,2,1] = -1
cubo_sem[2,2,2] = -1
cubo_sem[2,2,3] = -1
cubo_sem[2,2,4] = -1
cubo_sem[2,2,5] = -1
cubo_sem[2,2,6] =  3
cubo_sem[2,2,7] =  3
cubo_sem[2,2,8] =  3
cubo_sem[2,2,9] =  3
cubo_sem[2,2,10] = 3
cubo_sem[2,2,11] = 3
cubo_sem[2,2,12] = 2

#String Bool
cubo_sem[2,3,0] = -1
cubo_sem[2,3,1] = -1
cubo_sem[2,3,2] = -1
cubo_sem[2,3,3] = -1
cubo_sem[2,3,4] = -1
cubo_sem[2,3,5] = -1
cubo_sem[2,3,6] = -1
cubo_sem[2,3,7] = -1
cubo_sem[2,3,8] = -1
cubo_sem[2,3,9] = -1
cubo_sem[2,3,10] = -1
cubo_sem[2,3,11] = -1
cubo_sem[2,3,12] = -1

#Bool Int
cubo_sem[3,0,0] = -1
cubo_sem[3,0,1] = -1
cubo_sem[3,0,2] = -1
cubo_sem[3,0,3] = -1
cubo_sem[3,0,4] = -1
cubo_sem[3,0,5] = -1
cubo_sem[3,0,6] = -1
cubo_sem[3,0,7] = -1
cubo_sem[3,0,8] = -1
cubo_sem[3,0,9] = -1
cubo_sem[3,0,10] = -1
cubo_sem[3,0,11] = -1
cubo_sem[3,0,12] = -1

#Bool Float
cubo_sem[3,1,0] = -1
cubo_sem[3,1,1] = -1
cubo_sem[3,1,2] = -1
cubo_sem[3,1,3] = -1
cubo_sem[3,1,4] = -1
cubo_sem[3,1,5] = -1
cubo_sem[3,1,6] = -1
cubo_sem[3,1,7] = -1
cubo_sem[3,1,8] = -1
cubo_sem[3,1,9] = -1
cubo_sem[3,1,10] = -1
cubo_sem[3,1,11] = -1
cubo_sem[3,1,12] = -1

#Bool String
cubo_sem[3,2,0] = -1
cubo_sem[3,2,1] = -1
cubo_sem[3,2,2] = -1
cubo_sem[3,2,3] = -1
cubo_sem[3,2,4] = -1
cubo_sem[3,2,5] = -1
cubo_sem[3,2,6] = -1
cubo_sem[3,2,7] = -1
cubo_sem[3,2,8] = -1
cubo_sem[3,2,9] = -1
cubo_sem[3,2,10] = -1
cubo_sem[3,2,11] = -1
cubo_sem[3,2,12] = -1

#Bool Bool
cubo_sem[3,3,0] = -1
cubo_sem[3,3,1] = -1
cubo_sem[3,3,2] = -1
cubo_sem[3,3,3] = -1
cubo_sem[3,3,4] =  3
cubo_sem[3,3,5] =  3
cubo_sem[3,3,6] = -1
cubo_sem[3,3,7] = -1
cubo_sem[3,3,8] = -1
cubo_sem[3,3,9] = -1
cubo_sem[3,3,10] = 3
cubo_sem[3,3,11] = 3
cubo_sem[3,3,12] = 3

# Function to define the type of the result of a given operation
# Function recieves the operators and the operation
# Returns the type
def getResultType(operatorType1, operatorType2, operation):
	return cubo_sem[operatorType1, operatorType2, operation]