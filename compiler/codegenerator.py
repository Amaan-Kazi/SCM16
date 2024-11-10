from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
        self.output = []      # Store the generated code lines
        self.symbolTable = {} # Stores variables and their addresses

        self.exprRegisters = ["R9", "R8", "R7", "R6"]

        self.stackPointer = 65535

    def num(self, node):
        return ('num', int(node[0]))
    def var(self, node):
        return ('var', str(node[0]))

    def infix_to_postfix(self, expression):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
        associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '%': 'L'}
        operations = {"add":"+", "subtract":"-", "multiply":"*", "divide":"/", "modulus":"%"}
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


    def arithmetic_expr(self, node):
        postfix_expr = self.infix_to_postfix(node)

        resultRegister = self.exprRegisters.pop()
        expressionBasePointer = self.stackPointer

        self.output.append(f"\n## EXPRESSION START ##")

        if len(postfix_expr) == 1:
            if postfix_expr[0][0] == "num":
                self.output.append(f"\n# {resultRegister} = {int(postfix_expr[0][1])}")
                self.output.append(f"IADDI 0 {int(postfix_expr[0][1])} {resultRegister}")
            elif postfix_expr[0][0] == "var":
                var_name = str(postfix_expr[0][1])
                if not(var_name in self.symbolTable):
                    raise ValueError(f"ERROR: Variable {var_name} is not declared")
                else:
                    var_address = self.symbolTable[var_name]
                
                self.output.append(f"\n# {resultRegister} = {var_name}")
                self.output.append(f"ILOADI {var_address} 0 {resultRegister}")
        else:
            for token in postfix_expr:
                tokenType, tokenValue = token

                if tokenType == "num":
                    self.stackPointer -= 1
                    self.output.append(f"\n# [{self.stackPointer}] = {tokenValue}")
                    self.output.append(f"ISTOREI {self.stackPointer} {int(tokenValue)} 0")
                elif tokenType == "var":
                    self.stackPointer -= 1
                    tempRegister = self.exprRegisters.pop()
                    var_name = str(tokenValue)

                    if not(var_name in self.symbolTable):
                        raise ValueError(f"ERROR: Variable {var_name} is not declared")
                    else:
                        var_address = self.symbolTable[var_name]

                    self.output.append(f"\n# [{self.stackPointer}] = {var_name}")
                    self.output.append(f"ILOADI {int(var_address)} 0 {tempRegister}")
                    self.output.append(f"ISTORE {self.stackPointer} {tempRegister} 0")

                    self.exprRegisters.append(tempRegister)
                elif tokenType == "operator":
                    register1 = self.exprRegisters.pop()
                    register2 = self.exprRegisters.pop()
                    tempRegister = self.exprRegisters.pop()

                    operations = {"+":"ADD", "-":"SUB", "*":"MUL", "/":"DIV", "%":"MOD"}
                    instruction = operations[tokenValue]

                    self.output.append(f"\n# [{self.stackPointer}] = [{self.stackPointer + 1}] {tokenValue} [{self.stackPointer}]")
                    self.output.append(f"ILOADI {self.stackPointer} 0 {register2}")
                    self.stackPointer += 1
                    self.output.append(f"ILOADI {self.stackPointer} 0 {register1}")
                    
                    self.output.append(f"{instruction} {register1} {register2} {tempRegister}")
                    self.output.append(f"ISTORE {self.stackPointer} {tempRegister} 0")

                    self.exprRegisters.append(tempRegister)
                    self.exprRegisters.append(register2)
                    self.exprRegisters.append(register1)

            self.output.append(f"\n# {resultRegister} = [{self.stackPointer}]")
            self.output.append(f"ILOADI {self.stackPointer} 0 {resultRegister}")
        
        self.output.append(f"\n## EXPRESSION END ##")
        self.stackPointer = expressionBasePointer
        return ("register", str(resultRegister))


    def var_decl(self, node):
        var_type = str(node[0])
        var_name = str(node[1])

        # if no expression given, then value = 0
        if len(node) > 2:
            if (isinstance(node[2], tuple)) and (node[2][0] == "register"):
                register = node[2][1]
                self.stackPointer -= 1
                self.symbolTable[var_name] = self.stackPointer

                self.output.append(f"\n# {var_type} {var_name} = {register}")
                self.output.append(f"ISTORE {self.stackPointer} {register} 0")
                self.exprRegisters.append(register)
            else:
                raise MemoryError("ERROR: expression register not found for var_decl")
        else:
            self.stackPointer -= 1
            self.symbolTable[var_name] = self.stackPointer

            self.output.append(f"\n# {var_type} {var_name} = 0")
            self.output.append(f"ISTOREI {self.stackPointer} 0 0")
    
    def assign_stmt(self, node):
        var_name = str(node[0])

        if (isinstance(node[1], tuple)) and (node[1][0] == "register"):
            register = node[1][1]
            var_address = self.symbolTable[var_name]

            self.output.append(f"\n# {var_name} = {register}")
            self.output.append(f"ISTORE {var_address} {register} 0")
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for var_decl")


    def generate_code(self):
        # DEBUG: Requires result variable to be declared in code | Displays value of result on R15
        self.output.append(f"\n# DEBUG: Load variable result into R15")
        self.output.append(f"ILOADI {self.symbolTable["result"]} 0 R15")

        self.output.append("\nHALT 0 0 0\n") # End of program
        return "\n".join(self.output)
