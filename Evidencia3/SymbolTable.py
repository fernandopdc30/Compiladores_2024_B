from LL1 import principal 
from Lexico import get_tokens

class SymbolTable:
    def __init__(self):
        self.symbols = []

    # Método para añadir un símbolo a la tabla, especificando su nombre, tipo, valor, alcance y función a la que pertenece
    def add_symbol(self, name, symbol_type, value=None, scope='local', func_belong=None):
        self.symbols.append({
            'name': name,
            'type': symbol_type,
            'value': value,
            'scope': scope,
            'function_belonging': func_belong
        })

    # Método para imprimir la tabla de símbolos de forma formateada
    def __str__(self):
        header = f"{'Nombre':<15} {'Tipo':<10} {'Valor':<20} {'Scope':<10} {'Funcion':<15}"
        rows = [header]
        for symbol in self.symbols:
            row = f"{symbol['name']:<15} {symbol['type']:<10} {str(symbol['value']):<20} {symbol['scope']:<10} {symbol['function_belonging']}"
            rows.append(row)
        return '\n'.join(rows)

# Función que recorre el árbol sintáctico y construye la tabla de símbolos
def build_symbol_table(node, symbol_table, current_function=None):
    lexeme = getattr(node, 'lexeme', None)
    print(f"Procesando nodo: {lexeme}")

    # Manejo de declaraciones de funciones
    if lexeme == 'def' and len(node.children) > 1:
        function_name = getattr(node.children[1], 'lexeme', None)
        if function_name:
            # Añade la función a la tabla de símbolos con alcance global
            symbol_table.add_symbol(function_name, 'Función', None, 'global')
            print(f"Añadiendo función: {function_name}")
            current_function = function_name

            # Procesa los parámetros de la función, si existen
            if len(node.children) > 3:
                params_node = node.children[3]
                if params_node and getattr(params_node, 'lexeme', None) == 'PARAMETROS':
                    print("Procesando parámetros de la función:", function_name)
                    for param in params_node.children:
                        if param.lexeme == 'int' or param.lexeme == 'bool':
                            # Añade el parámetro a la tabla con alcance local
                            if len(param.children) > 1:
                                param_name = getattr(param.children[1], 'lexeme', None)
                                param_type = param.lexeme
                                if param_name:
                                    symbol_table.add_symbol(param_name, 'Parámetro', None, 'local', current_function)
                                    print(f"Añadiendo parámetro: {param_name} de tipo {param_type}")

            # Procesa declaraciones dentro de la función
            if len(node.children) > 6:
                declarations_node = node.children[6]
                if declarations_node and getattr(declarations_node, 'lexeme', None) == 'DECLARACIONES':
                    print(f"Procesando declaraciones en la función: {current_function}")
                    for decl in declarations_node.children:
                        if getattr(decl, 'lexeme', None) == 'DECLARACION' and len(decl.children) > 1:
                            var_type = getattr(decl.children[0], 'lexeme', None)
                            var_name = getattr(decl.children[1], 'lexeme', None)
                            if var_name and var_type:
                                symbol_table.add_symbol(var_name, 'Variable', None, 'local', current_function)
                                print(f"Añadiendo variable: {var_name} de tipo {var_type}")

            # Procesa el retorno de la función, si existe
            if len(node.children) > 8 and getattr(node.children[8], 'lexeme', None) == 'return':
                return_var = getattr(node.children[9], 'lexeme', None)
                if return_var:
                    symbol_table.add_symbol(return_var, 'Retorno', None, 'local', current_function)
                    print("Añadiendo retorno de la función:", return_var)

    # Manejo de asignaciones fuera de funciones
    elif lexeme == 'ASIGNAR' and len(node.children) > 1:
        var_name = getattr(node.children[0], 'lexeme', None)
        if var_name:
            # Añade una variable global en caso de asignación fuera de una función
            symbol_table.add_symbol(var_name, 'Variable', None, 'global')
            print(f"Añadiendo variable global en asignación: {var_name}")

    # Recursión sobre los hijos del nodo para procesar todo el árbol
    for child in getattr(node, 'children', []):
        build_symbol_table(child, symbol_table, current_function)

# Función que genera la tabla de símbolos a partir de un archivo de código fuente
def generate_symbol_table_from_code(file_path):
    # Abre el archivo y obtiene los tokens
    with open(file_path, 'r') as fp:
        tokens = get_tokens(fp)
    tokens.append({'type': '$', 'lexeme': None, 'line': None})

    # Genera el árbol sintáctico a partir de los tokens usando la función `principal`
    root, node_list = principal(tokens)

    # Crea una instancia de SymbolTable y construye la tabla
    symbol_table = SymbolTable()
    build_symbol_table(root, symbol_table)

    # Imprime la tabla de símbolos generada
    print("Tabla de Símbolos Generada:")
    print(symbol_table)

# Ejecuta la función principal para generar la tabla de símbolos
if __name__ == "__main__":
    generate_symbol_table_from_code("ejemplo5.txt")
