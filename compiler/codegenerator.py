from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
        self.output = []      # Store the generated code lines
        self.symbolTable = {} # Stores variables and their addresses

        self.exprRegisters = ["R9", "R8", "R7", "R6"]

        self.stackPointer = 65535

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

    def generate_code(self):
        # DEBUG: Requires result variable to be declared in code | Displays value of result on R15
        # self.output.append(f"\nILOADI {self.symbolTable["result"]} 0 R15")

        self.output.append("\nHALT 0 0 0\n") # End of program
        return "\n".join(self.output)
