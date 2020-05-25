import ply.lex as lex
tokens=[
"IDENTIFIER",
"PLUS","MINUS","TIMES","DIVIDE","DIV",'EXPONENTIAL',
'EQUALS',
"INTEGER","REAL",
'LESSTHAN','LESSTHANEQUAL','EQUALTO','NOTEQUALTO','GREATERTHAN','GREATERTHANEQUAL',
'LPAREN','RPAREN','LBRACKET','RBRACKET',
'STRING','COMMA','HASH','CONS','LBRACE','RBRACE','SEMICOLON'
]
reserved={
'True':'TRUE',
'False':'FALSE',
'in':'IN','not':'NOT',
'andalso':'ANDALSO','orelse':'ORELSE',
'while':'WHILE','if':'IF','else':'ELSE','print':'PRINT','fun':'FUN','mod':'MOD'
}
tokens +=  list(reserved.values())

t_ignore=' \t\n'

t_PLUS=r'\+'
t_TIMES=r'\*'
t_DIVIDE=r'/'
t_EXPONENTIAL=r'\*{2}'


t_EQUALS=r'='
t_CONS=r'::'

t_LESSTHAN=r'<'
t_LESSTHANEQUAL=r'<='
t_EQUALTO=r'=='
t_NOTEQUALTO=r'<>'
t_GREATERTHAN=r'>'
t_GREATERTHANEQUAL=r'>='

t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LBRACKET=r'\['
t_RBRACKET=r'\]'

t_COMMA=r'\,'
t_HASH=r'\#'
t_LBRACE=r'{'
t_RBRACE=r'}'
t_SEMICOLON=r';'
# t_PRINT=r'print'
# t_IF=r'if'
# t_ELSE=r'else'
# t_WHILE=r'while'
# t_CONS=r'::'

# t_REAL=r'[0-9]*[\.]([0-9]+)?'
# t_INTEGER=r'[0-9]+'
# t_NUMBER = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
#t_NUMBER = r'(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'

#checking validity of varible by checking if it is not a reserved word
# def t_MOD(t):
# 	r'mod'
# 	return t
def t_DIV(t):
	r'div'
	return t
from ast import IdentiferN
def t_IDENTIFIER(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	# r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type=reserved.get(t.value,'IDENTIFIER')
	if t.type=='IDENTIFIER':
		t.value=t.value
		# t.value=IdentiferN(t.value)
	return t

def t_STRING(t):
	# r'(["][\sa-zA-Z0-9_-]*["])|([\'][\sa-zA-Z0-9_-]*[\'])'
	r'\'[^\']*\'|\"[^\"]*\"'
	# print(t.value)
	t.value=str((t.value)[1:-1])
	# print(t.value)
	return t

def t_TRUE(t):
	r'True'
	t.value=True
	return t

def t_FALSE(t):
	r'False'
	t.value=False
	return t

def t_MINUS(t):
	r'\-'
	return t

def t_REAL(t):
	# r'[0-9]*[\.]([0-9]+)?'
	# r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
	# r'[-]?(\d+(\.\d*)|\.\d+)([eE][+-]?\d+)?'
	r'[-]?(\d+(\.\d*)|\.\d+)([eE][+-]?\d+)?'
	# print(t.value)
	try:
		t.value=float(t.value)
		t.type='REAL'
	except ValueError:
		t.value=0
	return t

def t_INTEGER(t):
	r'[0-9]+'
	try:
		t.value=int(t.value)
		t.type='INTEGER'
	except ValueError:
		t.value=0
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    raise SyntaxError



lexerin=lex.lex()
# if __name__ == '__main__':
#     # lex.runmain()
# 	# lex.input("'ass' 3 not 4 [False,True,24,22,'dd','$2asd',5.05e+5,True,] (2,3,True,False,'true',-5e-10)")
# 	lex.input('print(2)')
# 	while True:
# 		tok=lex.token()
# 		if not tok:
# 			break
# 		print(tok.value)
# 		print(tok.type)

