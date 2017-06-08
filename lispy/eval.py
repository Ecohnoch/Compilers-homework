# Evaluating Module

from parse import *
import math
import operator as op 

# A user-define Scheme procedure
class Procedure(object):
	def __init__(self, parms, body, env):
		self.parms, self.body, self.env = parms, body, env

	def __call__(self, *args):
		return eval(self.body, Env(self.parms, args, self.env))


# An environment: a dict with an outer Env
class Env(dict):
	def __init__(self, parms = (), args = (), outer = None):
		self.update(zip(parms, args))
		self.outer = outer

	# Find the innermost Env where var appears
	def find(self, var):
		return self if (var in self) else self.outer.find(var)

# Manual definition of folder
def foldr(combine, base, lst):
	if len(lst) == 0:
		return base
	else:
		value = combine(lst[0], foldr(combine, base, lst[1:]))
		return value

# Manual definition of foldl
def foldl(combine, acc, lst):
	if len(lst) == 0:
		return acc
	else:
		return _foldl(
				combine,
				combine(acc, lst[0]),
				lst[1:]
			)

# An environment with some Scheme standard procedures
def standard_env():
	env = Env()
	env.update(vars(math))
	env.update({
		'+':op.add,
		'-':op.sub,
		'*':op.mul,
		'/':op.truediv,
		'>':op.gt,
		'<':op.lt,
		'>=':op.ge,
		'<=':op.le,
		'=':op.eq,
		'abs': abs,
        'append': op.add,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x),
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'filter':   filter,
        'foldr':    foldr,
        'foldl':    foldl,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
		})
	return env

global_env = standard_env()

_quote = Sym('quote')
_if = Sym('if')
_set = Sym('set')
_define = Sym('define')
_lambda = Sym('lambda')
_begin = Sym('begin')
_definemacro = Sym('define-macro')
_quasiquote = Sym('quasiquote')
_unquote = Sym('unquote')
_unquotesplicing = Sym('unquote-splicing')
_checkexpect = Sym('check-expect')
_checkwithin = Sym('check-within')
_member = Sym('member?')
_struct = Sym('struct')

# Make predicates and field functions of a user define struce
def make_function(name, param, env  = global_env):
	create = 'make-' + name
	check = name + '?'
	index_array = []
	key_array = []
	i = 0
	for par in param:
		index_array.append(i)
		i += 1
	for par in param:
		key_array.append(name + '-' + per + '-pos')

	env.update(zip(key_array, index_array))

	env[name + '-pos'] = lambda arr, index: arr[index]
	env[check] = lambda arr: len(arr) == eval(create)
	env[create] = len(param)

# Evaluate an expression in an environment
def eval(x, env = global_env):
	if isinstance(x, Symbol):
		return env.find(x)[x]

	elif not isinstance(x, list):
		return x
	elif x[0] == _quote:
		(_, exp) = x
		return exp
	elif x[0] == _if:
		(_, test, conseq, alt) = x
		exp = (conseq if eval(test, env) else alt)
		return eval(exp, env)
	elif x[0] == _define:
		(_, var, exp) = x
		env[var] = eval(exp, env)
	elif x[0] == _set:
		(_, var, exp) = x
		env.find(var)[var] = eval(exp, env)
	elif x[0] == _lambda: 
		(_, parms, body) = x
		return Procedure(parms, body, env)
	elif x[0] == _checkexpect:
		(_, var, exp) = x
		return (eval(var, env) == eval(exp, env))
	elif x[0] == _checkwithin:
		(_, var, lower_bound, upper_bound) = x
		return ((eval(var, env) <= eval(upper_bound, env) and 
			(eval(var, env) >= eval(lower_bound, env))))
	elif x[0] == _member:
		(_, var, lst) = x
		return (eval(var, env) in eval(lst, env))
	elif x[0] == _struct:
		(_, name, params) = x
		make_function(name, params, env)
	else:
		proc = eval(x[0], env)
		if(isinstance(x[0], str) and x[0].startswith('make-')):
			args = [eval(arg, env) for arg in x[2:]]
			if len(args) != proc:
				print('TypeError: '+ x[0] + ' requires %d value, given %d' % (proc, len(args)))
			else:
				env[x[1]] = args
			return
		else:
			args = [eval(arg, env) for arg in x[1:]]
		return proc(*args)


print(eval(parse('(sin (/ 7 8))')))























