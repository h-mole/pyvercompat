from lexer import lexer
from parser import parser
def parse_query(query):
    # ret = lexer.input(query)
    # print(ret)
    return parser.parse(query)
import pprint as pp
query = "A<> x*(y+4)"
query = "A<> ((AC1>1&&3)&&(SIc2==250)&&(SIc1==200)&&(AC2==0))&&SIc>500"
# query = "A<> AC==1&&SIc>500"
# query = "A<> AC1<0&&SIc>500"
# query = "A<> ((a==3) && (a==5))"
result = parse_query(query)
# print(result)
print(pp.pprint(result.to_dict()))
print(type(result))
print(result.unparse())