import ply.yacc as yacc
from lexer import tokens
import sys
import ast as tree
precedence = (
    ('left','ORELSE'),
    ('left','ANDALSO'),
    ('left','NOT'),
    ('left', 'LESSTHAN', 'GREATERTHAN','LESSTHANEQUAL','GREATERTHANEQUAL','EQUALTO','NOTEQUALTO'),  # Nonassociative operators    ('right','EXPONENTIAL'),
    ('right','CONS'),  
    # ('left','EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','DIV','MOD'),
     ('right', 'UMINUS'),
      ('right','EXPONENTIAL'),
      ('left','LBRACKET','RBRACKET'),
    ('left','HASH'),    
    ('left','LPAREN','RPAREN'),
                 # Unary minus operator
)

def p_statement_block(p):
    'statement : block'
    p[0]=p[1]

def p_block_statements(p):
    '''block : LBRACE statements RBRACE
             | LBRACE RBRACE'''
    # print("in block")
    if len(p)== 4:
        p[0]=tree.BlockN(p[2])       
    else:
        p[0]=tree.BlockN([])

def p_statements_statement_sts(p):
    'statements : statement statements'
    # print("in statement_lst")
    p[0]=[p[1]]+p[2]

def p_statements_statement(p):
    'statements : statement '
    # print("in statement")
    p[0]=[p[1]]

def p_statement_expr(p):
    'statement : IDENTIFIER EQUALS expression SEMICOLON'
    # print("ia m here")
    # print(p[1],p[2],p[3])
    # p[1]=IdentiferN(p[1])
    # print("identifier############",p[1])
    # p[0]=p[1]
    p[0]=tree.AssignN(p[1],p[3])

def p_statement_assignlist(p):
    'statement : IDENTIFIER LBRACKET expression RBRACKET EQUALS expression SEMICOLON'
    # print("identifier***************",p[1])
    p[0]=tree.AssignListN(p[1],p[3],p[6])

def p_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0]=tree.PrinterN(p[3])

def p_ifblock(p):
    'statement : IF LPAREN expression RPAREN block'
    if len(p)==6:
        p[0]=tree.IFNode(p[3],p[5])

def p_ifelseblock(p):
    'statement : IF LPAREN expression RPAREN block ELSE block'
    p[0]=tree.IFELSENode(p[3],p[5],p[7])

def p_Whileblock(p):
    'statement :  WHILE LPAREN expression RPAREN block'
    # print("in while grammar")
    p[0]=tree.WhileNode(p[3],p[5])

