import math
import operator as op

# parse

Symbol = str
symbolTable = {}
def Sym(s):
	if s not in symbolTable:
		symbolTable[s] = Symbol(s)

_quote = Sym('quote')
_if = Sym('if')
_set = Sym('set!')
_define = Sym('define')
_lambda = Sym('lambda')
_begin = Sym('begin')
_definemacro = Sym('define-marco')
_quasiquote = Sym('quasiquote')
_unquote = Sym('unquote')
_unquotesplicing = Sym('unquote-solicing')
_checkexpect = Sym('check-expect')
_checkwithin = Sym('check-within')
_member = Sym('member?')
_struct = Sym('struct')

def tokenize(code):
	code = code.replace('(', ' ( ').replace(')', ' ) ')
	code = code.replace('\"', ' \" ').replace(';', ' ;').split()
	return code
def read_from_tokens(tokens):
	if len(tokens) == 0:
		raise SyntaxError('*** Unexpected EOF while reading')

	token = tokens.pop(0)
	
	if '(' == token:
		L = []
		while tokens[0] != ')':
			L.append(read_from_tokens(tokens))
		tokens.pop(0)
		return L

	elif '"' == token:
		L = []
		while tokens[0] != '"':
			L.append(read_from_tokens(tokens))
		end_quote = tokens.pop(0)
		string = token
		string += " ".join(L)
		string += end_quote
		return ["quote", string]

	elif ';' == token:
		L = []
		L.append(token)
		while tokens[0] != '\n':
			L.append(read_from_tokens(tokens))
		new_line = tokens.pop(0)
		L.append(new_line)
		string = " ".join(L)
		return ["quote", string]

	elif ')' == token:
		raise SyntaxError('*** Unexpected ) appears')
	else:
		return atom(token)

def atom(token):
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token)

def parse(code):
	return read_from_tokens(tokenize(code))




# env

class Env(dict):
	def __init__(self, parms = (), args = (), outer = None):
		self.update(zip(parms, args))
		self.outer = outer

	def find(self, var):
		return self if (var in self) else self.outer.find(var)	

def standard_env():
	env = Env()
	env.update(vars(math))
	env.update({
		'+': op.add,
		'-': op.sub,
		'*': op.mul,
		'/': op.truediv,
		'>': op.gt,
		'<': op.lt,
		'>=': op.ge,
		'<=': op.le,
		'=': op.eq,
		'abs': abs,
		'append': op.add,
		'begin': lambda *x: x[-1],
		'car': lambda x: x[0],
		'cdr': lambda x: x[1:],
		'cons': lambda x, y: [x] + y,
		'eq?': op.is_,
		'equal?': op.eq,
		'length': len,
		'list': lambda *x: list(x),
		'list?': lambda x: isinstance(x, list),
		'map': map,
		'max': max,
		'filter': filter,
		'min': min,
		'not': op.not_,
		'null?': lambda x: x == [],
		'number?': lambda x: isinstance(x, Number),
		'procedure?': callable,
		'round': round,
		'symbol?': lambda x: isinstance(x, Symbol)
		})
	return env

global_env = standard_env()

# eval

def eval(x, env = global_env):
	if isinstance(x, Symbol):
		return env.find(x)[x]

	elif not isinstance(x, list):
		return x

	elif x[0] == 'quote':
		(_, exp) = x
		return exp
	
	elif x[0] == 'if':
		(_, test, conseq, alt) = x
		exp = (conseq if eval(test ,env) else alt)
		return eval(exp, env)

	elif x[0] == 'define':
		(_, var, exp) = x
		env[var] = eval(exp, env)

	else:
		proc = eval(x[0], env)
		args = [eval(arg, env) for arg in x[1:]]
		return proc(*args)

# repl
def repl(prompt = '>>>>' ):
	print("laji lisp V1.0. Go go go\n")
	while True:
		i = input(prompt)
		try:
			if i == "quit": break
			val = eval(parse(i))
			print(val)
		except Exception as e:
			print('%s: %s' % (type(e).__name__, e))
repl()
# print(eval(['define', 'x', 10]))