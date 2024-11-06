from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
        self.output = []      # Store the generated code lines
        self.symbolTable = {} # Stores variables and their addresses

        self.stackPointer = "R1"
        self.basePointer = "R2"
        self.heapPointer = "R3"
        self.addressRegister = "R15"

        self.output.append(f"\n# Initialize Stack Pointer")
        self.output.append(f"ADDI R0 65535 {self.stackPointer}")

    def var_decl(self, node):
        data_type = node[0]
        var_name = node[1]
        initial_value =  0

        # int a = 5 (initial value = 5) | int a (initial value = 0)
        if len(node) > 2:
            initial_value = int(node[2])

        # Comment in assembly
        self.output.append(f"\n# {data_type} {var_name} = {initial_value}")
        # Decrement Stack Pointer (grows downwards)
        self.output.append(f"SUBI {self.stackPointer} 1 {self.stackPointer}")
        self.symbolTable[var_name] = self.stackPointer
        # Address Register = Stack Pointer
        self.output.append(f"ADDI {self.stackPointer} 0 {self.addressRegister}")
        # Store initial value on address pointed by Address Register
        self.output.append(f"STOREI {self.addressRegister} {initial_value} 0")

    def assign_stmt(self, node):
        var_name = node[0]
        value = node[1]




    def generate_code(self):
        return "\n".join(self.output)


"""
Register	Role	                            Description
R0	        Zero Register	                    Always holds the value 0 (constant zero).
R1	        Stack Pointer (SP)	                Points to the top of the stack. Decrements to allocate, increments to deallocate.
R2	        Base Pointer (BP)	                Points to the base of the current stack frame, enabling local variable access.
R3	        Heap Pointer (HP)	                Points to the base of the heap, used for global or dynamically allocated data.
R4-R7	    Argument/Parameter Registers	    Used to pass up to 4 arguments to functions.
R8-R11	    Return Value/Temporary Registers	Used for return values and temporary computation within functions.
R12	        Return Address Register (RA)	    Stores the return address for function calls.
R13-R14	    Caller-Saved Temporary Registers	Caller-saved; used for intermediate values.
R15         Temporary Address Register          Used for combining offset and address when Storing
"""
