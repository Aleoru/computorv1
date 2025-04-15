import sys
import re

def check_expr(expr:str): #contemplar si pasan = 0 desde el principio
	regex = r" ?[+|-]? ?\d+(\.\d+)? \* X\^\d+ ?"
	regex_empty = r" ?0 ?"

	monos = list()

	if re.match(regex_empty, expr):
		monos.append(expr[0:re.match(regex_empty, expr).span()[1]])
		return monos

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

def my_sqrt(num, precision = 0.00001):
	if num < 0:
		return "Error: Cannot calculate the square root of a negative num"
    
	res = num / 2.0
	while abs(res**2 - num) > precision:
		res = (res + num / res) / 2
    
	return res

def second_grade_equation(monos):
	print(monos)
	a = monos[-1][1]
	b = c = 0
	for mono in monos:
		if mono[0] == 1:
			b = mono[1]
		elif mono[0] == 0:
			c = mono[1]

	print(f"a: {a}, b: {b}, c: {c}")
	dis = b*b - 4*a*c
	print("dis =", dis)

	if dis < 0:
		print("Discriminant is strictly negative, the two complex solutions are:")
		res = my_sqrt(dis * -1)
		print(f"-{b}/{2*a} + {res}i/{2*a}")
		print(f"-{b}/{2*a} - {res}i/{2*a}")
	if dis > 0:
		print("Discriminant is strictly positive, the two solutions are:")
		res = ((-b + my_sqrt(dis) / (2*a)))
		res_neg = ((-b - my_sqrt(dis) / (2*a)))
		print(res)
		print(res_neg)
	if dis == 0:
		res = -b / (2*a)
		print("The solution is:")
		print(res)
	
	return

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

	for list_m in first_monos:
		if list_m[0] in reduced_form:
				reduced_form[list_m[0]] += list_m[1]
		else:
			reduced_form.update({list_m[0]: list_m[1]})

	for list_m in second_monos:
		if list_m[0] in reduced_form:
				reduced_form[list_m[0]] += list_m[1] * -1
		else:
			reduced_form.update({list_m[0]: list_m[1] * -1})
	#print("Res: ", reduced_form)
	sorted_reduced = sorted(reduced_form.items())

	print_reduced_form(sorted_reduced)
	print("Polynomian degree: ", sorted_reduced[-1][0])
	second_grade_equation(sorted_reduced)

if __name__ =="__main__":
	computor()
