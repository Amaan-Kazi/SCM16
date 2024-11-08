from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
        self.output = []      # Store the generated code lines
        self.symbolTable = {} # Stores variables and their addresses

        self.exprRegisters = ["R9", "R8", "R7", "R6", "R5"]

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
                tokenType, tokenValue = token

                if tokenType == "num":
                    output.append(token)
                elif tokenType == "var":
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
        """
        for token in expression:
            if token.isdigit():  # If the token is an operand (number)
                output.append(token)
            elif token == '(':  # Left parenthesis
                operators.append(token)
            elif token == ')':  # Right parenthesis
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Pop the '(' from the stack
            else:  # Operator
                while (operators and operators[-1] in precedence and
                    (associativity[token] == 'L' and precedence[token] <= precedence[operators[-1]] or
                        associativity[token] == 'R' and precedence[token] < precedence[operators[-1]])):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        return output
        """


    def arithmetic_expr(self, node):
        print(self.infix_to_postfix(node))


    """
    ## Types ##
    def var(self, node):
        register = self.exprRegisters.pop()
        var_name = node[0]

        if not(var_name in self.symbolTable):
            raise ValueError(f"ERROR: Variable {var_name} is not declared")
        else:
            var_address = self.symbolTable[var_name]

        self.output.append(f"\n# {register} = {var_name}")
        self.output.append(f"ILOADI {var_address} 0 {register}")
        return register
    
    def num(self, node):
        register = self.exprRegisters.pop()
        value = node[0]

        self.output.append(f"\n# {register} = {value}")
        self.output.append(f"IADDI {value} 0 {register}")
        return register


    ## Arithmetic ##
    def add(self, node):
        if len(node) < 2:
            raise ValueError(f"Expressions require 2 operands {node}")
        
        register1 = node[0]
        register2 = node[1]

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)

        destRegister = self.exprRegisters.pop()

        self.output.append(f"\n# {destRegister} = {register1} + {register2}")
        self.output.append(f"ADD {register1} {register2} {destRegister}")
        
        return destRegister
    
    def subtract(self, node):
        if len(node) < 2:
            raise ValueError(f"Expressions require 2 operands {node}")
        
        register1 = node[0]
        register2 = node[1]

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)

        destRegister = self.exprRegisters.pop()

        self.output.append(f"\n# {destRegister} = {register1} - {register2}")
        self.output.append(f"SUB {register1} {register2} {destRegister}")
        
        return destRegister

    def multiply(self, node):
        if len(node) < 2:
            raise ValueError(f"Expressions require 2 operands {node}")
        
        register1 = node[0]
        register2 = node[1]

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)

        destRegister = self.exprRegisters.pop()

        self.output.append(f"\n# {destRegister} = {register1} * {register2}")
        self.output.append(f"MUL {register1} {register2} {destRegister}")
        
        return destRegister

    def divide(self, node):
        if len(node) < 2:
            raise ValueError(f"Expressions require 2 operands {node}")
        
        register1 = node[0]
        register2 = node[1]

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)

        destRegister = self.exprRegisters.pop()

        self.output.append(f"\n# {destRegister} = {register1} / {register2}")
        self.output.append(f"DIV {register1} {register2} {destRegister}")
        
        return destRegister

    def modulus(self, node):
        if len(node) < 2:
            raise ValueError(f"Expressions require 2 operands {node}")
        
        register1 = node[0]
        register2 = node[1]

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)

        destRegister = self.exprRegisters.pop()

        self.output.append(f"\n# {destRegister} = {register1} % {register2}")
        self.output.append(f"MOD {register1} {register2} {destRegister}")
        
        return destRegister


    def var_decl(self, node):
        
        data_type = node[0]
        var_name = node[1]
        valueRegister =  "R0"

        if var_name in self.symbolTable:
            raise ValueError(f"ERROR: Variable {var_name} is already declared")

        if len(node) > 2:
            valueRegister = node[2]

        # Comment in assembly
        self.output.append(f"\n# {data_type} {var_name} = {valueRegister}")
        # Decrement Stack Pointer (grows downwards)
        self.stackPointer -= 1
        self.symbolTable[var_name] = self.stackPointer
        # Store initial value on stack pointer
        self.output.append(f"ISTORE {self.stackPointer} {valueRegister} 0")

        if valueRegister != "R0":
            self.exprRegisters.append(valueRegister)

    def assign_stmt(self, node):
        var_name = node[0]
        valueRegister = node[1]

        if not(var_name in self.symbolTable):
            raise ValueError(f"ERROR: Variable {var_name} is not declared")
        else:
            var_address = self.symbolTable[var_name]

        # Comment in assembly
        self.output.append(f"\n# {var_name} = {valueRegister}")
        # Store assigned value to address from symbol table
        self.output.append(f"ISTORE {var_address} {valueRegister} 0")

        self.exprRegisters.append(valueRegister)        
    """

    def generate_code(self):
        # DEBUG: Requires result variable to be declared in code | Displays value of result on R15
        # self.output.append(f"\nILOADI {self.symbolTable["result"]} 0 R15")

        self.output.append("\nHALT 0 0 0\n") # End of program
        return "\n".join(self.output)
