# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


## Variable Declaration ##
def var_decl_start(self: "CodeGenerator", node):
    self.comment(f"# VARIABLE DECLARATION:")
    self.indent()
    return str(node[0])

def var_decl(self: "CodeGenerator", node):
    var_type = str(node[0])
    var_name = str(node[1])

    # if no expression given, then value = 0
    if len(node) > 2:
        if (isinstance(node[2], tuple)) and (node[2][0] == "register"):
            register = node[2][1]
            self.stackPointer -= 1
            self.declare_variable(var_name, self.stackPointer)

            self.comment(f"# {var_type} {var_name} = {register}")
            self.code(f"ISTORE {self.stackPointer} {register} 0")
            
            self.unindent()
            self.comment(f"# END VARIABLE DECLARATION [ {var_type} {var_name} = {register} ]", newLine2=True)
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for var_decl")
    else:
        self.stackPointer -= 1
        self.declare_variable(var_name, self.stackPointer)

        self.comment(f"# {var_type} {var_name} = 0")
        self.code(f"ISTOREI {self.stackPointer} 0 0")
        
        self.unindent()
        self.comment(f"# END VARIABLE DECLARATION [ {var_type} {var_name} = 0 ]", newLine2=True)


## Assignment Statement ##
def assign_stmt_start(self: "CodeGenerator", node):
    self.comment(f"# ASSIGN STATEMENT:")
    self.indent()
    return str(node[0])

def assign_stmt(self: "CodeGenerator", node):
    var_name = str(node[0])

    if (isinstance(node[1], tuple)) and (node[1][0] == "register"):
        register = node[1][1]
        var_address = self.get_variable_address(var_name)

        self.comment(f"# {var_name} = {register}")
        self.code(f"ISTORE {var_address} {register} 0")
        self.exprRegisters.append(register)

        self.unindent()
        self.comment(f"# END ASSIGN STATEMENT [ {var_name} = {register} ]", newLine2=True)
    else:
        raise MemoryError("ERROR: expression register not found for var_decl")
