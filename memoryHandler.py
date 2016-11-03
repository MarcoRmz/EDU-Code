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
currentLocalVirtualAddress = [10000, 20000, 30000, 40000]

# Parse Virtual Address to Real Address
# Global
# type = virtual // 1000
# realAddr = virtual % 1000

# Constants
# type = (virtual // 1000) - 4
# realAddr = virtual % 1000

# Local
# type = (virtual // 10000) - 1
# realAddr = virtual % 10000