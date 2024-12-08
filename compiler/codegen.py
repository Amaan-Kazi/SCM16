from compiler.codegenerator.expressions import infix_to_postfix, expression
from compiler.codegenerator.variables   import var_decl_start, var_decl, assign_stmt_start, assign_stmt
from compiler.codegenerator.branching   import if_condition, else_if_condition, if_start, if_end, else_end, if_stmt
from compiler.codegenerator.while_loop  import while_condition_start, while_condition, while_stmt
from compiler.codegenerator.for_loop    import for_start, for_condition_start, for_condition, for_update_start, for_update_end, for_stmt
from compiler.codegenerator.display     import putpixel_start, putpixel, color_start, color, fill

from lark import Transformer


class CodeGenerator(Transformer):
    def __init__(self: "CodeGenerator"):
        self.output = []        # Store the generated code lines
        self.symbolTable = [{}] # Stores variables and their addresses
        self.scopePointerStack = []

        self.exprRegisters = ["R9", "R8", "R7", "R6", "R5", "R4"]

        self.stackPointer = 65535

        self.labels = []
        self.highestLabel = 0

        self.indentLevel = 0
        self.instructions = 0

        #self.inFunctionScope = False
        #self.functionScope = [{}]

    def generate_code(self: "CodeGenerator"):
        # DEBUG: Requires result variable to be declared in code | Displays value of result on R15
        var_address = self.get_variable_address("result")

        self.comment(f"# DEBUG: Load variable result into R15")
        self.code(f"ILOADI {var_address} 0 R15")

        self.code("HALT 0 0 0", newLine2=True) # End of program
        return "\n".join(self.output)


    ## Code Formatting ##
    def indent(self: "CodeGenerator"):
        self.indentLevel += 1
    def unindent(self: "CodeGenerator"):
        self.indentLevel -= 1

    def code(self: "CodeGenerator", instruction: str, newLine1 = False, newLine2 = False):
        indent = '\t' * self.indentLevel
        label = ''

        words = instruction.split()

        if words[0].startswith('@'):
            label = words.pop(0)
            label += ' '

        newLineChar1 = '\n' if newLine1 else ''
        newLineChar2 = '\n' if newLine2 else ''

        formatted_words = ' '.join([f"{word:<5}" for word in words[1:]])
        self.output.append(f"{newLineChar1}{indent}{label}{words[0]:<7} {formatted_words}{newLineChar2}")
        self.instructions =+ 1

    def comment(self: "CodeGenerator", comment: str, newLine1 = False, newLine2 = False):
        indent = '\t' * self.indentLevel
        
        newLineChar1 = '\n' if newLine1 else ''
        newLineChar2 = '\n' if newLine2 else ''

        self.output.append(f"{newLineChar1}{indent}{comment}{newLineChar2}")


    ## VARIABLES ##
    def declare_variable(self: "CodeGenerator", var_name: str, address: int):
        #if self.inFunctionScope == False:
        current_scope = self.symbolTable[-1]
        if var_name in current_scope:
            raise ValueError(f"Variable {var_name} is already declared in this scope")
        current_scope[var_name] = address
        #else:

    def get_variable_address(self: "CodeGenerator", var_name: str) -> int:
        for scope in reversed(self.symbolTable):  # Start from the innermost scope
            if var_name in scope:
                return scope[var_name]
        raise ValueError(f"Variable {var_name} is not declared in any accessible scope")


    ## SCOPES ##
    def enter_scope(self: "CodeGenerator"):
        self.scopePointerStack.append(int(self.stackPointer))
        self.symbolTable.append({}) # Push a new dictionary onto the stack to represent a new scope.

    def exit_scope(self: "CodeGenerator"):
        # Remove the top-most scope from the stack.
        if len(self.symbolTable) > 1:  # Prevent removing the global scope
            self.symbolTable.pop()
            self.stackPointer = self.scopePointerStack.pop()
        else:
            raise ValueError("Cannot exit global scope")


    ## DATA TYPES AND LITERALS ##
    def num(self: "CodeGenerator", node):
        return ('num', int(node[0]))
    def var(self: "CodeGenerator", node):
        return ('var', str(node[0]))


    ## EXPRESSIONS ##
    infix_to_postfix = infix_to_postfix
    expression       = expression
    
    
    ## VARIABLES ##
    var_decl_start = var_decl_start
    var_decl       = var_decl

    assign_stmt_start = assign_stmt_start
    assign_stmt       = assign_stmt


    ## BRANCHING ##
    if_condition      = if_condition
    else_if_condition = else_if_condition
    if_start          = if_start
    if_end            = if_end
    else_end          = else_end
    if_stmt           = if_stmt


    ## WHILE LOOP ##
    while_condition_start = while_condition_start
    while_condition       = while_condition
    while_stmt            = while_stmt


    ## FOR LOOP ##
    for_start           = for_start
    for_condition_start = for_condition_start
    for_condition       = for_condition
    for_update_start    = for_update_start
    for_update_end      = for_update_end
    for_stmt            = for_stmt

    
    ## DOT MATRIX DISPLAY FUNCTIONS ##
    putpixel_start = putpixel_start
    putpixel       = putpixel
    color_start    = color_start
    color          = color
    fill           = fill


    ## UTILITY FUNCTIONS ##
    def exit(self: "CodeGenerator", node):
        self.comment(f"# EXIT(): ")
        self.code(f"HALT 0 0 0", newLine2=True)
