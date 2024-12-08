# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


def putpixel_start(self: "CodeGenerator", node):
    self.comment(f"# PUTPIXEL(): ")
    self.indent()

def putpixel(self: "CodeGenerator", node):
    node.pop(0) # removal of unneeded empty node from putpixel_start
    if ((isinstance(node[0], tuple)) and (node[0][0] == "register") and (isinstance(node[1], tuple)) and (node[1][0] == "register")):
        register1 = node[0][1]
        register2 = node[1][1]

        self.comment(f"# PUT PIXEL [ {register1}, {register2} ]")
        self.code(f"PIXEL {register1} {register2} 0")

        self.unindent()
        self.comment(f"# END PUTPIXEL()", newLine2=True)

        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)
    else:
        raise MemoryError("ERROR: expression register not found for putpixel")


def color_start(self: "CodeGenerator", node):
    self.comment(f"# COLOR(): ")
    self.indent()

def color(self: "CodeGenerator", node):
    node.pop(0) # removal of unneeded empty node from color_start
    if ((isinstance(node[0], tuple)) and (node[0][0] == "register") and (isinstance(node[1], tuple)) and (node[1][0] == "register") and (isinstance(node[2], tuple)) and (node[2][0] == "register")):
        register1 = node[0][1]
        register2 = node[1][1]
        register3 = node[2][1]

        self.comment(f"# COLOR [ {register1}, {register2}, {register3} ]")
        self.code(f"SHLI {register1} 8 {register1}")
        self.code(f"ADD {register1} {register2} {register1}")
        self.code(f"COLOR {register1} {register3} 0")

        self.unindent()
        self.comment(f"# END COLOR()", newLine2=True)
        
        self.exprRegisters.append(register3)
        self.exprRegisters.append(register2)
        self.exprRegisters.append(register1)
    else:
        raise MemoryError("ERROR: expression register not found for color")

    
def fill(self: "CodeGenerator", node):
    self.comment(f"# FILL(): ")
    self.code(f"IFILLI 0 0 0", newLine2=True)
