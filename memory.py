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
		self.memory = [[None]] * TotalTypes
		print(self.memory)
		count = 0
		for i in range(0, 4):
			if SubTypeQty[i] != 0:
				self.memory[count] = [None for y in range(0, SubTypeQty[i])]
				count += 1

	def __del__(self):
		class_name = self.__class__.__name__