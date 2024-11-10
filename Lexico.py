import ply.lex as lex

# List of token names. This is always required
reserved = {

    'def'       : 'def',
    'if'        : 'if',
    'else'      : 'else',
    'return'    : 'return',
    'int'       : 'int',
    'while'     : 'while',
    'bool'      : 'bool',
    'true'      : 'true',
    'false'     : 'false',
    'and'       : 'and',
    'or'        : 'or'   
}
tokens = [
    'id',
    'num',
    'oper_suma',
    'oper_resta',
    'oper_mul',
    'oper_div',
    'oper_asig',
    'mayor',
    'menor',
    'par_inicio',
    'par_fin',
    'll_inicio',
    'll_fin',
    'punto_coma',
    'comma',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_oper_suma = r'\+'
t_oper_resta = r'\-'
t_oper_mul = r'\*'
t_oper_div = r'\/'
t_oper_asig = r'\='
t_mayor = r'\>'
t_menor = r'\<'
t_par_inicio = r'\('
t_par_fin = r'\)'
t_ll_inicio = r'\{'
t_ll_fin = r'\}'
t_punto_coma = r'\;'
t_comma = r'\,'



# A regular expression rule with some action code

def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_id(t):
    r'[a-zA-Z]+([a-zA-Z0-9]*)'
    t.type = reserved.get(t.value, 'id')
    return t

# Define a rule so we can track line numbers
def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def get_tokens(fp):

    data = fp.read()
    print(data)
    fp.close()

    # Give the lexer some input
    lexer.input(data)
    # Guarda la informacion

    guardar_token = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        guardar_token.append({'type': tok.type.lower(), 'lexeme': str(
            tok.value).lower(), 'line': tok.lineno})

    guardar_token.append(
        {'type': '$', 'lexeme': '$', 'line': guardar_token[-1]['line']})
    return guardar_token


if __name__ == "__main__":
    fp = open("ejemplo1.txt")
    tokens = get_tokens(fp)
    #print(tokens)