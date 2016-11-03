"""
MEMORIA

"""
class Memoria:
    def __init__(self):
        #DEFINICION DE ESPACIOS DE MEMORIA (llave direccion)
        #----------------
        # ESPACIOS
        #----------------
        #diccionario de enteros
        int_space = {}
        #diccionario de flotantes
        float_space = {}
        #diccionario de booleanas
        bool_space = {}
        #diccionario de strings
        string_space = {}

        #Diccionarios para mapear cte a memoria (invertidos) (llave valor)
        #-----------------------
        # Diccionarios INVERSOS
        #-----------------------
        #diccionario invertido para ctes enteras
        inv_cte_int = {}

        #diccionario invertido para ctes flotantes
        inv_cte_float = {}

        #Hardcode porque son 2 valores
        inv_cte_bool = {True:2000, False:2001}

        #DEFINICION de rangos de tamaño de memoria
        #-----------------
        # RANGOS
        #----------------
        #rango globales
        global_range = [(0,99),()
        #rango locales
        local_range = (100,399)
        #rango temporales
        temp_range = (400,1999)
        #rango cte's enteras
        cte_int_range = (2000,2199)
        #rango cte floats
        cte_float_range = (2000,2199)
        #rango cte bool
        cte_bool_range = (2000,2001)
        """
        HACK DE LISTA PARA SIMULAR POINTER
        El index tiene que estar en una lista para tener la referencia al index
        La funcion que regresa el index (getMemIndex) le regresa la referencia
        a la variable que recibe el valor de retorno (memIndex). memIndex
        modifica este valor accesando la lista con memIndex[0] y despues haciendo
        la operacion. Esto simula un pointer.
        """
        #Definicion de indices para el manejo de los espacios de memoria
        #----------------
        # INDEX ENTERAS
        #----------------
        """
            Rango de espacios para las ints va de la 100
        """
        #index para globales enteras
        index_gint = [global_range[0] + 10000]
        #index para locales enteras
        index_lint = [local_range[0] + 10000]
        #index para temporales enteras
        index_tint = [temp_range[0] + 10000]
        #index para ctes enteras
        index_cint = [cte_int_range[0] + 10000]

        #-----------------
        # INDEX FLOAT
        #-----------------
        #index para globales flotantes
        index_gfloat = [global_range[0]]
        #index para locales flotantes
        index_lfloat = [local_range[0]]
        #index para temporales flotantes
        index_tfloat = [temp_range[0]]
        #index para ctes flotantes
        index_cfloat = [cte_float_range[0]]

        #------------------
        #INDEX BOOL
        #------------------
        #index para globales bool
        index_gbool = [global_range[0]]
        #index para locales bool
        index_lbool = [local_range[0]]
        #index para temporales bool
        index_tbool = [temp_range[0]]

        #-------------------
        # INDEX STRING
        #-------------------
        #index para globales string
        index_gstring = [global_range[0]]
        #index para locales string
        index_lstring = [local_range[0]]
        #index para temporales string
        index_tstring = [temp_range[0]]

    #Metodo para obtener el index apropiado para el tipo de memoria
    #(global,local,temporal,cte) a partir del scope
    def getMemIndex(scope,tipo):
        #tipo es entero
        if tipo == 0:
            #si el scope es global
            if (scope==0):
                return index_gint
            #si el scope es local
        elif (scope==1):
                return index_lint
            #si el scope es temporal
        elif (scope == 2):
                return index_tint
            #si el scope es cte
        elif (scope == 3):
                return index_cint
            else:
                print("Error: Segmentation fault")
                exit(1)
        #tipo es flotante
        elif tipo == 1:
            #si el scope es global
            if (scope==0):
                return index_gfloat
            #si el scope es local
        elif (scope==1):
                return index_lfloat
            #si el scope es temporal
        elif (scope == 2):
                return index_tfloat
            #si el scope es cte
        elif (scope == 3):
                return index_cfloat
            else:
                print("Error: Segmentation fault")
                exit(1)
        #tipo es string
        elif tipo == 2:
            #si el scope es global
            if (scope==0):
                return index_gstring
            #si el scope es local
        elif (scope==1):
                return index_lstring
            #si el scope es temporal
        elif (scope == 2):
                return index_tstring
            else:
                print("Error: Segmentation fault")
                exit(1)
        #tipo es bool
        elif tipo == 3:
            #si el scope es global
            if (scope==0):
                return index_gbool
            #si el scope es local
        elif (scope==1):
                return index_lbool
            #si el scope es temporal
        elif (scope == 2):
                return index_tbool
            else:
                print("Error: Segmentation fault")
                exit(1)
        #tipo incorrecto
        else:
            print("Error: Type not defined")
            exit(1)


    #Metodo para agregar memoria
    def agregaMemoria(tipo, scope, valor):

    #Metodo para borrar memoria param1:tuple -> rango, param2:int
    def borrarMemoria(rango,tipo):
        #Obtener el index apropiado
        memIndex = getMemIndex(rango,tipo)
        #condiciones para checar de que espacio de memoria se borrara (int,float,bool,string)
        #Si el tipo es entero
        if tipo == 0:
            #hack de lista
            memIndex[0] = rango[0]
            #i = inicio del rango
            i = rango[0]
            while(i < rango[1]):
                del int_space[i]
                i += 1

        #si el tipo es flotante
        elif tipo == 1:
            #hack de lista
            memIndex[0] = rango[0]
            #i = inicio del rango
            i = rango[0]
            while(i < rango[1]):
                del float_space[i]
                i += 1

        #si el tipo es string
        elif tipo == 2:
            #hack de lista
            memIndex[0] = rango[0]
            #i = inicio del rango
            i = rango[0]
            while(i < rango[1]):
                del string_space[i]
                i += 1

        #si el tipo es bool
        elif tipo == 3:
            #hack de lista
            memIndex[0] = rango[0]
            #i = inicio del rango
            i = rango[0]
            while(i < rango[1]):
                del bool_space[i]
                i += 1
