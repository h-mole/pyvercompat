
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AE AG AMPERSAND AND AND_OP ARG_LIST ARROW ASSIGNMENT BOUNDS BUILTIN_FUNCTION1 BUILTIN_FUNCTION2 BUILTIN_FUNCTION3 CARET COLON COMMA DEADLOCK DECIMAL_NUMBER DIVIDE DOT DYNAMIC_EXPRESSION EE EG EQ FALSE GE GT ID IDENTIFIER IMPLY INF LBRACE LBRACKET LE LOCATION LPAREN LSHIFT LT MINUS MINUSMINUS MINUS_2147483648 MITL_EXPRESSION MOD NE NON_TYPE_ID OR OR_OP PIPE PLUS PLUSPLUS POS_INTEGER POW QUESTION QUOTED_TEXT RBRACE RBRACKET RPAREN RSHIFT STRING_LITERAL SUP TIMES TRUE TYPE UNDER XOR XOR_OP\n    SymbolicQuery : AE expression\n    | EG expression\n    | EE expression\n    | expression ARROW expression\n    List : expression\n    | expression COMMA List\n    \n    expression : bin_op_lv6\n\n    bin_op_lv6 : bin_op_lv5\n    | bin_op_lv5 XOR bin_op_lv6\n    | bin_op_lv5 AND bin_op_lv6\n    | bin_op_lv5 OR bin_op_lv6\n    bin_op_lv5 : bin_op_lv4\n    | bin_op_lv4 GT bin_op_lv5\n    | bin_op_lv4 LE bin_op_lv5\n    | bin_op_lv4 GE bin_op_lv5\n    | bin_op_lv4 EQ bin_op_lv5\n    | bin_op_lv4 NE bin_op_lv5\n    | bin_op_lv4 LT bin_op_lv5\n    \n    bin_op_lv4 : bin_op_lv3 PLUS bin_op_lv4\n        | bin_op_lv3 MINUS bin_op_lv4\n        | bin_op_lv3 LSHIFT bin_op_lv4\n        | bin_op_lv3 RSHIFT bin_op_lv4\n        | bin_op_lv3\n    \n    bin_op_lv3 : sub_expression TIMES bin_op_lv3\n        | sub_expression DIVIDE bin_op_lv3\n        | sub_expression MOD bin_op_lv3\n        | sub_expression\n    \n    sub_expression :  LPAREN expression RPAREN\n        | primary\n    \n    primary : IDENTIFIER\n        | POS_INTEGER\n    '
    
