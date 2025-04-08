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

def parse_one_mono(expr:str):
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
			res.append(re.sub(" ", "", expr[0:pos]))
		expr = expr[pos:len(expr)]

	mono = [res[3],res[1]]

	return(mono)

def print_reduced_form(monos:dict):
	print("Reduced form: ", end="")
	for key,value in monos:
		if value >= 0 and key is not monos[0][0]:
			print("+ ", end="")
		elif value <= 0:
			print("- ", end="")
		print(f"{abs(value)} * X^{key} ", end="")
	print("= 0")
	print(monos)
	return 0
	

def computor():
	exprs = sys.argv[1].split("=")
	if len(exprs) != 2:
		print("Invalid expression")
		return 1
	monos_f = check_expr(exprs[0])
	monos_s = check_expr(exprs[1])
	#print("Polynom: ", sys.argv[1])
	if check_expr(exprs[0]) is False or check_expr(exprs[1]) is False:
		print("Wrong expression")
		return 1
	
	first_monos = list()
	for mono in monos_f:
		first_monos.append(parse_one_mono(mono))
	#print("Res: ", first_monos)
	second_monos = list()
	for mono in monos_s:
		second_monos.append(parse_one_mono(mono))
	reduced_form = dict()

	for lista in first_monos:
		if lista[0] in reduced_form:
				reduced_form[lista[0]] += lista[1]
		else:
			reduced_form.update({lista[0]: lista[1]})

	for lista in second_monos:
		if lista[0] in reduced_form:
				reduced_form[lista[0]] += lista[1] * -1
		else:
			reduced_form.update({lista[0]: lista[1] * -1})
	#print("Res: ", reduced_form)
	sorted_reduced = sorted(reduced_form.items())

	print_reduced_form(sorted_reduced)
	print("Polynomian degree: ", sorted_reduced[-1][0])

if __name__ =="__main__":
	computor()
