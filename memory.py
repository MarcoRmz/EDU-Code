#########################################################
#														#
# 	memory.py											#
#														#
# 	Memory Object										#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581		   				#
#														#
#########################################################

class Memory:
	def __init__(self, SubTypeQty):
		# Return address used for functions that return a value
		self.returnAddress = None
		
		# Initializes the memory with a list for each type
		# [[INTs], [FLOATs], [STRINGs], [BOOLs]]
		self.memory = [[None]] * 4
		
		# Adds a space for each variable used in its corresponding type
		count = 0
		for i in range(0, 4):
			if SubTypeQty[i] != 0:
				self.memory[count] = [None] * SubTypeQty[i]
			count += 1

	def __del__(self):
		class_name = self.__class__.__name__