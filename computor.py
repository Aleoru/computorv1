import sys
import re

def parse(expr:str):
	regexs = [r" ?[+|-]? ?", 	#sign
			 r"\d+(\.\d+)?",	#coefficient
			 r" \* X\^",		#literal
			 r"\d+"]			#exponent
	
	mono = dict()
	l_expr:int = len(expr)
	key = 0
	value = 0
	end:int = 0

	for regex in regexs:
		span = re.match(regex, expr)
		end = span.span()[1]

	return(mono)

def computor():
	print("Polynom: ", sys.argv[1])
	print("Res: ", parse(sys.argv[1]))

if __name__ =="__main__":
	computor()