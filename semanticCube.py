#########################################################
#														#
# 	semanticCube.py	 									#
#														#
# 	Semantic Cube										#
#														#
# 	Marco Ramirez		A01191344						#
# 	Andres Gutierrez	A01191581						#
#														#
#########################################################

"""
Cube structure
semanticCube[operand1, operand2, operator] = result-type

Types
	-1	: ERROR
	0	: INT
	1	: FLOAT
	2	: STRING
	3	: BOOL

Operatos
	+	 :	0
	-	 :	1
	*	 :	2
	/	 :	3
	and	 :	4
	or	 :	5
	<	 :	6
	>	 :	7
	<=	 :	8
	>=	 :	9
	==	 :	10
	!=	 :	11
	=	 :	12
"""

#Semantic Cube var initialized
semanticCube={}

#########################################
#										#
#	Valid operations for INT & INT		#
#										#
#########################################
semanticCube[0,0,0] =0
semanticCube[0,0,1] =0
semanticCube[0,0,2] =0
semanticCube[0,0,3] =0
semanticCube[0,0,4] = -1
semanticCube[0,0,5] = -1
semanticCube[0,0,6] =3
semanticCube[0,0,7] =3
semanticCube[0,0,8] =3
semanticCube[0,0,9] =3
semanticCube[0,0,10] = 3
semanticCube[0,0,11] = 3
semanticCube[0,0,12] = 0

#########################################
#										#
#	Valid operations for INT & FLOAT	#
#										#
#########################################
semanticCube[0,1,0] = -1
semanticCube[0,1,1] = -1
semanticCube[0,1,2] = -1
semanticCube[0,1,3] = -1
semanticCube[0,1,4] = -1
semanticCube[0,1,5] = -1
semanticCube[0,1,6] =3
semanticCube[0,1,7] =3
semanticCube[0,1,8] =3
semanticCube[0,1,9] =3
semanticCube[0,1,10] = 3
semanticCube[0,1,11] = 3
semanticCube[0,1,12] = -1

#########################################
#										#
#	Valid operations for INT & STRING	#
#										#
#########################################
semanticCube[0,2,0] = -1
semanticCube[0,2,1] = -1
semanticCube[0,2,2] = -1
semanticCube[0,2,3] = -1
semanticCube[0,2,4] = -1
semanticCube[0,2,5] = -1
semanticCube[0,2,6] = -1
semanticCube[0,2,7] = -1
semanticCube[0,2,8] = -1
semanticCube[0,2,9] = -1
semanticCube[0,2,10] = -1
semanticCube[0,2,11] = -1
semanticCube[0,2,12] = -1

#########################################
#										#
#	Valid operations for INT & BOOL		#
#										#
#########################################
semanticCube[0,3,0] = -1
semanticCube[0,3,1] = -1
semanticCube[0,3,2] = -1
semanticCube[0,3,3] = -1
semanticCube[0,3,4] = -1
semanticCube[0,3,5] = -1
semanticCube[0,3,6] = -1
semanticCube[0,3,7] = -1
semanticCube[0,3,8] = -1
semanticCube[0,3,9] = -1
semanticCube[0,3,10] = -1
semanticCube[0,3,11] = -1
semanticCube[0,3,12] = -1

#########################################
#										#
#	Valid operations for FLOAT & INT	#
#										#
#########################################
semanticCube[1,0,0] = -1
semanticCube[1,0,1] = -1
semanticCube[1,0,2] = -1
semanticCube[1,0,3] = -1
semanticCube[1,0,4] = -1
semanticCube[1,0,5] = -1
semanticCube[1,0,6] =3
semanticCube[1,0,7] =3
semanticCube[1,0,8] =3
semanticCube[1,0,9] =3
semanticCube[1,0,10] = 3
semanticCube[1,0,11] = 3
semanticCube[1,0,12] = -1

#########################################
#										#
#	Valid operations for FLOAT & FLOAT	#
#										#
#########################################
semanticCube[1,1,0] =1
semanticCube[1,1,1] =1
semanticCube[1,1,2] =1
semanticCube[1,1,3] =1
semanticCube[1,1,4] = -1
semanticCube[1,1,5] = -1
semanticCube[1,1,6] =3
semanticCube[1,1,7] =3
semanticCube[1,1,8] =3
semanticCube[1,1,9] =3
semanticCube[1,1,10] = 3
semanticCube[1,1,11] = 3
semanticCube[1,1,12] = 1

#########################################
#										#
#	Valid operations for FLOAT & STRING	#
#										#
#########################################
semanticCube[1,2,0] = -1
semanticCube[1,2,1] = -1
semanticCube[1,2,2] = -1
semanticCube[1,2,3] = -1
semanticCube[1,2,4] = -1
semanticCube[1,2,5] = -1
semanticCube[1,2,6] = -1
semanticCube[1,2,7] = -1
semanticCube[1,2,8] = -1
semanticCube[1,2,9] = -1
semanticCube[1,2,10] = -1
semanticCube[1,2,11] = -1
semanticCube[1,2,12] = -1

#########################################
#										#
#	Valid operations for FLOAT & BOOL	#
#										#
#########################################
semanticCube[1,3,0] = -1
semanticCube[1,3,1] = -1
semanticCube[1,3,2] = -1
semanticCube[1,3,3] = -1
semanticCube[1,3,4] = -1
semanticCube[1,3,5] = -1
semanticCube[1,3,6] = -1
semanticCube[1,3,7] = -1
semanticCube[1,3,8] = -1
semanticCube[1,3,9] = -1
semanticCube[1,3,10] = -1
semanticCube[1,3,11] = -1
semanticCube[1,3,12] = -1

