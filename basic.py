from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data

def doPrint(toPrint):
	if toPrint[0:6] == "STRING":
		toPrint = toPrint[10:]
		toPrint = toPrint[:-1]
	elif toPrint[0:3] == "NUM":
		toPrint = toPrint[6:]
	elif toPrint[0:4] == "EXPR":
		toPrint = evalExpress(toPrint[7:])

	print toPrint

def evalExpress(expr):
	# expr = "," + expr

	# i = len(expr) - 1
	# num = ""

	# while i >= 0:
	# 	if expr[i] == "+" or expr[i] == "-" or expr[i] == "*" or expr[i] == "/" or expr[i] == "%":
	# 		num = num[::-1]
	# 		num_stack.append(num)
	# 		num_stack.append(expr[i])
	# 		num = ""
	# 	elif expr[i] == ",":
	# 		num = num[::-1]
	# 		num_stack.append(num)
	# 		num = ""
	# 	else:
	# 		num += expr[i]
	# 	i -= 1
	# print num_stack
	return eval(expr)

def doAssign(varname, value):
	symbols[varname[6:]] = value

def getVariable(varname):
	if varname in symbols:
		return symbols[varname]
	else:
		return "Variable Error : Undefined Variable"


def lax(filecontents):
	tok = ""
	state = 0
	varStarted = 0
	isexpr = 0
	var = ""
	expr = ""
	string = ""
	n = 0
	filecontents = list(filecontents)

	for char in filecontents:
		tok += char
		
		if tok == " ":
			if state == 0:
				tok = ""
			elif state == 1:
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR : " + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM : " + expr)
			elif var != "":
				tokens.append("VAR : " + var)
				var = ""
				varStarted = 0
			tok = ""
		elif tok == "=" and state == 0:
			if var != "":
				tokens.append("VAR : " + var)
				var = ""
				varStarted = 0
			tokens.append("EQUALS")
			tok = ""
			
		elif tok == "$" and state == 0:
			varStarted = 1
			var += tok
			tok = ""
		elif varStarted == 1:
			if tok == "<" or tok == ">":
				if var != "":
					tokens.append("VAR : " + var)
					var = ""
					varStarted = 0
			var += tok
			tok = ""

		elif tok == "PRINT" or tok == "print":
			tokens.append("PRINT")
			tok = ""

		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			expr += tok
			tok = ""

		elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
			isexpr = 1
			expr += tok
			tok = ""

		# "" as switch
		elif tok == "\"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING : " + string + "\"")
				string = ""
				state = 0
				tok = ""

		elif state == 1:
			string += tok
			tok = ""
	return tokens

def parse(toks):
	i = 0
	while i < len(toks):
		if toks[i] + " " + toks[i + 1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i + 1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i + 1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i + 1][0:3] == "PRINT VAR":
			if toks[i + 1][0:6] == "STRING":
				doPrint(toks[i + 1])
			elif toks[i + 1][0:3] == "NUM":
				doPrint(toks[i + 1])
			elif toks[i + 1][0:4] == "EXPR":
				doPrint(toks[i + 1])
			elif toks[i + 1][0:3] == "VAR":
				doPrint(getVariable(toks[i + 1][6:]))
			i += 2

		elif toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:4] == "VAR EQUALS EXPR": 
			if toks[i + 2][0:6] == "STRING":
				doAssign(toks[i], toks[i + 2])
			elif toks[i + 2][0:3] == "NUM":
				doAssign(toks[i], toks[i + 2])
			elif toks[i + 2][0:4] == "EXPR":
				doAssign(toks[i], "NUM : " + str(evalExpress(toks[i + 2][7:])))
			i += 3

def run():
	data = open_file(argv[1])
	toks = lax(data)
	parse(toks)

run()