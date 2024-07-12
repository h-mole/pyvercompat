import ply.lex as lex
from ltl import Const, Identifier

tokens = (
    "AG",  # All paths, Always satisfy
    "EG",  # Exists a path, Always satisfy
    "AE",  # All paths, Eventually satisfy
    "EE",  # Exists a path, Eventually satisfy
    "SUP",
    "INF",
    "BOUNDS",
    # "STRATEGYNAME",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COLON",
    "COMMA",
    "ARROW",
    "UNDER",
    "IDENTIFIER",
    "LPAREN",
    "RPAREN",
    "FALSE",
    "TRUE",
    "POS_INTEGER",
    "DECIMAL_NUMBER",
    "QUOTED_TEXT",
    "BUILTIN_FUNCTION1",
    "BUILTIN_FUNCTION2",
    "BUILTIN_FUNCTION3",
    "PLUSPLUS",
    "MINUSMINUS",
    "DOT",
    "LOCATION",
    "NON_TYPE_ID",
    "ARG_LIST",
    "ASSIGNMENT",
    "STRING_LITERAL",
    "DYNAMIC_EXPRESSION",
    "MITL_EXPRESSION",
    "ID",
    "TYPE",
    "LT",
    "LE",
    "EQ",
    "NE",
    "GT",
    "GE",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "POW",
    "AMPERSAND",
    "PIPE",
    "CARET",
    "LSHIFT",
    "RSHIFT",
    "AND",
    "OR",
    "XOR",
    "QUESTION",
    "IMPLY",
    "AND_OP",
    "OR_OP",
    "XOR_OP",
    "MINUS_2147483648",
    "DEADLOCK",
    # "EXPRESSION",
)


# The token parsing order
# could be seen from
# https://ply.readthedocs.io/en/latest/ply.html#specification-of-tokens
# The function-defined tokens first, then string-defined tokens.
def t_AG(t):
    r"A\[\]"
    return t


def t_EG(t):
    r"E\[\]"
    return t


def t_EE(t):
    r"E<>"
    return t


def t_AE(t):
    r"A<>"
    return t


def t_POS_INTEGER(t):
    r"\d+"
    t.value = Const(t.value, "int")
    return t


def t_IDENTIFIER(t):
    r"\w+"
    t.value = Identifier(t.value)
    return t


def t_DECIMAL_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = Const(t, "float")
    return t


t_SUP = r"sup"
t_INF = r"inf"
t_BOUNDS = r"bounds"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COLON = r"\:"
t_COMMA = r","
t_ARROW = r"-->"
t_UNDER = r"under"
t_FALSE = r"false"
t_TRUE = r"true"


t_QUOTED_TEXT = r"\".*?\""
# t_NON_TYPE_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"--"
t_DOT = r"\."
t_LOCATION = r"location"
t_MINUS_2147483648 = r"-2147483648"
t_DEADLOCK = r"deadlock"
t_STRING_LITERAL = r"\'.*?\'"
# t_DYNAMICE_EXPRESSION = r'\w+?D/ynamicExpression'
t_MITL_EXPRESSION = r"\w+?MITLExpression"
t_ASSIGNMENT = r"\w+?Assignment"
t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_TYPE = r"\w+?Type"
t_LT = r"<"
t_LE = r"<="
t_EQ = r"=="
t_NE = r"!="
t_GT = r">"
t_GE = r">="
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"
t_POW = r"\*\*"
t_AMPERSAND = r"&"
t_PIPE = r"\|"
t_CARET = r"\^"
t_LSHIFT = r"<<"
t_RSHIFT = r">>"
t_AND = r"&&"
t_OR = r"\|\|"
t_XOR = r"\^"
t_QUESTION = r"\?"
t_IMPLY = r"imply"
t_AND_OP = r"and"
t_OR_OP = r"or"
t_XOR_OP = r"xor"
t_ignore = " \t\n"


def t_error(t):
    print(t.value)
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