#########################################
#										#
#	Valid operations for STRING	& INT	#
#										#
#########################################
semanticCube[2,0,0] = -1
semanticCube[2,0,1] = -1
semanticCube[2,0,2] = -1
semanticCube[2,0,3] = -1
semanticCube[2,0,4] = -1
semanticCube[2,0,5] = -1
semanticCube[2,0,6] = -1
semanticCube[2,0,7] = -1
semanticCube[2,0,8] = -1
semanticCube[2,0,9] = -1
semanticCube[2,0,10] = -1
semanticCube[2,0,11] = -1
semanticCube[2,0,12] = -1

#########################################
#										#
#	Valid operations for STRING	& FLOAT	#
#										#
#########################################
semanticCube[2,1,0] = -1
semanticCube[2,1,1] = -1
semanticCube[2,1,2] = -1
semanticCube[2,1,3] = -1
semanticCube[2,1,4] = -1
semanticCube[2,1,5] = -1
semanticCube[2,1,6] = -1
semanticCube[2,1,7] = -1
semanticCube[2,1,8] = -1
semanticCube[2,1,9] = -1
semanticCube[2,1,10] = -1
semanticCube[2,1,11] = -1
semanticCube[2,1,12] = -1

#########################################
#										#
#	Valid operations for STRING	& STRING#
#										#
#########################################
semanticCube[2,2,0] = 2
semanticCube[2,2,1] = -1
semanticCube[2,2,2] = -1
semanticCube[2,2,3] = -1
semanticCube[2,2,4] = -1
semanticCube[2,2,5] = -1
semanticCube[2,2,6] = 3
semanticCube[2,2,7] = 3
semanticCube[2,2,8] = 3
semanticCube[2,2,9] = 3
semanticCube[2,2,10] = 3
semanticCube[2,2,11] = 3
semanticCube[2,2,12] = 2

#########################################
#										#
#	Valid operations for STRING	& BOOL	#
#										#
#########################################
semanticCube[2,3,0] = -1
semanticCube[2,3,1] = -1
semanticCube[2,3,2] = -1
semanticCube[2,3,3] = -1
semanticCube[2,3,4] = -1
semanticCube[2,3,5] = -1
semanticCube[2,3,6] = -1
semanticCube[2,3,7] = -1
semanticCube[2,3,8] = -1
semanticCube[2,3,9] = -1
semanticCube[2,3,10] = -1
semanticCube[2,3,11] = -1
semanticCube[2,3,12] = -1

#########################################
#										#
#	Valid operations for BOOL & INT		#
#										#
#########################################
semanticCube[3,0,0] = -1
semanticCube[3,0,1] = -1
semanticCube[3,0,2] = -1
semanticCube[3,0,3] = -1
semanticCube[3,0,4] = -1
semanticCube[3,0,5] = -1
semanticCube[3,0,6] = -1
semanticCube[3,0,7] = -1
semanticCube[3,0,8] = -1
semanticCube[3,0,9] = -1
semanticCube[3,0,10] = -1
semanticCube[3,0,11] = -1
semanticCube[3,0,12] = -1

#########################################
#										#
#	Valid operations for BOOL & FLOAT	#
#										#
#########################################
semanticCube[3,1,0] = -1
semanticCube[3,1,1] = -1
semanticCube[3,1,2] = -1
semanticCube[3,1,3] = -1
semanticCube[3,1,4] = -1
semanticCube[3,1,5] = -1
semanticCube[3,1,6] = -1
semanticCube[3,1,7] = -1
semanticCube[3,1,8] = -1
semanticCube[3,1,9] = -1
semanticCube[3,1,10] = -1
semanticCube[3,1,11] = -1
semanticCube[3,1,12] = -1

#########################################
#										#
#	Valid operations for BOOL & STRING	#
#										#
#########################################
semanticCube[3,2,0] = -1
semanticCube[3,2,1] = -1
semanticCube[3,2,2] = -1
semanticCube[3,2,3] = -1
semanticCube[3,2,4] = -1
semanticCube[3,2,5] = -1
semanticCube[3,2,6] = -1
semanticCube[3,2,7] = -1
semanticCube[3,2,8] = -1
semanticCube[3,2,9] = -1
semanticCube[3,2,10] = -1
semanticCube[3,2,11] = -1
semanticCube[3,2,12] = -1

#########################################
#										#
#	Valid operations for BOOL & BOOL	#
#										#
#########################################
semanticCube[3,3,0] = -1
semanticCube[3,3,1] = -1
semanticCube[3,3,2] = -1
semanticCube[3,3,3] = -1
semanticCube[3,3,4] = 3
semanticCube[3,3,5] = 3
semanticCube[3,3,6] = -1
semanticCube[3,3,7] = -1
semanticCube[3,3,8] = -1
semanticCube[3,3,9] = -1
semanticCube[3,3,10] = 3
semanticCube[3,3,11] = 3
semanticCube[3,3,12] = 3

# Function to define the type of the result of a given operation
# Function recieves the operators and the operation
# Returns the type
def getResultType(operatorType1, operatorType2, operation):
	return semanticCube[operatorType1, operatorType2, operation]
