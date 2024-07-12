import ply.yacc as yacc
from lexer import lexer
from lexer import tokens
from ltl import *


# https://docs.uppaal.org/grammar/#Query
def p_symbolic_query(p):
    """
    SymbolicQuery : AE expression
    | EG expression
    | EE expression
    | expression ARROW expression
    """
    # print(list(p))
    if len(p) == 3:
        p[0] = UnaryOperator(p[1], p[2])
    elif len(p) == 4:
        p[0] = BinaryOperator(p[1], p[2], p[3])
    else:
        raise NotImplementedError(p[:])
    # '''
    #     | expression ARROW expression Subjection
    #     | SUP COLON List Subjection
    #     | SUP LBRACE Predicate RBRACE COLON List Subjection
    #     | INF COLON List Subjection
    #     | INF LBRACE Predicate RBRACE COLON List Subjection
    #     | BOUNDS COLON List Subjection
    #     | BOUNDS LBRACE Predicate RBRACE COLON List Subjection
    # '''
    pass


def p_List(p):
    """List : expression
    | expression COMMA List
    """
    match p:
        case [_, expr]:
            p[0] = [expr]
        case [_, expr, _, list]:
            p[0] = [expr] + list


def p_EXPRESSION(p):
    """
    expression : bin_op_lv6

    """
    print("aa", p[:])
    match p[:]:
        case [_, Identifier() | Const()]:
            p[0] = p[1]
        case [_, BinaryOperator()]:
            p[0] = p[1]
        case [_, "(", ex, ")"]:
            p[0] = ex
        case [_, l, op, r]:
            p[0] = BinaryOperator(l, op, r)
        case _:
            raise NotImplementedError(p[:])


# 逻辑连接词级别
def p_binop_level_6(p):
    """bin_op_lv6 : bin_op_lv5
    | bin_op_lv5 XOR bin_op_lv6
    | bin_op_lv5 AND bin_op_lv6
    | bin_op_lv5 OR bin_op_lv6
    """
    match p[:]:
        case [_, expr, op, expr2]:
            p[0] = BinaryOperator(expr, op, expr2)
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])


# 比较级别
def p_binop_level_5(p):
    """bin_op_lv5 : bin_op_lv4
    | bin_op_lv4 GT bin_op_lv5
    | bin_op_lv4 LE bin_op_lv5
    | bin_op_lv4 GE bin_op_lv5
    | bin_op_lv4 EQ bin_op_lv5
    | bin_op_lv4 NE bin_op_lv5
    | bin_op_lv4 LT bin_op_lv5
    """
    match p[:]:
        case [_, expr, op, expr2]:
            p[0] = BinaryOperator(expr, op, expr2)
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])


# 加减、左右移位级别
def p_binop_level_4(p):
    """
    bin_op_lv4 : bin_op_lv3 PLUS bin_op_lv4
        | bin_op_lv3 MINUS bin_op_lv4
        | bin_op_lv3 LSHIFT bin_op_lv4
        | bin_op_lv3 RSHIFT bin_op_lv4
        | bin_op_lv3
    """
    match p[:]:
        case [_, expr, op, expr2]:
            p[0] = BinaryOperator(expr, op, expr2)
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])
    # p [0] = BinaryOperator(p[1], p[2], p[3])


# 乘除求余级别
def p_binop_level_3(p):
    """
    bin_op_lv3 : sub_expression TIMES bin_op_lv3
        | sub_expression DIVIDE bin_op_lv3
        | sub_expression MOD bin_op_lv3
        | sub_expression
    """
    match p[:]:
        case [_, expr, op, expr2]:
            p[0] = BinaryOperator(expr, op, expr2)
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])





def p_SUB_expression(p):
    """
    sub_expression :  LPAREN expression RPAREN
        | primary
    """
    match p[:]:
        case [_, "(", expr, ")"]:
            p[0] = expr
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])
def p_simple_expression(p):
    """
    primary : IDENTIFIER
        | POS_INTEGER
    """
    match p[:]:
        case [_, BinaryOperator()]:
            p[0] = p[1]
        case [_, Identifier() | Const()]:
            p[0] = p[1]
        case _:
            raise NotImplementedError(p[:])

def p_error(p):
    print(p)
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc(debug=True)
