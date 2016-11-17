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
		self.returnAddress = None
		self.memory = [[None]] * 4
		count = 0
		for i in range(0, 4):
			if SubTypeQty[i] != 0:
				self.memory[count] = [None] * SubTypeQty[i]
			count += 1

	def __del__(self):
		class_name = self.__class__.__name__