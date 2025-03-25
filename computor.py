import sys
import re

def parse(exp):
    regex = [r"[+-]? ?", #sign
             r"\d"]
    res = re.find(exp, bar)
    return(res)

def computor():
    print("Polynom: ", sys.argv[1])
    print("Res: ", parse(sys.argv[1]))

if __name__ =="__main__":
    computor()