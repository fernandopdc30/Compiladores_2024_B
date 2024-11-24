import pandas as pd
import lexico
import os

class node_stack:
    def __init__(self, symbol, lexeme):
        global count
        self.symbol = symbol
        self.lexeme = lexeme
        self.id = count
        count += 1

class node_tree:
    def __init__(self, id, symbol, lexeme):
        self.id = id
        self.symbol = symbol
        self.lexeme = lexeme
        self.children = []
        self.father = None

# Función para buscar un nodo en el árbol
def buscar_nodo(raiz, id): 
    if raiz.id == id:
        return raiz
    else:
        for hijo in raiz.children:
            resultado = buscar_nodo(hijo, id)
            if resultado is not None:
                return resultado
        return None

# Mostrar el directorio actual
#print("Directorio actual antes de cambiar:", os.getcwd())

# Cambiar al directorio del script
os.chdir(os.path.dirname(__file__))
#print("Nuevo directorio actual:", os.getcwd())

# Listar archivos en el directorio actual
#print("Archivos en el directorio actual:", os.listdir())

tabla = pd.read_csv("tablaV3.csv", index_col=0)
#print("Archivo leído correctamente.")

count = 0
stack = []


# Inicializar la pila con símbolos de inicio y fin
symbol_E = node_stack('INICIO', None)
symbol_dollar = node_stack('$', None)
stack.append(symbol_dollar)
stack.append(symbol_E)

# Configurar el árbol con el símbolo de inicio
root = node_tree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme)

entrada = lexico.lexico('ejemplo_tipos.txt')
#print(entrada)
index_entrada = 0

while len(stack) > 1:
    simbolo_entrada = entrada[index_entrada]["simbolo"]
    # Comparar la cima de la pila con el símbolo de entrada
    if stack[-1].symbol == simbolo_entrada:
        # Recuperamos el lexema.
        nodoActual = buscar_nodo(root, stack[-1].id)
        nodoActual.lexeme = entrada[index_entrada]["lexema"]
        
        print("Terminal:", stack[-1].symbol)
        stack.pop()
        index_entrada += 1
    else:
        if (stack[-1].symbol not in tabla.index
          or simbolo_entrada not in tabla.columns):
            print("-----------------Error en el proceso sintáctico1-----------------")
            print("ERROR CERCA A: ", entrada[index_entrada]["lexema"], "           En la linea: ", entrada[index_entrada]["nroline"])
            break
        # Obtener la producción de la tabla de análisis
        produccion = tabla.loc[stack[-1].symbol, simbolo_entrada]
        # Manejar errores de sintaxis
        if isinstance(produccion, float):
            print("-----------------Error en el proceso sintáctico2-----------------")
            print("ERROR CERCA A: ", entrada[index_entrada]["lexema"], "           En la linea: ", entrada[index_entrada]["nroline"])
            break

        # Aplicar la producción en la pila y el árbol
        if produccion != 'e':
            #print("Pila antes de aplicar producción:", [n.symbol for n in stack])
            #print("Producción:", produccion)
            #padre = buscar_nodo(stack[-1].id, root)
            node_x=stack.pop()
            for simbolo in reversed(str(produccion).split()):
                nodo_p = node_stack(simbolo, None)
                stack.append(nodo_p)
                hijo = node_tree(nodo_p.id, nodo_p.symbol, nodo_p.lexeme)  # Utiliza el lexema
                node_father = buscar_nodo(root, node_x.id)
                node_father.children.append(hijo)
                hijo.father = node_father
            print("Pila después de aplicar producción:", [n.symbol for n in stack])
        else:
            print("Pila antes de eliminar símbolo epsilon:", [n.symbol for n in stack])
            stack.pop()
            print("Pila después de eliminar símbolo epsilon:", [n.symbol for n in stack])


nombre_archivo = "arbol.txt"
archivo = open(nombre_archivo, "w")

def imprimir(nodo, padre=None):
    if nodo is not None:
        # Llama recursivamente para procesar los hijos primero
        for hijo in reversed(nodo.children):
            imprimir(hijo, nodo)

        # Determinar si el nodo es una hoja (no tiene hijos)
        es_hoja = len(nodo.children) == 0

        # Asignar colores según la posición del nodo
        if es_hoja:
            color = "yellow"  # Nodos finales (hojas)
        elif padre is None:
            color = "skyblue"  # Nodo raíz
        else:
            color = "white"  # Nodos intermedios

        # Crear el label del nodo con su información
        label = f"<Symbol: {nodo.symbol}<BR/>Lexeme: '{nodo.lexeme}'>"

        # Escribir el nodo al archivo con su color
        archivo.write(f"{nodo.id} [style = filled fillcolor= {color} label = {label}]\n")

        # Si tiene padre, escribir la conexión
        if padre is not None:
            archivo.write(f"{padre.id} -> {nodo.id}\n")


