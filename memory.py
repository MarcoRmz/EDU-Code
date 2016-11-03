#########################################################
#														#
# 	memory.py											#
#														#
# 	Memory Object										#
#														#
# 	Marco Ramirez 		A01191344						#
# 	Andres Gutierrez	A01191581       				#
#														#
#########################################################

class Memory:
	def __init__(self, TotalTypes, SubTypeQty):
		self.returnAddress = None
		self.memory = [[None] * TotalTypes]
		for i in range(0, SubTypeQty):
			self.memory[i] = [None for x in range(0, SubTypeQty[i])]

	def __del__(self):
		class_name = self.__class__.__name__