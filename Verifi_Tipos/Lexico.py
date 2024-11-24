import ply.lex as lex

# Palabras reservadas
reserved = {
    'Proceso':          'INICIO_PROCESO',
    'FinProceso':       'FIN_PROCESO',
    'si':               'CONDICIONES_SI',
    'sino':             'CONDICIONES_SINO',
    'mientras':         'MIENTRAS',
    'imprimir':         'IMPRESOR',
    'entero':           'DATO_ENTERO',
    'para':             'PARA',
    'largo':            'DATO_DECIMAL',
    'flotante':         'DATO_FLOTANTE',
    'caracter':         'DATO_CARACTER',
    'booleano':         'DATO_BOOLEANO',
    'funcion':          'FUNCION',
    'regresa':          'REGRESA',
    'true' :            'NUM_BOOLEANOV',
    'false' :           'NUM_BOOLEANOF',
    'OR' :              'OP_LOGICOOR',
    'AND' :             'OP_LOGICOAND',
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR', 
    'NUM_ENTERO', 
    'NUM_DECIMAL', 
    'OP_SUMA', 
    'OP_RESTA',
    'OP_MULTIPLICACION', 
    'OP_DIVISION', 
    'MAYOR_Q', 
    'MENOR_Q', 
    'IGUALDAD',
    'COMPARACION', 
    'MAYOR_IGUAL', 
    'MENOR_IGUAL', 
    'INCREMENTO',
    'COMPARACION_IGUALDAD', 
    'SUM_ASIGNACION', 
    'DECREMENTO',
    'CADENA_TEXTO', 
    'COMENTARIO', 
    'INICIO_PARENTESIS', 
    'FIN_PARENTESIS',
    'PARENTESIS_ABRIR', 
    'PARENTESIS_CERRAR', 
    'LLAVE_ABRIR', 
    'LLAVE_CERRAR',
    'COMA', 
    'PUNTO', 
    'P_COMA', 
    'INICIO_COMENTARIO', 
    'FIN_COMENTARIO'
] + list(reserved.values())

# Expresiones regulares para los tokens
t_OP_SUMA = r'\+'
t_OP_RESTA = r'-'
t_OP_MULTIPLICACION = r'\*'
t_OP_DIVISION = r'%|/'
t_MAYOR_Q = r'>'
t_MENOR_Q = r'<'
t_IGUALDAD = r'='
t_COMPARACION = r'=='
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_INCREMENTO = r'\+\+'
t_COMPARACION_IGUALDAD = r'!='
t_SUM_ASIGNACION = r'\+='
t_DECREMENTO = r'--'
t_PARENTESIS_ABRIR = r'\('
t_PARENTESIS_CERRAR = r'\)'
t_LLAVE_ABRIR = r'\{'
t_LLAVE_CERRAR = r'\}'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_P_COMA = r'\;'
t_INICIO_COMENTARIO = r'\.\*'
t_FIN_COMENTARIO = r'\*\.'


# Regla para manejar identificadores
def t_IDENTIFICADOR(t):
  r'[_a-zA-Z][_a-zA-Z0-9]*'
  t.type = reserved.get(t.value,'IDENTIFICADOR')  # Verificar palabras reservadas
  return t


def t_NUM_DECIMAL(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  #print("se reconocio el numero")
  return t

def t_NUM_ENTERO(t):
  r'\d+'
  t.value = int(t.value) 
  #print("se reconocio el numero")
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
  print("Caracter invalido '%s'" % t.value[0])
  t.lexer.skip(1)


def t_COMENTARIO(t):
  r'\#.*\#'
  pass
  '''t.value = t.value[1:-1]  # Elimina los símbolos # al principio y al final
  return t'''


# Regla para manejar cadenas de texto
def t_CADENA_TEXTO(t):
  r'"([^"\\]|\\.)*"'
  t.value = str(t.value)
  return t


# Construir el lexer
lexer = lex.lex()

def lexico(ruta):
    with open(ruta, 'r') as file:
        data = file.read()

    lexer.input(data)

    lista_tokens = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        info_token = {
            "simbolo": tok.type,
            "lexema": tok.value,
            "nroline": tok.lineno,
            "col": tok.lexpos
        }
        print(info_token)
        lista_tokens.append(info_token)

    # Añadir token de fin de archivo
    lista_tokens.append({"simbolo": "$", "lexema": "$", "nroline": 0, "col": 0})
    print("\033[92mAnalizador Lexico: CORRECTO\n\033[0m")
    return lista_tokens