def p_expression_binaryop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression EXPONENTIAL expression
                  | expression DIV expression
                  | '''
    # print("in binops val",p[2])
    # print(p[2] in lst_ops)
    lst_ops=['+','-','*','/','mod','**','div']
    if len(p)==4 and p[2] in lst_ops:
        # print("yeah")
        p[0]=tree.BinaryOpN(p[1],p[2],p[3])  

def p_expression_conditional_exp(p):
    '''expression : expression ANDALSO expression
                    | expression ORELSE expression
                    | expression IN expression
                    | expression LESSTHAN expression
                    | expression LESSTHANEQUAL expression
                    | expression EQUALTO expression
                    | expression GREATERTHAN expression
                    | expression GREATERTHANEQUAL expression
                    | expression NOTEQUALTO expression
                    '''
    # print("in comparator")
    # print(p[1] ,p[2],p[3])
    p[0]=tree.ComparisonN(p[1],p[2],p[3])

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    if p[1]=='True' : p[0] =tree.BooleanN(True)#True 
    elif p[1] == 'False' : p[0]=tree.BooleanN(False)#False

def p_notExpression(p):
    'expression : NOT expression'
    # p[0]=not p[2]
    p[0]=tree.NotBoolN(p[2])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    # p[0] = -p[2]
    # print("UMinusN")
    p[0]=tree.UMinusN(p[2])

def p_expression_str(p):
    'expression : STRING'
    # p[0]=p[1]
    # print("stringgrammar")
    p[0]=tree.StringN(p[1])

def p_expression_number(p):
    '''expression : REAL
                  | INTEGER
                  '''
    # p[0]=p[1]
    # print("number  grammar",p[1])
    p[0]=tree.NumbersN(p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    # print("i reached here")
    p[0] = p[2]
			 
def p_lst_expression(p):
    '''expression : LIST
                  | TUPLE'''
    # print("inside Tuple or list")
    p[0]=p[1]

def p_lst(p):
    'LIST : LBRACKET  inside_lst RBRACKET'
    # print("left inside right")
    p[0]=p[2]

def p_exp_inlst(p):
    'inside_lst : expression'
    # p[0]=[p[1]]
    # print(" insideexp")
    p[0]=tree.ListN(p[1])

def p_exp_inlstComma(p):
    'inside_lst : inside_lst COMMA expression'
    # p[1].append(p[3])
    # print("inside comma exp")
    p[1].list.append(p[3])
    p[0]=p[1]

# def p_exp_inlstEmpt(p):
#     'inside_lst : LBRACKET RBRACKET'
#     # p[0]=[]
#     p[0]=EmptyListN()
#new addition
def p_exp_inlstEmpty(p):
    'LIST : LBRACKET RBRACKET'
    # p[0]=[]
    # print("emptylst")
    p[0]=tree.EmptyListN()

def p_exp_con_OP(p):
    'expression : expression CONS expression'
    # if(type([p[1]])!=type(p[3])):
        # raise Exception
    # else:
    # print("inconsls")
    p[0]=tree.ConsN(p[1],p[3])

def p_expListIndex(p):
    'expression : expression LBRACKET expression RBRACKET'
    # print(p[3])
    # if(type(p[3])!=int):
    #     raise Exception
    # p[0]=p[1][p[3]]
    p[0]=tree.IndexListN(p[1],p[3])

def p_exp_str_index(p):
    'expression : STRING LBRACKET expression RBRACKET'
    # if(type(p[3])!=int):
    #     print("error found",type(p[3]))
    #     raise Exception
    # p[0]=p[1][p[3]]
    ####check again
    stringNode=tree.StringIndexN(StringN(p[1]),p[3])
    p[0]=stringNode

def p_expListIndex_DoubleIndex(p):
    'expression : LIST LBRACKET expression RBRACKET LBRACKET expression RBRACKET'
    # if(type(p[1][p[3]])!=list):
    #     raise Exception
    # if(type(p[1].eval()[p[3].eval()])!=list):
    #     raise Exception
    # p[0]=p[1][p[3]][p[6]]
    # print("list double indexing")
    p[0]=tree.DoubleIndexListN(p[1],p[3],p[6])

def p_tuple(p):
    'TUPLE : LPAREN inside_tuple RPAREN'
    # print("inside_tuple1")
    p[0]=p[2]

def p_tupe_comma(p):
    'TUPLE : LPAREN inside_tuple COMMA RPAREN'
    p[0]=p[2]

def p_in_tuple_exp(p):
    '''inside_tuple : expression '''
    # p[0]=[p[1]]
    # print("inside_tuple2")
    p[0]=tree.TupleN(p[1])


def p_in_tuple_COMMA_exp(p):
    'inside_tuple : inside_tuple COMMA expression'
    # if len(p)==4:p[1].value.append(p[3])
    p[1].value.append(p[3])
    p[0]=p[1]

def p_tupleIndex(p):
    'expression  : HASH INTEGER TUPLE'
    p[0]=tree.TupleIndexN(p[3],p[2])

def p_expression_name(p):
    'expression : IDENTIFIER'
    # print("in expression name")
    # print(p[1])
    try:
        # p[0] = names[p[1]]
        p[0]=p[1]
        # p[0]=IdentiferN(p[1])
    except LookupError:
        # print(f"Undefined name {p[1]!r}")
        p[0] = 0
        raise Exception

def p_error(p):
    # print(f"Syntax error at {p.value!r}")
    raise SyntaxError

yacc.yacc(debug=False)
# if len (sys.argv)!=2:
#     print("Invalid Parameters")
# else:
#     filePath=sys.argv[1]
#     fileStream=open(filePath,'r')
#     for line in fileStream:
#         try:
#             rootNode=yacc.parse(line)
#             result=rootNode.eval()
#             if type(result) is str:print("\'"+result+"\'")
#             else:print(result)
#         except SyntaxError:
#             print("SYNTAX ERROR")
#         except Exception:
#             print("SEMANTIC ERROR")
#             continue
    

# while True:
#     try:
#         s = input('calc > ')
#         # head=yacc.parse(s)
#         # head.eval()
#         head=yacc.parse(s)
#         # print("head",head)
#         val=head.eval()
#         if type(val) is str:print("\'"+val+"\'")
#         else:print("result:",val)
#     except SyntaxError:
#         print("SYNTAX ERROR")
        # break
        
    # except Exception:
    #     print("SEMANTIC ERROR")

import ply.lex as lex
from lexer import lexerin

if (len(sys.argv) == 2):
    filePath=sys.argv[1]
    try:
        with open(filePath, 'r') as inputFile:
            data = inputFile.read().replace('\n', '')
        lexerin.input(data)
        while True:
           token = lex.token()
           if not token:
               break
           # print(token)
        head = yacc.parse(data)
        head.eval()
    except SyntaxError:
        print("SYNTAX ERROR")

    except Exception as e:
        print("SEMANTIC ERROR")
else:    
    sys.exit("Argument Error")