
#########################################################
#                                                       #
#   maquina.py                                          #
#                                                       #
#   Maquina Virtual                                     #
#                                                       #
#   Marco Ramirez       A01191344                       #
#   Andres Gutierrez    A01191581                       #
#                                                       #
#########################################################

from memoryHandler import *
from cuadruplos import *


#Count variable for quadruples
i = 0

executionStack = []

#While the quadruple holds no EOF operation
while(cuadruplos.dirCuadruplos[i][0] != 99):
#conditions to determine actions on quadruples
    #case for PLUS (+)
    if(cuadruplos.dirCuadruplos[i][0] == 0):
        #get operands from the memory
        operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
        operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

        #apply sum operation to operands
        result = operand1 + operand2

        #save the new value for the specified address
        memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

        i += 1

        #case for MINUS (-)
    elif(cuadruplos.dirCuadruplos[i][0] == 1):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
                operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

                #apply substraction operation to operands
                result = operand1 - operand2

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

                i += 1

        #case for MULT (*)
    elif(cuadruplos.dirCuadruplos[i][0] == 2):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
                operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

                #apply multiplication operation to operands
                result = operand1 * operand2

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

                i += 1

        #case for DIVIDE (/)
    elif(cuadruplos.dirCuadruplos[i][0] == 3):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
                operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

                #apply divide operation to operands
                result = operand1 / operand2

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

                i += 1

        #case for AND
    elif(cuadruplos.dirCuadruplos[i][0] == 4):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
                operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

                #apply and operation to operands
                result = operand1 and operand2

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

                i += 1
        #case for OR
    elif(cuadruplos.dirCuadruplos[i][0] == 5):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
                operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

                #apply or operation to operands
                result = operand1 or operand2

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

                i += 1

        #case for LESS than (<)
    elif(cuadruplos.dirCuadruplos[i][0] == 6):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            #apply less than to operands
            result = operand1 < operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1

        #case for  GREATER than (>)
    elif(cuadruplos.dirCuadruplos[i][0] == 7):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            #apply greater than to operands
            result = operand1 > operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1

        #case for LESS THAN OR EQUALS (<=)
    elif(cuadruplos.dirCuadruplos[i][0] == 8):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            ##apply less than equals to operands
            result = operand1 <= operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1
        #case for GREATER THAN OR EQUALS (>=)
    elif(cuadruplos.dirCuadruplos[i][0] == 9):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            #apply greater than equals to operands
            result = operand1 >= operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1

        #case for DOUBLE EQUALS (==)
    elif(cuadruplos.dirCuadruplos[i][0] == 10):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            #apply double equals to operands
            result = operand1 == operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1
        #case for DIFFERENT (!=)
    elif(cuadruplos.dirCuadruplos[i][0] == 11):
            #get operands from the memory
            operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])
            operand2 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][2])

            #apply not equals to operands
            result = operand1 != operand2

            #save the new value for the specified address
            memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],result)

            i += 1
        #case for EQUALS (=)
    elif(cuadruplos.dirCuadruplos[i][0] == 12):
                #get operands from the memory
                operand1 = memoryHandler.getValue(cuadruplos.dirCuadruplos[i][1])

                #save the new value for the specified address
                memoryHandler.setValue(cuadruplos.dirCuadruplos[i][3],operand1)

                i += 1

        #case for GOTO
    elif(cuadruplos.dirCuadruplos[i][0] == 13):
        #obtain the index of the quadruple and jump to it
        i = cuadruplos.dirCuadruplos[i][3]

        #case for GOTOF
    elif(cuadruplos.dirCuadruplos[i][0] == 14):
        #if the temporal is false jump to the specified quadruple
        if(cuadruplos.dirCuadruplos[i][1] == False):
            i = cuadruplos.dirCuadruplos[i][3]

        #case for GOTOT
    elif(cuadruplos.dirCuadruplos[i][0] == 15):
        #if the temporal holds a True jump to the specified quadruple
        if(cuadruplos.dirCuadruplos[i][1] == True):
            i = cuadruplos.dirCuadruplos[i][3]

        #case for GOSUB
    elif(cuadruplos.dirCuadruplos[i][0] == 16):
        #append next quadruple to the executionStack
        executionStack.append(i+1)

        #jump to function quadruple
        i = cuadruplos.dirCuadruplos[i][3]


        #case for RETURN
    elif(cuadruplos.dirCuadruplos[i][0] == 17):

        #get return value from quadruple
        rtn = memoryHandler.memoryStack[-1].returnAddress
        rtn_value = memoryHandler.getValue(cuadruplos.dirCuadruplos[1])

        #assign return value to the return address of the function
        memoryHandler.delete()

        memoryHandler.setValue(rtn, rtn_value)

        #case for PRINT
    elif(cuadruplos.dirCuadruplos[i][0] == 18):

        #case for INPUT
    elif(cuadruplos.dirCuadruplos[i][0] == 19):

        #case for ERA
    elif(cuadruplos.dirCuadruplos[i][0] == 20):

        #creates memory for a specific function createMemory(TotalTypes,SubTypeQty,returnAddress)
        memoryHandler.createMemory(cuadruplos.dirCuadruplos[i][1],cuadruplos.dirCuadruplos[i][2])
        #assigns return address to memory
        memoryHandler.memoryStack[-1].returnAddress = cuadruplos.dirCuadruplos[i][3]

        #case for ENDPROC
    elif(cuadruplos.dirCuadruplos[i][0] == 21):
        #Returns to the next instruction after the function call
        i = executionStack.pop()

        #case for PARAM
    elif(cuadruplos.dirCuadruplos[i][0] == 22):
        #get param types
        param_type = cuadruplos.dirCuadruplos[i][1]
        #get param virtual memory addresses
        param_vaddress = cuadruplos.dirCuadruplos[i][2]


        param_realAddr = param_vaddress % 1000
        #gets value from previous function (memory object)
        paramValue = memoryHandler.memoryStack[-2].memory[param_type][param_realAddr]
        #gets real address
        realAddr = cuadruplos.dirCuadruplos[i][3]
        #assigns paramValue to corresponding memory address
        memoryHandler.memoryStack[-1].memory[param_type][realAddr] = paramValue
