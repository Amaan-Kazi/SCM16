# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


def infix_to_postfix(self: "CodeGenerator", expression):
    precedence = {
        '*':  3, '/':  3, '%': 3,
        '+':  2, '-':  2,
        '==': 1, '!=': 1,
        '<':  1, '<=': 1,
        '>':  1, '>=': 1,
        '&&': 0, '||': 0
    }
    
    associativity = {
        '*':  'L', '/':  'L', '%': 'L',
        '+':  'L', '-':  'L',
        '==': 'L', '!=': 'L',
        '<':  'L', '<=': 'L',
        '>':  'L', '>=': 'L',
        '&&': 'L', '||': 'L'
    }

    operations = {
        "multiply":     "*",  "divide":                "/", "modulus": "%",
        "add":          "+",  "subtract":              "-",
        "equal":        "==", "not_equal":             "!=",
        "lesser_than":  "<",  "lesser_than_or_equal":  "<=",
        "greater_than": ">",  "greater_than_or_equal": ">=",
        "logical_and":  "&&", "logical_or":            "||"
    }

    output = []
    operators = []

    for token in expression:
        if isinstance(token, tuple):
            output.append(token)
        else:
            if token.data == "left_parenthesis":
                # start of sub expression
                operators.append("(")
            elif token.data == "right_parenthesis":
                # end of sub expression
                # while operators stack not empty and last operator not (
                while operators and operators[-1] != "(":
                    output.append( ("operator", operators.pop()) )
                operators.pop() # pop ( from stack
            else:
                tokenData = operations[token.data]

                while (operators and operators[-1] in precedence and
                    (associativity[tokenData] == 'L' and precedence[tokenData] <= precedence[operators[-1]] or
                    associativity[tokenData] == 'R' and precedence[tokenData] < precedence[operators[-1]])):
                    output.append( ("operator", operators.pop()) )
                operators.append(tokenData)
    
    while operators:
        output.append( ("operator", operators.pop()) )

    return output

def expression(self: "CodeGenerator", node):
    postfix_expr = self.infix_to_postfix(node)

    resultRegister = self.exprRegisters.pop()
    expressionBasePointer = self.stackPointer

    symbols = {
        "multiply":     "*",  "divide":                "/", "modulus": "%",
        "add":          "+",  "subtract":              "-",
        "equal":        "==", "not_equal":             "!=",
        "lesser_than":  "<",  "lesser_than_or_equal":  "<=",
        "greater_than": ">",  "greater_than_or_equal": ">=",
        "logical_and":  "&&", "logical_or":            "||",
        "left_parenthesis": "(", "right_parenthesis": ")"
    }

    infixExpr = ''

    for exprToken in node:
        if isinstance(exprToken, tuple):
            infixExpr += str(exprToken[1]) + ' '
        else:
            infixExpr += symbols[str(exprToken.data)] + ' '

    self.comment(f"# EXPRESSION [ {infixExpr}]: ")
    self.indent()

    if len(postfix_expr) == 1:
        if postfix_expr[0][0] == "num":
            self.comment(f"# {resultRegister} = {int(postfix_expr[0][1])}")
            self.code(f"IADDI 0 {int(postfix_expr[0][1])} {resultRegister}")
        elif postfix_expr[0][0] == "var":
            var_name = str(postfix_expr[0][1])
            var_address = self.get_variable_address(var_name)
            
            self.comment(f"# {resultRegister} = {var_name}")
            self.code(f"ILOADI {var_address} 0 {resultRegister}")
    else:
        for token in postfix_expr:
            tokenType, tokenValue = token

            if tokenType == "num":
                self.stackPointer -= 1
                self.comment(f"# [{self.stackPointer}] = {tokenValue}")
                self.code(f"ISTOREI {self.stackPointer} {int(tokenValue)} 0", newLine2=True)
            elif tokenType == "var":
                self.stackPointer -= 1
                tempRegister = self.exprRegisters.pop()

                var_name = str(tokenValue)
                var_address = self.get_variable_address(var_name)

                self.comment(f"# [{self.stackPointer}] = {var_name}")
                self.code(f"ILOADI {int(var_address)} 0 {tempRegister}")
                self.code(f"ISTORE {self.stackPointer} {tempRegister} 0", newLine2=True)

                self.exprRegisters.append(tempRegister)
            elif tokenType == "operator":
                register1 = self.exprRegisters.pop()
                register2 = self.exprRegisters.pop()
                tempRegister = self.exprRegisters.pop()

                operations = {
                    "*":  "MUL",  "/":  "DIV", "%":"MOD",
                    "+":  "ADD",  "-":  "SUB",
                    "==": "BEQ",  "!=": "BNE",
                    "<":  "BLTU", "<=": "BLEU",
                    ">":  "BGTU", ">=": "BGEU",
                    "&&": "LAND", "||": "LOR"
                }

                instruction = operations[tokenValue]

                self.comment(f"# [{self.stackPointer}] = [{self.stackPointer + 1}] {tokenValue} [{self.stackPointer}]")
                self.code(f"ILOADI {self.stackPointer} 0 {register2}")
                self.stackPointer += 1
                self.code(f"ILOADI {self.stackPointer} 0 {register1}")
                
                self.code(f"{instruction} {register1} {register2} {tempRegister}")
                self.code(f"ISTORE {self.stackPointer} {tempRegister} 0", newLine2=True)

                self.exprRegisters.append(tempRegister)
                self.exprRegisters.append(register2)
                self.exprRegisters.append(register1)

        self.comment(f"# {resultRegister} = [{self.stackPointer}]")
        self.code(f"ILOADI {self.stackPointer} 0 {resultRegister}")
    
    self.unindent()
    self.comment(f"# END EXPRESSION [ {resultRegister} ]", newLine2=True)

    self.stackPointer = expressionBasePointer
    return ("register", str(resultRegister))
