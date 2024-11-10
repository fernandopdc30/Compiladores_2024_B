import pandas as pd
import sys
import graphviz

from Lexico import get_tokens

#Variables globales
counter = 0
cont = 0
copia = []
copia2 = []
dot = graphviz.Digraph('round-table', comment='parser')
syntax_table = pd.read_csv("gramatica.csv", index_col=0)
# Crea un gráfico creando una instancia de un nuevo objeto Graph o Digraph:
#dot = graphviz.Digraph('round-table', comment='The Round Table')
arbol = graphviz.Graph(comment="Arbol Generedo")

# Recorrido del stack: muestra el contenido actual pila
def print_stack():
    print("\nStack:")
    for e in stack:
        print(e.symbol, end=" ")
    print()

# Recorrido de tokens: muestra tokens que en proceso
def print_input():
    print("\ntokens:")
    for t in tokens:
        print(t['type'], end=" ")
    print()

# Retorna un nodo del arbol sintáctico segun el id
def find_in_tree(node_list, id):
    for nod in node_list:
        if nod.symbol.id == id:
            return nod

# Genera la representación grafica del árbol sintáctico con graphviz
def print_tree(node, node_list, info=False):
    global dot
    dot = "digraph G { \n"

    for nod in node_list:
        if nod.symbol.is_terminal:
            if nod.symbol.symbol == 'e':
                # Nodo terminal con color
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> >, style=filled, fillcolor=yellow ]; \n'
            else:
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme
                # Nodo terminal con color
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(lexeme) + ' >, style=filled, fillcolor=yellow ]; \n'
        else:
            # Nodo no terminal, sin color
            if info and (nod.symbol.symbol == 'E' or nod.symbol.symbol == 'T' or nod.symbol.symbol == "E'" or nod.symbol.symbol == 'TERM'):
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme

                if nod.visited == True:
                    dot += str(nod.symbol.id) + ' [ <b>' + nod.symbol.symbol + '</b> <br/> ' + str(nod.type) + ' <br/> line ' + str(nod.line) + ' > ]; \n'
                else:
                    dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(nod.type) + ' > ]; \n'
            else:
                dot += str(nod.symbol.id) + ' [ label=" ' + nod.symbol.symbol + ' " ]; \n'
    # Conecto los nodos del arbol recursivamente, para el grafico
    print_tree_recursive(node)
    dot += "}"

    graph = graphviz.Source(dot, format='png')
    graph.render("Arbol.png", view=True)


def print_tree_recursive(node):
    global dot
    tmp = []
    for child in node.children:
        dot += str(node.symbol.id) + ' -> ' + str(child.symbol.id) + '; \n'
        tmp.append(str(child.symbol.id))
        print_tree_recursive(child)
    
    if len(node.children) > 0:
        dot += "{ \n"
        dot += "    rank = same; \n"
        dot += "    edge[ style=invis]; \n"
        dot += " -> ".join(tmp) + "; \n"
        dot += "    rankdir = LR; \n"
        dot += "} \n"

# Reemplazar valores /token_type - > Actuliza la pila
def update_stack(stack, token_type):
    production = syntax_table.loc[stack[0].symbol][token_type] # -> Es el primer elemento del input

    #   Error Sintactico
    if (pd.isna(production)):
        print("Error, no es reconocida")
        sys.exit()


    elementos = production.split(" ")
    father = elementos[0]

    # Eliminación de los valores
    elementos.pop(0)
    elementos.pop(0)
    # Eliminación de la pila
    father = stack.pop(0)
    # Implementa una función que retorna una instancia a nodo_parser a partir de father.id
    node_father = find_in_tree(node_list, father.id)


    if elementos[0] == "''":  # nulo
        new_symbol = node_stack( 'e', True )
        nod_tree    = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        node_list.append(nod_tree)
        return True

    for prod in reversed(elementos):
        # Inserta en la pila
        new_symbol = node_stack( prod, False if prod.isupper() else True )
        stack.insert(0, new_symbol)
        
        nod_tree = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        node_list.append(nod_tree)

    return True


# Nodo principal -> representa elementos de la pila, terminales y noterminales
class node_stack:

    def __init__(self, symbol, is_terminal):
        global counter
        self.id = counter
        self.symbol = symbol
        self.is_terminal = is_terminal
        counter += 1

# Las Hojas del arbol -> representa los nodos en el arbol sintactico
class node_parser:

    def __init__(self, symbol, lexeme=None, children=[], father=None, line=None):
        self.symbol = symbol
        self.lexeme = lexeme
        self.line = line
        self.children = children
        self.father = father


#  Entrada para el Stak -> Inicialización de la pila y el árbol
stack = []
symbol_1 = node_stack('$', True)        # numero 0 en stack
symbol_2 = node_stack('INICIO', False)  # numero 1 en stack
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)
# Se creara los hijos
# Creaer el node -> raiz
root = node_parser(symbol_2, [])
node_list = []
node_list.append(root)


# Condicionales -> procesa los tokens uno por uno
# El proceso de deteniene cuando el simbolo de la pila y token, son ambos $
def principal(tokens):
    while True:
        #print("ITERACIÓN...")
        #print_stack()
        #print_input()
        if stack[0].symbol == '$' and tokens[0]['type'] == '$':
            print("Todo bien, ejecución exitosa")
            break

        if stack[0].is_terminal:
            #print("Terminales...")
            if stack[0].symbol == tokens[0]['type']:
                nod = find_in_tree(node_list, stack[0].id)
                nod.lexeme = tokens[0]['lexeme'] 
                nod.line = tokens[0]['line']
                stack.pop(0)
                tokens.pop(0)
            else:
                print("ERROR sintáctico")
                break

        # Si son diferentes se tiene que reemplazar segun la tabla 
        else:
            update_stack(stack, tokens[0]['type'])

    return root, node_list


if __name__ == "__main__":
    fp = open("ejemplo5.txt")
    tokens = get_tokens(fp)
    tokens.append([ '$', None, None ])
    principal(tokens)
    print_tree(root, node_list, info = False)
    #print(dot)
