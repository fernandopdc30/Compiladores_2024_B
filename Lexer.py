# ------------------------------------------------------------
# Lexer.py
#
# tokenizer for a simple expression evaluator for
# 
# ------------------------------------------------------------
import ply.lex as lex

# List of token names. This is always required
reserved = { 
    'doit'              : 'DEF',
    'innig'             : 'IN',
    'weing'             : 'TIPO_WHILE',
    'fall'              : 'TIPO_FOR',
    'play'              : 'PRINT',
    'irato'             : 'IF',
    'etwas'             : 'ELSE',
    'tutti'             : 'TRUE',
    'flat'              : 'FALSE',
    'resolve'           : 'RETURN',
    'assai'             : 'AND',
    'ossia'             : 'OR'
}

tokens = [
    'NUM',
    'REAL',
    'STRING',
    'NULL',
    'OPER_SUMA',
    'OPER_RESTA',
    'OPER_MUL',
    'OPER_DIV',
    'OPER_RESTO',
    'SIG_MAYOR',
    'SIG_MENOR',
    'SIG_MAYORIGUAL',
    'SIG_MENORIGUAL',
    'SIG_IGUAL',
    'OPER_IGUALDAD',
    'OPER_DIFER',
    'PAR_INICIO',
    'PAR_FIN',
    'LL_INICIO',
    'LL_FIN',
    'COR_INICIO',
    'COR_FIN',
    'COMA',
    'PUNTO_COMA',
    'PUNTO',
    'DOS_PUNTOS',
    'GUION_BAJO',
    'ID',
    'COMEN_LINEA',
    'COMEN_PARRAFO'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_OPER_SUMA    = r'\+'
t_OPER_RESTA   = r'-'
t_OPER_MUL   = r'\*'
t_OPER_DIV  = r'/'
t_OPER_RESTO = r'%'
t_SIG_MAYOR = r'>'
t_SIG_MENOR = r'<'
t_SIG_MAYORIGUAL = r'>='
t_SIG_MENORIGUAL = r'<='
t_SIG_IGUAL = r'\='
t_OPER_IGUALDAD = r'\=\='
t_OPER_DIFER = r'!='
t_PAR_INICIO  = r'\('
t_PAR_FIN  = r'\)'
t_LL_INICIO = r'\{'
t_LL_FIN = r'\}'
t_COR_INICIO = r'\['
t_COR_FIN = r'\]'
t_COMA = r'\,'
t_PUNTO_COMA = r'\;'
t_PUNTO = r'\.'
t_DOS_PUNTOS = r'\:'
t_GUION_BAJO = r'\_'


# A regular expression rule with some action code
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.strip('"'),'ID')
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)   
    return t

def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover las comillas
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

def t_COMEN_LINEA(t):
    r'\#.*'
    return t

def t_COMEN_PARRAFO(t):
    r'\/\*(?:.|\n)*?\*\/'
    return t 

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Archivo externo
archivo_externo = "ejemplo1.txt" 
with open(archivo_externo, "r") as file:
    data = file.read()

# Give the lexer some input
lexer.input(data)

# Tokenize
def tokenize(input_string):
    lexer.input(input_string)
    tokens = []
    
    while True:
        tok = lexer.token()
        if not tok: 
            break
        tokens.append(tok)
    return tokens
    
# Print(tok)
tokens = tokenize(data)
for tok in tokens:
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