if stack[-1].symbol == "$":
    print("\033[92mAnalisador Sintactico: CORRECTO\n\n\033[0m")


stack2 = []
# Funcion para registrar funciones en la tabla de simbolos
def registrar_funciones(nodo):
    if nodo is not None and nodo.symbol == "IDENTIFICADOR" and nodo.father.symbol == "FUNC":
        # Verificar si el nodo tiene al menos tres hijos
        ID= nodo.id 
        tipo_dato = "dinamico"
        nombre_funcion = nodo.lexeme 
        ambito = "global"
        codigo_flag = "FUNCION"
        stack2.append({
            "ID": ID,
            "tipo_dato": tipo_dato,
            "nombre_funcion": nombre_funcion,
            "ambito": ambito,
            "codigo_flag": codigo_flag
        })
    elif nodo is not None and nodo.symbol == "IDENTIFICADOR" and nodo.father.symbol == "PARAMETRO":
        # Verificar si el nodo tiene al menos tres hijos
        ID= nodo.id 
        tipo_dato = nodo.father.children[-1].children[-1].lexeme
        nombre_funcion = nodo.lexeme 
        ambito = "funcion"
        codigo_flag = "variable"
        stack2.append({
            "ID": ID,
            "tipo_dato": tipo_dato,
            "nombre_funcion": nombre_funcion,
            "ambito": ambito,
            "codigo_flag": codigo_flag
        })

    for hijo in nodo.children:
        registrar_funciones(hijo)



tipo_actual = ''

# Funcion para registrar variables en la tabla de simbolos
global ambit
ambit = "global"
def registrar_VARIABLES(nodo): 
    global ambit, tipo_actual
    if nodo.symbol == "REGRESA":
        ambit = "funcion"
    if nodo is not None and nodo.symbol == "IDENTIFICADOR" and nodo.father.symbol == "DECLARACION":
        # Verificar si el nodo tiene al menos tres hijos

        ID= nodo.id 
        tipo_dato = nodo.father.children[-1].children[-1].symbol 
        nombre_variable = nodo.lexeme 
        ambito = ambit
        codigo_flag = "VARIABLE"
        stack2.append({
            "ID": ID,
            "tipo_dato": tipo_dato,
            "nombre_variable": nombre_variable,
            "ambito": ambito,
            "codigo_flag": codigo_flag
        })
        
    for hijo in nodo.children:
        registrar_VARIABLES(hijo)

# Verifica la compatibilidad de tipo: entero a = 12 + 123 + 2.1
def semantico(nodo):
    global stack2, tipo_actual
    if nodo is not None and nodo.symbol == "IDENTIFICADOR" and nodo.father.symbol == "DECLARACION":
        # Verificar si el nodo tiene al menos tres hijos
        nombre_variable = nodo.lexeme 
        tipo_dato = nodo.father.children[-1].children[-1].symbol 
        
        if tipo_dato == 'DATO_ENTERO':
            tipo_dato = 'NUM_ENTERO'
        elif tipo_dato == 'DATO_CARACTER':
            tipo_dato = 'CADENA_TEXTO'
        elif tipo_dato == 'DATO_DECIMAL':
                tipo_dato = 'NUM_DECIMAL'

        print("Tipo inicial: ", nodo.father.children[0].children[0].children[-1].children[-1].symbol)
        tipo_actual = nodo.father.children[0].children[0].children[-1].children[-1].symbol
        if tipo_actual == "IDENTIFICADOR":
            print("Hola")
            tipo_actual = recuperar_tipo_dato_por_nombre_variable(stack2, nombre_variable)
            if tipo_actual == 'DATO_ENTERO':
                tipo_actual = 'NUM_ENTERO'
            elif tipo_actual == 'DATO_CARACTER':
                tipo_actual = 'CADENA_TEXTO'
            elif tipo_actual == 'DATO_DECIMAL':
                tipo_actual = 'NUM_DECIMAL'

        if definirTipo(tipo_dato, tipo_actual) is None :
            print(f"Error de tipo: No se puede asignar {tipo_actual} con {tipo_dato}.")
            exit(1)

        tipo_actual = definirTipo(tipo_dato, tipo_actual)

        
        print("NODO MANDADO:", nodo.father.children[0].children[0].children[0].symbol)
        verificar_tipos(nodo.father.children[0].children[0].children[0])
        print("Nuevo Tipo:", tipo_actual)
    for hijo in nodo.children:
        semantico(hijo)

