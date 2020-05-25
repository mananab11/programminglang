import ply.yacc as yacc
from lexer import tokens
import sys
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
# dictionary of names (for storing variables)
names = { }

#Some code referenced from TT_grammar.py and calculator slide from lectures
class Node:
    def __init__(self):
        # print("")
        self.parent = None
        self.child1=None
        self.child2=None
    def eval(self):
        return 0

class BinaryOpN(Node):
    def __init__(self,value1,operator,value2):
        super().__init__()
        self.type = "binop"
        self.value1=value1
        self.value2=value2
        self.operator=operator
        # print("BinaryOpN node",value1,value2,operator)

    def eval(self):
        # print("calculating node",self.value1,self.value2,self.operator)
        eval1=self.value1.eval()
        eval2=self.value2.eval()
        if (self.operator == '+'):
            if(type(eval1)!=tuple and type(eval2)!=tuple):
                if(type(eval1)==type(eval2)) or self.Checkhelper(eval1,eval2):
                    return eval1 +eval2
        elif (self.operator == '-'):
            if self.Checkhelper(eval1,eval2):
                return eval1-eval2
        elif (self.operator == '*'):
            if self.Checkhelper(eval1,eval2):
                return eval1*eval2
        elif (self.operator == '**'):
            if self.Checkhelper(eval1,eval2):
                return eval1**eval2
        elif (self.operator == '/'):
            if self.Checkhelper(eval1,eval2) and eval2!=0:
                return eval1/eval2
        elif (self.operator == 'mod') and eval2!=0:
            if self.divmodTypeCheck(eval1,eval2):
                return eval1%eval2
        elif (self.operator == 'div') and eval2!=0:
            if self.divmodTypeCheck(eval1,eval2):
                return eval1//eval2
        raise Exception

    def Checkhelper(self,value1,value2):
        cond=((type(value1)==int and (type(value2)==int or type(value2)==float)) or (type(value1)==float and (type(value2)==int or type(value2)==float))) 
        flag=cond and (type(value1)!=bool or type(value2)!=bool)
        # print("checkhelper",flag)
        return flag
    def divmodTypeCheck(self,val1,val2):
        return type(val1)==int and type(val2)==int

class ComparisonN(Node):
    def __init__(self,val1,comparator,val2):
        super().__init__()
        self.type = "Comparison"
        self.value1=val1
        self.value2=val2
        self.condition=comparator

    def eval(self):
        eval1=self.value1.eval()
        eval2=self.value2.eval()
        if (self.condition == 'andalso'):
            return eval1 and eval2
        elif (self.condition == 'orelse'):
            return eval1 or eval2
        elif (self.condition == 'in'):
            return eval1 in eval2
        if self.CheckComparisonValid(eval1,eval2) is False:
            raise Exception
        elif (self.condition == '<'):
            return eval1 < eval2
        elif (self.condition == '<='):
            return eval1 <= eval2
        elif (self.condition == '=='):
            return eval1 == eval2
        elif (self.condition == '>'):
            return eval1 > eval2
        elif (self.condition == '>='):
            return eval1 >= eval2
        elif (self.condition == '<>'):
            return eval1 != eval2

    def CheckComparisonValid(self,val1,val2):
        cond=((type(val1)==int and (type(val2)==int or type(val2)==float)) or (type(val1)==float and (type(val2)==int or type(val2)==float))) 
        flag=cond or (type(val1)==str and type(val2)==str)
        # print("ComparisonNnode",flag)
        return flag

class UMinusN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "UMINUS"
        self.value=value.eval()

    def eval(self):
        # print("in_uminus",self.value)
        return self.value *-1

class StringIndexN(Node):
    def __init__(self,value,index):
        super().__init__()
        self.type = "StringIndexing"
        self.stringVal=value.eval()
        self.index=index.eval()
    def eval(self):
        if(type(self.index)!=int) or self.index>len(self.stringVal):
        # print("error found",type(p[3]))
            raise Exception
        return self.stringVal[self.index]
class NumbersN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "NumberNode"
        self.number=value

    def eval(self):
        # print("number  eval",self.number)
        return self.number

class StringN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "StringNode"
        self.stringVal=value
    def eval(self):
        # print("string is ",type(self.stringVal))
        return self.stringVal


class NamesN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "NameNode"
        self.name=value

    def eval(self):
        return names[self.name]

class NotBoolN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "NegationBool"
        self.value=value
        # print('notBoolnode_init',self.value)

    def eval(self):
        # print('notBoolnode_eval',self.value)
        eval1=self.value.eval()
        if type(eval1)==bool:
            return not self.value.eval()
        raise Exception

class ListN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "ListNode"
        self.list=[value]
    def eval(self):
        lst = list()
        for item in self.list:
            try:
                lst.append(item.eval())
            except:
                lst.append(item)
        return lst

class TupleN(Node):
    def __init__(self, value):
        super().__init__()
        self.type = "TupNode"
        self.value = [value]

    def eval(self):
        allval=[]
        for vals in self.value:
            allval.append(vals.eval())
        # print("values",self.eval())
        return tuple(allval)

class EmptyListN(Node):
    def __init__(self):
        super().__init__()
        self.type = "EmptyListNode"
        self.list = list()
    def eval(self):
        return self.list

