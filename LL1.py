import pandas as pd

# Clase para representar un nodo en la pila de análisis sintáctico
class NodoPila:
    def __init__(self, simbolo, lexema):
        global contador
        self.simbolo = simbolo
        self.lexema = lexema
        self.id = contador + 1
        contador += 1

# Clase para representar un nodo en el árbol de análisis sintáctico
class NodoArbol:
    def __init__(self, id, simbolo, lexema):
        self.id = id
        self.simbolo = simbolo
        self.lexema = lexema
        self.hijos = []
        self.padre = None

tabla = pd.read_csv("tabla.csv", index_col=0)

contador = 0

pila = []

# Inicializar la pila con símbolos iniciales (E y $)
simbolo_E = NodoPila('E', None)
simbolo_dolar = NodoPila('$', None)
pila.append(simbolo_dolar)
pila.append(simbolo_E)

# Inicializar un árbol sintáctico con la raíz
raiz = NodoArbol(simbolo_E.id, simbolo_E.simbolo, simbolo_E.lexema)

# Definir una lista de entrada para el análisis sintáctico
entrada = [ 
    {"simbolo":"int", "lexema":"4", "nroline":2, "col":2},
    {"simbolo":"+", "lexema":"+", "nroline":2, "col":4},
    {"simbolo":"int", "lexema":"5", "nroline":2, "col":6},
    {"simbolo":"$", "lexema":"$", "nroline":0, "col":0},
]

indice_entrada = 0

# Iniciar el bucle principal del análisis sintáctico
while len(pila) > 0:
    # Comprobar si el símbolo actual de entrada está en las columnas de la tabla
    if entrada[indice_entrada]["simbolo"] not in tabla.columns:
        print("Error de sintaxis")
        break 

    # Comprobar si el símbolo en la cima de la pila coincide con el símbolo de entrada actual
    if pila[-1].simbolo == entrada[indice_entrada]["simbolo"]:
        pila.pop()
        indice_entrada += 1
    else:
        # Si no hay una coincidencia directa, buscar una producción en la tabla
        produccion = tabla.loc[pila[-1].simbolo, entrada[indice_entrada]["simbolo"]]
        print(produccion)

        # Comprobar si la producción no es una producción nula ('e')
        if produccion != ('e'):
            pila.pop()
            
            # Procesar cada símbolo en la producción y agregarlo a la pila
            for simbolo in reversed(produccion.split()):
                nodo = NodoPila(simbolo, None)
                print ('produccion:', nodo.simbolo)
                print ('entrada actual', entrada[indice_entrada]["simbolo"])
                pila.append(nodo)
        else:
            pila.pop()

# Comprobar si la pila está vacía al final del análisis sintáctico
if len(pila) == 0:
    print("Análisis sintáctico exitoso")
else:
    print("Error de sintaxis")

# https://onlinegdb.com/VmW-GLWuv