def verificar_tipos(nodo):
    global tipo_actual
    global stack2
    if nodo is not None:
        # Verificar si el nodo es una operación binaria
        if nodo.symbol in ["OP_SUMA", "OP_RESTA", "OP_MULTIPLICACION", "OP_DIVISION"]:
            tipo_propuesto = nodo.father.children[1].children[-1].symbol
            #
            if tipo_propuesto == "IDENTIFICADOR":
                #print("Hola", nodo.father.children[1].children[-1].lexeme)
                tipo_propuesto = recuperar_tipo_dato_por_nombre_variable(stack2, nodo.father.children[1].children[-1].lexeme)
                if tipo_propuesto == 'DATO_ENTERO':
                    tipo_propuesto = 'NUM_ENTERO'
                elif tipo_propuesto == 'DATO_CARACTER':
                    tipo_propuesto = 'CADENA_TEXTO'
                elif tipo_propuesto == 'DATO_DECIMAL':
                    tipo_propuesto = 'NUM_DECIMAL'

            
            print("TIPO PROPUESTO", tipo_propuesto)
            if tipo_resultante(tipo_actual, tipo_propuesto, nodo.symbol) is None:
                print(f"Error semantico: No se puede operar {tipo_actual} con {tipo_propuesto}.")
                exit(1)
            tipo_actual = tipo_resultante(tipo_actual, tipo_propuesto, nodo.symbol)
        # Verificar recursivamente en los hijos
        for hijo in nodo.children:
            verificar_tipos(hijo)

def recuperar_tipo_dato_por_nombre_variable(stack2, nombre_variable_buscado):
    #print("HOLA", stack2)
    for elemento in stack2:
        if elemento["nombre_variable"] == nombre_variable_buscado:
            return elemento["tipo_dato"]
    return None

#---------------------------------
# Definición de subtipos de datos
subtipos = {
    "NUM_BOOLEANOF": [],
    "NUM_BOOLEANOV": ["NUM_ENTERO"],
    "NUM_ENTERO": ["NUM_BOOLEANOF"],
    "CADENA_TEXTO": [],
    "NUM_DECIMAL": ['NUM_ENTERO']
}

# Función para definir el tipo resultante de dos tipos
def definirTipo(tipo1, tipo2):
    if tipo1 == tipo2:
        return tipo1

    def buscar_subtipo(tipo_actual, tipo_objetivo):
        if tipo_actual == tipo_objetivo:
            return True
        for subtipo in subtipos.get(tipo_actual, []):
            if buscar_subtipo(subtipo, tipo_objetivo):
                return True
        return False

    if buscar_subtipo(tipo1, tipo2):
        return tipo1

    if buscar_subtipo(tipo2, tipo1):
        return tipo2
    return None

# Función para determinar el tipo resultante de una operación
def tipo_resultante(tipo1, tipo2, operador):
    TipoFinal = definirTipo(tipo1, tipo2)

    if (operador in ('OP_SUMA', 'OP_RESTA', 'OP_MULTIPLICACION', 'OP_DIVISION')) and (TipoFinal in ('NUM_DECIMAL', 'NUM_ENTERO')):
        return TipoFinal
    elif (operador in ('MAYOR_Q', 'MENOR_Q', 'MAYOR_IGUAL', 'MENOR_IGUAL')) and (TipoFinal in ('NUM_DECIMAL', 'NUM_ENTERO')):
        return 'NUM_BOOLEANOF'
    elif (operador in ('COMPARACION', 'COMPARACION_IGUALDAD')) and (TipoFinal in ('NUM_DECIMAL', 'NUM_ENTERO', 'NUM_BOOLEANOF', 'CADENA_TEXTO')):
        return 'NUM_BOOLEANOF'
    elif (operador == 'OP_SUMA') and (TipoFinal == 'CADENA_TEXTO'):
        return 'CADENA_TEXTO'
    else:
        print("\nError Semántico(ES-01-TYPE): Operación: '", tipo1, operador, tipo2, "' no es válida")
        exit(1)




archivo.write("digraph G {\n")
imprimir(root)
#print("}")
archivo.write("}\n")
archivo.close()

# Llamada a la funcion para registrar variables
registrar_funciones(root)
# Llamada a la funcion para registrar variables
registrar_VARIABLES(root)

semantico(root)

print("\033[92mVerificación de ambito de variables: CORRECTO\n\n\033[0m")

# Imprimir la tabla de simbolos
print("\033[93mTabla de Símbolos:\033[0m")
for simbolo in stack2:
    print(simbolo)

