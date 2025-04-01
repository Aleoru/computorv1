import sys
import re

def check_expr(expr:str):
	regex = r" ?[+|-]? ?\d+(\.\d+)? \* X\^\d+ ?"

	monos = list()

	while len(expr) > 0:
		span = re.match(regex, expr)
		if span is None:
			return (False)
		pos = span.span()[1]
		monos.append(expr[0:pos])
		expr = expr[pos:len(expr)]

	return monos

def parse(expr:str):
	regexs = [r" ?[+|-]? ?", 	#sign
			 r"\d+(\.\d+)?",	#coefficient
			 r" \* X\^",		#literal
			 r"\d+"]			#exponent
	
	res = list()

	for regex in regexs:
		span = re.match(regex, expr)
		pos = span.span()[1]
		if len(res) % 2:
			if len(res) == 1:
				res.append(float(res[0] + expr[0:pos]))
			else:
				res.append(int(expr[0:pos]))
		else:
			res.append(expr[0:pos])
		expr = expr[pos:len(expr)]

	mono = {res[3] : res[1]}

	return(mono)

def computor():
	exprs = sys.argv[1].split("=")
	if len(exprs) == 2:
		monos_f = check_expr(exprs[0])
		monos_s = check_expr(exprs[1])
	else:
		print("Invalid expression")
		return 1
	print("Polynom: ", sys.argv[1])
	if check_expr(exprs[0]) and check_expr(exprs[1]):
		print("Res: ", parse(monos_f[0]))
	else:
		print("Wrong expression")
		return 1

if __name__ =="__main__":
	computor()