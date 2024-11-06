from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
        self.output = []      # Store the generated code lines
        self.symbolTable = {} # Stores variables and their addresses

        self.stackPointer = 65535

    def var_decl(self, node):
        data_type = node[0]
        var_name = node[1]
        initial_value =  0

        if var_name in self.symbolTable:
            raise ValueError(f"ERROR: Variable {var_name} is already declared")

        # int a = 5 (initial value = 5) | int a (initial value = 0)
        if len(node) > 2:
            initial_value = int(node[2])

        # Comment in assembly
        self.output.append(f"\n# {data_type} {var_name} = {initial_value}")
        # Decrement Stack Pointer (grows downwards)
        self.stackPointer -= 1
        self.symbolTable[var_name] = self.stackPointer
        # Store initial value on stack pointer
        self.output.append(f"ISTOREI {self.stackPointer} {initial_value} 0")

    def assign_stmt(self, node):
        var_name = node[0]
        value = node[1]

        if not(var_name in self.symbolTable):
            raise ValueError(f"ERROR: Variable {var_name} is not declared")
        else:
            var_address = self.symbolTable[var_name]

        # Comment in assembly
        self.output.append(f"\n# {var_name} = {value}")
        # Store assigned value to address from symbol table
        self.output.append(f"ISTOREI {var_address} {value} 0")

    def generate_code(self):
        return "\n".join(self.output)
