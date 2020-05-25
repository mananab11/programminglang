names = [{ }]
functions = {}
#Some code referenced from TT_grammar.py and calculator slide from lectures
class Node:
    def __init__(self):
        # print("")
        self.parent = None
        self.child1=None
        self.child2=None
    def eval(self):
        return 0

class Function_N(Node):
    def __init__(self, name, args, funcblock,expr):
        self.name = name
        self.args = args
        self.block = funcblock
        self.expr = expr
        # print("init function**************",self.name)

    def eval(self):
        # print("adding function to dict",self.name,self)
        functions[self.name] = self
        if not type(self.block) == BlockN:
            raise SyntaxError

class CallFunction_N(Node):
    def __init__(self, funcname, arguments):
        self.name = funcname
        self.args = arguments
    def eval(self):
        if not self.name in functions:
            raise Exception
        func = functions[self.name]
        if not len(func.args) == len(self.args):
            raise Exception
        names.insert(0, {})
        for i in range(len(self.args)):
            names[0][func.args[i]] = self.args[i].eval()
        func.block.eval()
        return_value = func.expr.eval()

        names.pop(0)
        return return_value

lst=[int,str,bool,float]
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
        # print("exception here")
        raise Exception
        # print("exception raised")

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
        # print("ComparisonNode initialize exiting",self.value1,self.condition,self.value2)

    def eval(self):
        # print("error line",self.value1,self.value2)
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
        # print("ComparisonNode eval exiting")

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
        # print("here")
    def eval(self):
        idx=self.index.eval()
        lst=self.list.eval()
        if(type(idx)!=int) or idx>len(lst)-1 or len(lst)<1 or idx<0:
            # print("here")
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

class AssignN(Node):
    def __init__(self,name,value):
        self.var=name
        self.expr=value
        # print("value assigned to node",self.var," = ",self.expr)

    def eval(self):
        result = self.expr.eval()
        # print("assign eval called ++++++++++++++++:",self.var,result)
        if result is None:
            raise Exception
        else:
            for i in range(len(names)):
                if self.var.name in names[i]:
                    names[i][self.var.name] = self.expr.eval()
                    return
            names[0][self.var.name] = self.expr.eval()
        # print("in assign","left : ",self.name," = ",self.value.eval())
        # if type(self.value) in lst:
        #     names[self.name.value]=self.value
        # else:
        #     names[self.name.value]=self.value.eval()

class AssignListN(Node):
    def __init__(self, name, index, value):
        self.name = name
        self.value = value
        self.index = index

    def eval(self):        
        present = False
        scope = 0
        # print("assign list called")
        for i in range(len(names)):
            if self.name in names[i]:
                var_val = names[i][self.name]                
                scope = i
                present = True
                break
        if not present:
            raise Exception
        try:
            temp = var_val
            indices=[self.index.eval()]            
            for i in indices[:-1]:
                temp = temp[i]
            temp[indices[-1]] = self.value.eval()
        except IndexError:
            raise Exception
        names[scope][self.name] = var_val

class BlockN(Node):
    def __init__(self,value):
        self.statement_lst=value

    def eval(self):
        for statement in self.statement_lst:
            # print("statement",statement)
            statement.eval()

class PrinterN(Node):
    def __init__(self,value):
        self.value= value

    def eval(self):
        if type(self.value) in lst:
            print(self.value)
        else:
            # print("in printer value :",self.value)
            print(self.value.eval())
                 
        # try:
        #     print(self.value.eval())
        # except:
        #     print(self.value)

class IFELSENode(Node):
    def __init__(self,condition,if_block,else_block):
        self.condition=condition
        self.if_block=if_block
        self.else_block=else_block

    def eval(self):
        if self.condition.eval() is True:
            self.if_block.eval()
        else:
            self.else_block.eval()

class IFNode(Node):
    def __init__(self,condition,block):
        self.condition=condition
        self.block=block
    def eval(self):
        if self.condition.eval() is True:
            self.block.eval()

class WhileNode(Node):
    def __init__(self,condition,block):
        self.condition=condition
        self.block=block
    def eval(self):
        if type(self.condition)==bool:
            while(self.condition is True):
                self.block.eval()
        else:
            while(self.condition.eval() is True):
                self.block.eval()

        # try:
        #     while(self.condition.eval() is True):
        #         self.block.eval()
        # except:
            # while(self.condition is True):
            #     self.block.eval()

class IdentiferN(Node):
    def __init__(self,value):
        self.name=value
        # print("identifier init***",self.name)
    def eval(self):
        # return names[self.value]
        for i in range(len(names)):
            if self.name in names[i]:
                return names[i][self.name]

        return None

