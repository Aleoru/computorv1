import sys
import re

def check_expr(expr:str): #contemplar si pasan = 0 desde el principio
	regex = r" ?[+|-]? ?\d+(\.\d+)? \* X\^\d+ ?"
	regex_s = r" ?[+|-] ?\d+(\.\d+)? \* X\^\d+ ?"
	regex_empty = r" ?0 ?"

	monos = list()
	if re.match(regex_empty, expr):
		monos.append(expr[0:re.match(regex_empty, expr).span()[1]])
		return True
	
	first = True
	while len(expr) > 0:
		if first:
			span = re.match(regex, expr)
			first = False
		else:
			span = re.match(regex_s, expr)
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
		elif value <= 0 and key is monos[0][0]:
			print("-", end="")
		elif value <= 0:
			print("- ", end="")
		coef = abs(value) if abs(value) - int(abs(value)) != 0 else int(abs(value))
		print(f"{coef} * X^{key} ", end="")
	print("= 0")
	return 0

def my_sqrt(num, precision = 0.00001):
	if num < 0:
		return "Error: Cannot calculate the square root of a negative num"
    
	res = num / 2.0
	while abs(res**2 - num) > precision:
		res = (res + num / res) / 2
    
	return round(res, 6)

def gcd(a, b):
	while b != 0:
		a, b = b, a % b
    
	return a

def simpl_fraction(num, den, precision:int = 6):
	div = gcd(num, den)
	if div == 1:
		return num, den
	else:
		return round(num/div, 6), round(den/div, 6)

def second_grade_equation(monos):
	a = monos[-1][1]
	b = c = 0
	for mono in monos:
		if mono[0] == 1:
			b = mono[1]
		elif mono[0] == 0:
			c = mono[1]

	dis = b*b - 4*a*c

	if dis < 0:
		print("Discriminant is strictly negative, the two complex solutions are:")
		res = my_sqrt(dis * -1)
		rnum, rden = simpl_fraction(-b, 2*a)
		inum, iden = simpl_fraction(res, 2*a)
		print(f"{(int(rnum))}/{int(rden)} + {int(inum)}i/{int(iden)}")
		print(f"{int(rnum)}/{int(rden)} - {int(inum)}i/{int(iden)}")
	if dis > 0:
		print("Discriminant is strictly positive, the two solutions are:")
		res_neg = (((-b - my_sqrt(dis)) / (2*a)))
		res = (((-b + my_sqrt(dis)) / (2*a)))
		print(round(res_neg if abs(res_neg) - int(abs(res_neg)) != 0 else int(res_neg), 6))
		print(round(res if abs(res) - int(abs(res)) != 0 else int(res), 6))
	if dis == 0:
		res = -b / (2*a)
		print("The solution is:")
		print(res if abs(res) - int(abs(res)) != 0 else int(res))
	
	return

def computor():
	exprs = sys.argv[1].split("=")
	if len(exprs) != 2:
		print("Invalid expression")
		return 1
	monos_f = check_expr(exprs[0])
	monos_s = check_expr(exprs[1])
	if monos_f is False or monos_s is False:
		print("Wrong expression")
		return 1
	
	first_monos = list()
	for mono in monos_f:
		first_monos.append(parse_one_mono(mono))
	if monos_s is not True:
		second_monos = list()
		for mono in monos_s:
			second_monos.append(parse_one_mono(mono))
	
	reduced_form = dict()
	for list_m in first_monos:
		if list_m[0] in reduced_form:
				reduced_form[list_m[0]] += list_m[1]
		else:
			reduced_form.update({list_m[0]: list_m[1]})

	if monos_s is not True:
		for list_m in second_monos:
			if list_m[0] in reduced_form:
					reduced_form[list_m[0]] += list_m[1] * -1
			else:
				reduced_form.update({list_m[0]: list_m[1] * -1})
	sorted_reduced = sorted(reduced_form.items())

	print_reduced_form(sorted_reduced)

	any_sol = True
	for mono in sorted_reduced:
		if mono[1] != 0:
			any_sol = False

	if any_sol:
		print("Any real number is a solution.")
		return
	elif sorted_reduced[-1][0] == 0:
		print("No solution.")
		return

	print("Polynomian degree:", sorted_reduced[-1][0])

	if sorted_reduced[-1][0] > 2:
		print("The polynomial degree is strictly greater than 2, I can't solve.")
	elif sorted_reduced[-1][0] == 2:
		second_grade_equation(sorted_reduced)
	elif sorted_reduced[-1][0] == 1:
		if len(sorted_reduced) == 1:
			print(f"The solution is:\n0")
		else:
			res = (sorted_reduced[0][1] * -1) / sorted_reduced[1][1]
			print(f"The solution is:\n{round(res, 6) if abs(res) - int(abs(res)) != 0 else int(res)}")

if __name__ =="__main__":
	computor()