_lr_action_items = {'AE':([0,],[2,]),'EG':([0,],[4,]),'EE':([0,],[5,]),'LPAREN':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'IDENTIFIER':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]),'POS_INTEGER':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'$end':([1,6,7,8,9,10,12,13,14,15,17,18,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[0,-7,-8,-12,-23,-27,-29,-30,-31,-1,-2,-3,-4,-9,-10,-11,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'ARROW':([3,6,7,8,9,10,12,13,14,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[16,-7,-8,-12,-23,-27,-29,-30,-31,-9,-10,-11,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'RPAREN':([6,7,8,9,10,12,13,14,35,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[-7,-8,-12,-23,-27,-29,-30,-31,53,-9,-10,-11,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'XOR':([7,8,9,10,12,13,14,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[19,-12,-23,-27,-29,-30,-31,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'AND':([7,8,9,10,12,13,14,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[20,-12,-23,-27,-29,-30,-31,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'OR':([7,8,9,10,12,13,14,40,41,42,43,44,45,46,47,48,49,50,51,52,53,],[21,-12,-23,-27,-29,-30,-31,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-24,-25,-26,-28,]),'GT':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[22,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'LE':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[23,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'GE':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[24,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'EQ':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[25,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'NE':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[26,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'LT':([8,9,10,12,13,14,46,47,48,49,50,51,52,53,],[27,-23,-27,-29,-30,-31,-19,-20,-21,-22,-24,-25,-26,-28,]),'PLUS':([9,10,12,13,14,50,51,52,53,],[28,-27,-29,-30,-31,-24,-25,-26,-28,]),'MINUS':([9,10,12,13,14,50,51,52,53,],[29,-27,-29,-30,-31,-24,-25,-26,-28,]),'LSHIFT':([9,10,12,13,14,50,51,52,53,],[30,-27,-29,-30,-31,-24,-25,-26,-28,]),'RSHIFT':([9,10,12,13,14,50,51,52,53,],[31,-27,-29,-30,-31,-24,-25,-26,-28,]),'TIMES':([10,12,13,14,53,],[32,-29,-30,-31,-28,]),'DIVIDE':([10,12,13,14,53,],[33,-29,-30,-31,-28,]),'MOD':([10,12,13,14,53,],[34,-29,-30,-31,-28,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'SymbolicQuery':([0,],[1,]),'expression':([0,2,4,5,11,16,],[3,15,17,18,35,36,]),'bin_op_lv6':([0,2,4,5,11,16,19,20,21,],[6,6,6,6,6,6,37,38,39,]),'bin_op_lv5':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,],[7,7,7,7,7,7,7,7,7,40,41,42,43,44,45,]),'bin_op_lv4':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,46,47,48,49,]),'bin_op_lv3':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,50,51,52,]),'sub_expression':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'primary':([0,2,4,5,11,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> SymbolicQuery","S'",1,None,None,None),
  ('SymbolicQuery -> AE expression','SymbolicQuery',2,'p_symbolic_query','parser.py',10),
  ('SymbolicQuery -> EG expression','SymbolicQuery',2,'p_symbolic_query','parser.py',11),
  ('SymbolicQuery -> EE expression','SymbolicQuery',2,'p_symbolic_query','parser.py',12),
  ('SymbolicQuery -> expression ARROW expression','SymbolicQuery',3,'p_symbolic_query','parser.py',13),
  ('List -> expression','List',1,'p_List','parser.py',35),
  ('List -> expression COMMA List','List',3,'p_List','parser.py',36),
  ('expression -> bin_op_lv6','expression',1,'p_EXPRESSION','parser.py',47),
  ('bin_op_lv6 -> bin_op_lv5','bin_op_lv6',1,'p_binop_level_6','parser.py',66),
  ('bin_op_lv6 -> bin_op_lv5 XOR bin_op_lv6','bin_op_lv6',3,'p_binop_level_6','parser.py',67),
  ('bin_op_lv6 -> bin_op_lv5 AND bin_op_lv6','bin_op_lv6',3,'p_binop_level_6','parser.py',68),
  ('bin_op_lv6 -> bin_op_lv5 OR bin_op_lv6','bin_op_lv6',3,'p_binop_level_6','parser.py',69),
  ('bin_op_lv5 -> bin_op_lv4','bin_op_lv5',1,'p_binop_level_5','parser.py',82),
  ('bin_op_lv5 -> bin_op_lv4 GT bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',83),
  ('bin_op_lv5 -> bin_op_lv4 LE bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',84),
  ('bin_op_lv5 -> bin_op_lv4 GE bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',85),
  ('bin_op_lv5 -> bin_op_lv4 EQ bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',86),
  ('bin_op_lv5 -> bin_op_lv4 NE bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',87),
  ('bin_op_lv5 -> bin_op_lv4 LT bin_op_lv5','bin_op_lv5',3,'p_binop_level_5','parser.py',88),
  ('bin_op_lv4 -> bin_op_lv3 PLUS bin_op_lv4','bin_op_lv4',3,'p_binop_level_4','parser.py',102),
  ('bin_op_lv4 -> bin_op_lv3 MINUS bin_op_lv4','bin_op_lv4',3,'p_binop_level_4','parser.py',103),
  ('bin_op_lv4 -> bin_op_lv3 LSHIFT bin_op_lv4','bin_op_lv4',3,'p_binop_level_4','parser.py',104),
  ('bin_op_lv4 -> bin_op_lv3 RSHIFT bin_op_lv4','bin_op_lv4',3,'p_binop_level_4','parser.py',105),
  ('bin_op_lv4 -> bin_op_lv3','bin_op_lv4',1,'p_binop_level_4','parser.py',106),
  ('bin_op_lv3 -> sub_expression TIMES bin_op_lv3','bin_op_lv3',3,'p_binop_level_3','parser.py',121),
  ('bin_op_lv3 -> sub_expression DIVIDE bin_op_lv3','bin_op_lv3',3,'p_binop_level_3','parser.py',122),
  ('bin_op_lv3 -> sub_expression MOD bin_op_lv3','bin_op_lv3',3,'p_binop_level_3','parser.py',123),
  ('bin_op_lv3 -> sub_expression','bin_op_lv3',1,'p_binop_level_3','parser.py',124),
  ('sub_expression -> LPAREN expression RPAREN','sub_expression',3,'p_SUB_expression','parser.py',140),
  ('sub_expression -> primary','sub_expression',1,'p_SUB_expression','parser.py',141),
  ('primary -> IDENTIFIER','primary',1,'p_simple_expression','parser.py',152),
  ('primary -> POS_INTEGER','primary',1,'p_simple_expression','parser.py',153),
]
