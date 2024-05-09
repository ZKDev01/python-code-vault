import pprint
import sys

def parse(s):
    
    curr = [0]
    def FACT():
        if s[curr[0]] == "(":
            curr[0] += 1
            expr = EXPR()
            if s[curr[0]] == ")":
                curr[0] += 1
                return expr
        elif s[curr[0]].isnumeric():
            num = s[curr[0]]
            curr[0] += 1
            return {"t":"num", "val": num}
        else:
            print("Expresion mal formada")
            sys.exit()

    def TERM():
        expr = FACT()
        if len(s[curr[0]:]) > 0 and s[curr[0]] == "*":
            curr[0] += 1
            return {"t":"mul", "expr1":expr, "expr2":TERM()}
        else:
            return expr

    def EXPR():
        expr = TERM()
        if len(s[curr[0]:]) > 0 and s[curr[0]] == "+":
            curr[0] += 1
            return {"t":"sum", "expr1":expr, "expr2":EXPR()}
        else:
            return expr
    
    ast = EXPR()

    if len(s) == curr[0]:
        return ast
    else:
        print("Expresion mal formada")
        sys.exit()

pprint.pprint (parse("1+2*"))
pprint.pprint (parse("1*2+3"))
pprint.pprint (parse("1*(2+3)"))
pprint.pprint (parse("(((1)))"))
pprint.pprint (parse("1"))