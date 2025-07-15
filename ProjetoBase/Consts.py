"""
add:
    TRUE = 'true'
    FALSE = 'false'
    BOOL = 'BOOL'
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'
    EQEQ = '=='
    NE = '!='
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='
    KEYS += [TRUE, FALSE, IF, THEN, ELSE]
"""
import string

class Consts:
    DIGITOS = '0123456789'
    LETRAS = string.ascii_letters
    LETRAS_DIGITOS = DIGITOS + LETRAS
    UNDER = '_'
    INT       = 'INT'
    FLOAT     = 'FLOAT'
    PLUS      = '+'
    MINUS     = '-'
    MUL       = '*'
    DIV       = '/'
    LPAR      = '('
    RPAR      = ')'
    EOF       = '$EOF'
    EQ        = '='
    POW       = '^'
    ID	      = 'ID'
    KEY		  = 'KEY'
    NULL      = 'null'
    STRING    = "STRING"
    GRAPH     = '@'
    LSQUARE   = "[" # Left  Box brackets [
    RSQUARE   = "]" # Right Box brackets ]
    COMMA      = ","
    TRUE = 'true'
    FALSE = 'false'
    BOOL = 'BOOL'
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'
    EQEQ = '=='
    NE = '!='
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='

    # Exemplos de Palavras reservadas
    LET         = 'let'
    IF          = 'if'
    WHILE       = 'while'
    FOR         = 'for'
    KEYS = [
        LET,
        IF,
        WHILE,
        FOR
    ]
    KEYS += [TRUE, FALSE, IF, THEN, ELSE]


