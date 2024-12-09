# Import the CodeGenerator class for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from codegen import CodeGenerator


## IF STATEMENT ##
def if_condition_start(self: "CodeGenerator", node):
    self.comment(f"# CONDITIONAL BRANCHES: ")
    self.indent()

    self.comment(f"# IF: ")
    self.indent()

    self.comment(f"# IF CONDITION: ")
    self.indent()

def if_condition(self: "CodeGenerator", node):
    if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
        register = node[0][1]

        self.code(f"LNOTI {register} 0 {register}")

        # push 1 label for end of if block which can be continued by else if, else statements
        # and push 1 label for end of entire if ladder
        self.highestLabel += 1
        self.labels.append(f"ifLabel{self.highestLabel}")
        self.highestLabel += 1
        self.labels.append(f"ifLabel{self.highestLabel}")

        self.code(f"JMPI {register} 0 @{self.labels[-1]}")
        self.exprRegisters.append(register)

        self.unindent()
        self.comment(f"# END IF CONDITION", newLine2=True)
    else:
        raise MemoryError("ERROR: expression register not found for if_condition")
    
def if_start(self: "CodeGenerator", node):
    self.comment(f"# IF BODY: ")
    self.indent()
    self.enter_scope()

def if_end(self: "CodeGenerator", node):
    label = self.labels.pop()

    self.unindent()
    self.comment(f"# END IF BODY", newLine2=True)

    self.code(f"IJMPI 1 0 @{self.labels[-1]}")
    self.code(f"@{label}: IADDI 0 0 0") # dummy instruction due to how labels are assembled
    self.exit_scope()
    

    self.unindent()
    self.comment(f"# END IF", newLine2=True)
    

## ELSE IF STATEMENTS ##
def else_if_condition_start(self: "CodeGenerator", node):
    self.comment(f"# ELSE IF: ")
    self.indent()

    self.comment(f"# ELSE IF CONDITION: ")
    self.indent()

def else_if_condition(self: "CodeGenerator", node):
    if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
        register = node[0][1]

        self.code(f"LNOTI {register} 0 {register}")

        # push 1 label for end of else if block
        self.highestLabel += 1
        self.labels.append(f"elseIfLabel{self.highestLabel}")

        self.code(f"JMPI {register} 0 @{self.labels[-1]}")
        self.exprRegisters.append(register)

        self.unindent()
        self.comment(f"# END ELSE IF CONDITION: ", newLine2=True)
    else:
        raise MemoryError("ERROR: expression register not found for else_if_condition")

def else_if_start(self: "CodeGenerator", node):
    self.comment(f"# ELSE IF BODY: ")
    self.indent()
    self.enter_scope()

def else_if_end(self: "CodeGenerator", node):
    label = self.labels.pop()

    self.unindent()
    self.comment(f"# END ELSE IF BODY", newLine2=True)

    self.code(f"IJMPI 1 0 @{self.labels[-1]}")
    self.code(f"@{label}: IADDI 0 0 0") # dummy instruction due to how labels are assembled
    self.exit_scope()

    self.unindent()
    self.comment(f"# END ELSE IF", newLine2=True)


## ELSE STATEMENT ##
def else_start(self: "CodeGenerator", node):
    self.comment(f"# ELSE: ")
    self.indent()

    self.comment(f"# ELSE BODY: ")
    self.indent()
    self.enter_scope()

def else_end(self: "CodeGenerator", node):
    self.unindent()
    self.comment(f"# END ELSE BODY")
    
    self.unindent()
    self.comment(f"# END ELSE", newLine2=True)

    self.exit_scope()


def if_stmt(self: "CodeGenerator", node):
    label = self.labels.pop()
    self.code(f"\n@{label}: IADDI 0 0 0") # dummy instruction due to how labels are assembled

    self.unindent()
    self.comment(f"# END CONDITIONAL BRANCHING", newLine2=True)
