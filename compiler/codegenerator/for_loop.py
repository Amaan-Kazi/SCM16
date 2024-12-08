# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


def for_start(self: "CodeGenerator", node):
    self.comment(f"# FOR LOOP: ")
    self.indent()

    self.comment(f"# FOR INITIALIZATION: ")
    self.indent()

    self.enter_scope()

def for_condition_start(self: "CodeGenerator", node):
    self.unindent()
    self.comment(f"# END FOR INTIALIZATION", newLine2=True)

    # start of loop condition
    self.highestLabel += 1
    self.labels.append(f"forLabel{self.highestLabel}")
    self.highestLabel += 1
    self.labels.append(f"forLabel{self.highestLabel}")
    self.highestLabel += 1
    self.labels.append(f"forLabel{self.highestLabel}")
    self.highestLabel += 1
    self.labels.append(f"forLabel{self.highestLabel}")

    self.comment(f"# FOR CONDITION: ")
    self.indent()

    self.code(f"@{self.labels[-4]}: IADDI 0 0 0")

def for_condition(self: "CodeGenerator", node):
    if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
        register = node[0][1]

        self.code(f"LNOTI {register} 0 {register}")
        self.code(f"JMPI {register} 0 @{self.labels[-1]}")

        self.unindent()
        self.comment(f"# END FOR CONDITION", newLine2=True)

        self.exprRegisters.append(register)
    else:
        raise MemoryError("ERROR: expression register not found for for_condition")
    
def for_update_start(self: "CodeGenerator", node):
    # skip evaluating assign stmt first, then come back to it after loop block is evaluated
    # at end of assign stmt evaluation, jmp back to the condition of loop
    self.comment(f"# FOR UPDATE: ")
    self.indent()

    self.code(f"\nIJMPI 1 0 @{self.labels[-3]}")
    self.code(f"@{self.labels[-2]}: IADDI 0 0 0", newLine2=True)

def for_update_end(self: "CodeGenerator", node):
    self.code(f"\nIJMPI 1 0 @{self.labels[-4]}")
    self.code(f"@{self.labels[-3]}: IADDI 0 0 0")

    self.unindent()
    self.comment(f"# END FOR UPDATE", newLine2=True)

    self.comment(f"# FOR BODY: ")
    self.indent()

def for_stmt(self: "CodeGenerator", node):
    self.unindent()
    self.comment(f"# END FOR BODY", newLine2=True)

    self.code(f"\nIJMPI 1 0 @{self.labels[-2]}")
    self.code(f"@{self.labels[-1]}: IADDI 0 0 0")
    
    self.unindent()
    self.comment(f"# END FOR LOOP", newLine2=True)

    self.exit_scope()
    self.labels.pop()
    self.labels.pop()
    self.labels.pop()
    self.labels.pop()
