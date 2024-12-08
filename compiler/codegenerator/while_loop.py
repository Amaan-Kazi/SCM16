# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


def while_condition_start(self: "CodeGenerator", node):
    # label to start of loop
    self.highestLabel += 1
    self.labels.append(f"whileLabel{self.highestLabel}")

    # label to jump out of loop
    self.highestLabel += 1
    self.labels.append(f"whileLabel{self.highestLabel}")

    self.comment(f"# WHILE LOOP: ")
    self.indent()
    self.comment(f"# WHILE CONDITION: ")
    self.indent()

    self.code(f"@{self.labels[-2]}: IADDI 0 0 0")

def while_condition(self: "CodeGenerator", node):
    if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
        register = node[0][1]

        self.comment(f"# if while condition false, jump out of loop")
        self.code(f"LNOTI {register} 0 {register}")
        self.code(f"JMPI {register} 0 @{self.labels[-1]}")
        self.exprRegisters.append(register)

        self.unindent()
        self.comment(f"# END WHILE CONDITION", newLine2=True)

        self.enter_scope()
        self.comment(f"# WHILE BODY: ")
        self.indent()
    else:
        raise MemoryError("ERROR: expression register not found for while_condition")

def while_stmt(self: "CodeGenerator", node):
    self.unindent()
    self.comment(f"# END WHILE BODY", newLine2=True)

    self.code(f"IJMPI 1 0 @{self.labels[-2]}") # always go back to start of loop
    self.code(f"@{self.labels[-1]}: IADDI 0 0 0") # end of loop in case condition false

    self.unindent()
    self.comment(f"# END WHILE LOOP", newLine2=True)

    self.exit_scope()
    self.labels.pop()
    self.labels.pop()