class IndexListN(Node):
    def __init__(self, listv, index):
        super().__init__()
        self.type = "IndexListNode"
        self.list = listv
        self.index = index
    def eval(self):
        idx=self.index.eval()
        if(type(idx)!=int):
            raise Exception
        return self.list.eval()[idx]

class TupleIndexN(Node):
    def __init__(self, value1, value2):
        super().__init__()
        self.type = "TupleIndexing"
        self.value1 = value1 #tuple
        self.value2 = value2 #index only int allowed not any expression

    def eval(self):
        tupl = self.value1.eval()
        index = self.value2
        if type(index)!=int or (len(tupl)<=1):
            raise Exception
        if(index<1 or index>len(tupl)): #index starts from 1
            raise Exception
        return tupl[index - 1]

class DoubleIndexListN(Node):
    def __init__(self, listv, index1, index2):
        super().__init__()
        self.type = "DoubleIndexingg"
        self.list = listv
        self.index1 = index1
        self.index2 = index2
    def eval(self):
        idx1=self.index1.eval()
        idx2=self.index2.eval()
        lst=self.list.eval()
        if type(idx1)!=int or type(idx2)!=int:
            raise Exception
        return lst[idx1][idx2]

class BooleanN(Node):
    def __init__(self,value):
        super().__init__()
        self.type = "BoolNode"
        self.boolVal=value

    def eval(self):
        return self.boolVal

class ConsN(Node):
    def __init__(self,index,value):
        super().__init__()
        self.type = "ConsOpNode"
        self.index=index
        self.list=value

    def eval(self):
        idx=self.index.eval()
        lst=self.list.eval()
        return [idx]+lst

def p_statement_expr(p):
    'statement : expression'
    # print("ia m here")
    # print(p[1])
    p[0]=p[1]
lst_ops=['+','-','*','/','mod','**','div']
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
    if len(p)==4 and p[2] in lst_ops:
        # print("yeah")
        p[0]=BinaryOpN(p[1],p[2],p[3])  

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
    p[0]=ComparisonN(p[1],p[2],p[3])

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    if p[1]=='True' : p[0] =BooleanN(True)#True 
    elif p[1] == 'False' : p[0]=BooleanN(False)#False

def p_notExpression(p):
    'expression : NOT expression'
    # p[0]=not p[2]
    p[0]=NotBoolN(p[2])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    # p[0] = -p[2]
    # print("UMinusN")
    p[0]=UMinusN(p[2])

def p_expression_str(p):
    'expression : STRING'
    # p[0]=p[1]
    # print("stringgrammar")
    p[0]=StringN(p[1])

def p_expression_number(p):
    '''expression : REAL
                  | INTEGER
                  '''
    # p[0]=p[1]
    # print("number  grammar",p[1])
    p[0]=NumbersN(p[1])

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
    p[0]=ListN(p[1])

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
    p[0]=EmptyListN()

def p_exp_con_OP(p):
    'expression : expression CONS expression'
    # if(type([p[1]])!=type(p[3])):
        # raise Exception
    # else:
    # print("inconsls")
    p[0]=ConsN(p[1],p[3])

def p_expListIndex(p):
    'expression : LIST LBRACKET expression RBRACKET'
    # print(p[3])
    # if(type(p[3])!=int):
    #     raise Exception
    # p[0]=p[1][p[3]]
    p[0]=IndexListN(p[1],p[3])

def p_exp_str_index(p):
    'expression : STRING LBRACKET expression RBRACKET'
    # if(type(p[3])!=int):
    #     print("error found",type(p[3]))
    #     raise Exception
    # p[0]=p[1][p[3]]
    ####check again
    stringNode=StringIndexN(StringN(p[1]),p[3])
    p[0]=stringNode

def p_expListIndex_DoubleIndex(p):
    'expression : LIST LBRACKET expression RBRACKET LBRACKET expression RBRACKET'
    # if(type(p[1][p[3]])!=list):
    #     raise Exception
    # if(type(p[1].eval()[p[3].eval()])!=list):
    #     raise Exception
    # p[0]=p[1][p[3]][p[6]]
    p[0]=DoubleIndexListN(p[1],p[3],p[6])

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
    p[0]=TupleN(p[1])


def p_in_tuple_COMMA_exp(p):
    'inside_tuple : inside_tuple COMMA expression'
    # if len(p)==4:p[1].value.append(p[3])
    p[1].value.append(p[3])
    p[0]=p[1]

def p_tupleIndex(p):
    'expression  : HASH INTEGER TUPLE'
    p[0]=TupleIndexN(p[3],p[2])

def p_expression_name(p):
    'expression : IDENTIFIER'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0
        raise Exception

def p_error(p):
    # print(f"Syntax error at {p.value!r}")
    raise SyntaxError

yacc.yacc(debug=False)
if len (sys.argv)!=2:
    print("Invalid Parameters")
else:
    filePath=sys.argv[1]
    fileStream=open(filePath,'r')
    for line in fileStream:
        try:
            rootNode=yacc.parse(line)
            result=rootNode.eval()
            if type(result) is str:print("\'"+result+"\'")
            else:print(result)
        except SyntaxError:
            print("SYNTAX ERROR")
        except Exception:
            print("SEMANTIC ERROR")
            continue
    



