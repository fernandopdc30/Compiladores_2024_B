import pandas as pd
import json

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

# Leer la tabla de análisis sintáctico
tabla = pd.read_csv("tabla.csv", index_col=0)

# Leer el archivo de entrada desde un archivo JSON
with open("entrada1.txt", "r") as archivo:
    entrada = json.load(archivo)  # Convertir el archivo JSON a lista de diccionarios

contador = 0
pila = []

# Inicializar la pila con símbolos iniciales (E y $)
simbolo_E = NodoPila('E', None)
simbolo_dolar = NodoPila('$', None)
pila.append(simbolo_dolar)
pila.append(simbolo_E)

# Inicializar un árbol sintáctico con la raíz
raiz = NodoArbol(simbolo_E.id, simbolo_E.simbolo, simbolo_E.lexema)

indice_entrada = 0

# Iniciar el bucle principal del análisis sintáctico
while len(pila) > 0:
    # Comprobar si el símbolo actual de entrada está en las columnas de la tabla
    if entrada[indice_entrada]["simbolo"] not in tabla.columns:
        print("La tabla no reconoce esta producción")
        break 

    # Comprobar si el símbolo en la cima de la pila coincide con el símbolo de entrada actual
    if pila[-1].simbolo == entrada[indice_entrada]["simbolo"]:
        pila.pop()
        indice_entrada += 1
    else:
        try:
            # Intentar obtener la producción de la tabla
            produccion = tabla.loc[pila[-1].simbolo, entrada[indice_entrada]["simbolo"]]
            
            # Verificar si la producción es NaN (no existe en la tabla)
            if pd.isna(produccion):
                print("La tabla no reconoce esta producción")
                break
            
            # Comprobar si la producción no es una producción nula ('e')
            if produccion != 'e':
                pila.pop()
                
                # Procesar cada símbolo en la producción y agregarlo a la pila
                for simbolo in reversed(produccion.split()):
                    nodo = NodoPila(simbolo, None)
                    #print('produccion:', nodo.simbolo)
                    #print('entrada actual:', entrada[indice_entrada]["simbolo"])
                    pila.append(nodo)
            else:
                pila.pop()
        except KeyError:
            # Si ocurre un KeyError, significa que la producción no fue encontrada
            print("La tabla no reconoce esta producción")
            break

# Comprobar si la pila está vacía al final del análisis sintáctico
if len(pila) == 0:
    print("Análisis sintáctico exitoso")
else:
    print("Error de sintaxis")
    
#  https://onlinegdb.com/j8g5bibF7
