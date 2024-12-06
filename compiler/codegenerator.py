from lark import Transformer

class CodeGenerator(Transformer):
    def __init__(self):
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

    ## TODO: separate this class into separate files for different categories of functions
    ## TODO: replace self.output.append with suitable code output functions

    def indent(self):
        self.indentLevel += 1
    def unindent(self):
        self.indentLevel -= 1

    def code(self, instruction: str, newLine1 = False, newLine2 = False):
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

    def comment(self, comment: str, newLine1 = False, newLine2 = False):
        indent = '\t' * self.indentLevel
        
        newLineChar1 = '\n' if newLine1 else ''
        newLineChar2 = '\n' if newLine2 else ''

        self.output.append(f"{newLineChar1}{indent}{comment}{newLineChar2}")


    ## VARIABLES ##
    def declare_variable(self, var_name: str, address: int):
        #if self.inFunctionScope == False:
        current_scope = self.symbolTable[-1]
        if var_name in current_scope:
            raise ValueError(f"Variable {var_name} is already declared in this scope")
        current_scope[var_name] = address
        #else:

    def get_variable_address(self, var_name: str) -> int:
        for scope in reversed(self.symbolTable):  # Start from the innermost scope
            if var_name in scope:
                return scope[var_name]
        raise ValueError(f"Variable {var_name} is not declared in any accessible scope")


    ## SCOPES ##
    def enter_scope(self):
        self.scopePointerStack.append(int(self.stackPointer))
        self.symbolTable.append({}) # Push a new dictionary onto the stack to represent a new scope.

    def exit_scope(self):
        # Remove the top-most scope from the stack.
        if len(self.symbolTable) > 1:  # Prevent removing the global scope
            self.symbolTable.pop()
            self.stackPointer = self.scopePointerStack.pop()
        else:
            raise ValueError("Cannot exit global scope")


    ## DATA TYPES AND LITERALS ##
    def num(self, node):
        return ('num', int(node[0]))
    def var(self, node):
        return ('var', str(node[0]))


    ## EXPRESSIONS ##    
    def infix_to_postfix(self, expression):
        precedence = {
            '*':  3, '/':  3, '%': 3,
            '+':  2, '-':  2,
            '==': 1, '!=': 1,
            '<':  1, '<=': 1,
            '>':  1, '>=': 1,
            '&&': 0, '||': 0
        }
        
        associativity = {
            '*':  'L', '/':  'L', '%': 'L',
            '+':  'L', '-':  'L',
            '==': 'L', '!=': 'L',
            '<':  'L', '<=': 'L',
            '>':  'L', '>=': 'L',
            '&&': 'L', '||': 'L'
        }

        operations = {
            "multiply":     "*",  "divide":                "/", "modulus": "%",
            "add":          "+",  "subtract":              "-",
            "equal":        "==", "not_equal":             "!=",
            "lesser_than":  "<",  "lesser_than_or_equal":  "<=",
            "greater_than": ">",  "greater_than_or_equal": ">=",
            "logical_and":  "&&", "logical_or":            "||"
        }

        output = []
        operators = []

        for token in expression:
            if isinstance(token, tuple):
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

    def expression(self, node):
        postfix_expr = self.infix_to_postfix(node)

        resultRegister = self.exprRegisters.pop()
        expressionBasePointer = self.stackPointer

        symbols = {
            "multiply":     "*",  "divide":                "/", "modulus": "%",
            "add":          "+",  "subtract":              "-",
            "equal":        "==", "not_equal":             "!=",
            "lesser_than":  "<",  "lesser_than_or_equal":  "<=",
            "greater_than": ">",  "greater_than_or_equal": ">=",
            "logical_and":  "&&", "logical_or":            "||",
            "left_parenthesis": "(", "right_parenthesis": ")"
        }

        infixExpr = ''

        for exprToken in node:
            if isinstance(exprToken, tuple):
                infixExpr += str(exprToken[1]) + ' '
            else:
                infixExpr += symbols[str(exprToken.data)] + ' '

        self.comment(f"# EXPRESSION [ {infixExpr}]: ")
        self.indent()

        if len(postfix_expr) == 1:
            if postfix_expr[0][0] == "num":
                self.comment(f"# {resultRegister} = {int(postfix_expr[0][1])}")
                self.code(f"IADDI 0 {int(postfix_expr[0][1])} {resultRegister}")
            elif postfix_expr[0][0] == "var":
                var_name = str(postfix_expr[0][1])
                var_address = self.get_variable_address(var_name)
                
                self.comment(f"# {resultRegister} = {var_name}")
                self.code(f"ILOADI {var_address} 0 {resultRegister}")
        else:
            for token in postfix_expr:
                tokenType, tokenValue = token

                if tokenType == "num":
                    self.stackPointer -= 1
                    self.comment(f"# [{self.stackPointer}] = {tokenValue}")
                    self.code(f"ISTOREI {self.stackPointer} {int(tokenValue)} 0", newLine2=True)
                elif tokenType == "var":
                    self.stackPointer -= 1
                    tempRegister = self.exprRegisters.pop()

                    var_name = str(tokenValue)
                    var_address = self.get_variable_address(var_name)

                    self.comment(f"# [{self.stackPointer}] = {var_name}")
                    self.code(f"ILOADI {int(var_address)} 0 {tempRegister}")
                    self.code(f"ISTORE {self.stackPointer} {tempRegister} 0", newLine2=True)

                    self.exprRegisters.append(tempRegister)
                elif tokenType == "operator":
                    register1 = self.exprRegisters.pop()
                    register2 = self.exprRegisters.pop()
                    tempRegister = self.exprRegisters.pop()

                    operations = {
                        "*":  "MUL",  "/":  "DIV", "%":"MOD",
                        "+":  "ADD",  "-":  "SUB",
                        "==": "BEQ",  "!=": "BNE",
                        "<":  "BLTU", "<=": "BLEU",
                        ">":  "BGTU", ">=": "BGEU",
                        "&&": "LAND", "||": "LOR"
                    }

                    instruction = operations[tokenValue]

                    self.comment(f"# [{self.stackPointer}] = [{self.stackPointer + 1}] {tokenValue} [{self.stackPointer}]")
                    self.code(f"ILOADI {self.stackPointer} 0 {register2}")
                    self.stackPointer += 1
                    self.code(f"ILOADI {self.stackPointer} 0 {register1}")
                    
                    self.code(f"{instruction} {register1} {register2} {tempRegister}")
                    self.code(f"ISTORE {self.stackPointer} {tempRegister} 0", newLine2=True)

                    self.exprRegisters.append(tempRegister)
                    self.exprRegisters.append(register2)
                    self.exprRegisters.append(register1)

            self.comment(f"# {resultRegister} = [{self.stackPointer}]")
            self.code(f"ILOADI {self.stackPointer} 0 {resultRegister}")
        
        self.unindent()
        self.comment(f"# END EXPRESSION [{resultRegister}]", newLine2=True)

        self.stackPointer = expressionBasePointer
        return ("register", str(resultRegister))


    ## VARIABLES ##
    def var_decl(self, node):
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
                self.exprRegisters.append(register)
            else:
                raise MemoryError("ERROR: expression register not found for var_decl")
        else:
            self.stackPointer -= 1
            self.declare_variable(var_name, self.stackPointer)

            self.comment(f"# {var_type} {var_name} = 0")
            self.code(f"ISTOREI {self.stackPointer} 0 0")
    
    def assign_stmt(self, node):
        var_name = str(node[0])

        if (isinstance(node[1], tuple)) and (node[1][0] == "register"):
            register = node[1][1]
            var_address = self.get_variable_address(var_name)

            self.comment(f"# {var_name} = {register}")
            self.code(f"ISTORE {var_address} {register} 0")
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for var_decl")


    ## BRANCHING ##
    def if_condition(self, node):
        if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
            register = node[0][1]

            self.comment(f"## IF START ##")
            self.code(f"LNOTI {register} 0 {register}")

            # push 1 label for end of if block which can be continued by else if, else statements
            # and push 1 label for end of entire if ladder
            self.highestLabel += 1
            self.labels.append(f"ifLabel{self.highestLabel}")
            self.highestLabel += 1
            self.labels.append(f"ifLabel{self.highestLabel}")

            self.code(f"JMPI {register} 0 @{self.labels[-1]}")
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for if_condition")
        
    def else_if_condition(self, node):
        if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
            register = node[0][1]

            self.comment(f"## ELSE IF START ##")
            self.code(f"LNOTI {register} 0 {register}")

            # push 1 label for end of else if block
            self.highestLabel += 1
            self.labels.append(f"elseIfLabel{self.highestLabel}")

            self.code(f"JMPI {register} 0 @{self.labels[-1]}")
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for else_if_condition")
        
    def if_start(self, node):
        self.enter_scope()

    def if_end(self, node):
        label = self.labels.pop()

        self.comment(f"## IF END ##")
        self.code(f"IJMPI 1 0 @{self.labels[-1]}")
        self.code(f"@{label}: IADDI 0 0 0") # dummy instruction due to how labels are assembled
        self.exit_scope()

    def else_end(self, node):
        self.comment(f"## ELSE END ##")
        self.exit_scope()

    def if_stmt(self, node):
        label = self.labels.pop()
        self.code(f"\n@{label}: IADDI 0 0 0") # dummy instruction due to how labels are assembled


    ## WHILE LOOP ##
    def while_condition_start(self, node):
        # label to start of loop
        self.highestLabel += 1
        self.labels.append(f"whileLabel{self.highestLabel}")

        # label to jump out of loop
        self.highestLabel += 1
        self.labels.append(f"whileLabel{self.highestLabel}")

        self.comment(f"## WHILE LOOP START ##")
        self.code(f"@{self.labels[-2]}: IADDI 0 0 0")

    def while_condition(self, node):
        if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
            register = node[0][1]

            self.code(f"\nLNOTI {register} 0 {register}")
            self.code(f"JMPI {register} 0 @{self.labels[-1]}")
            self.exprRegisters.append(register)

            self.enter_scope()
        else:
            raise MemoryError("ERROR: expression register not found for while_condition")
    
    def while_stmt(self, node):
        self.code(f"\nIJMPI 1 0 @{self.labels[-2]}") # always go back to start of loop
        self.code(f"@{self.labels[-1]}: IADDI 0 0 0") # end of loop in case condition false
        self.comment(f"## WHILE LOOP END ##")

        self.exit_scope()
        self.labels.pop()
        self.labels.pop()


    ## FOR LOOP ##
    def for_start(self, node):
        self.enter_scope()
    
    def for_condition_start(self, node):
        # start of loop condition
        self.highestLabel += 1
        self.labels.append(f"forLabel{self.highestLabel}")
        self.highestLabel += 1
        self.labels.append(f"forLabel{self.highestLabel}")
        self.highestLabel += 1
        self.labels.append(f"forLabel{self.highestLabel}")
        self.highestLabel += 1
        self.labels.append(f"forLabel{self.highestLabel}")

        self.comment(f"## FOR LOOP START ##")
        self.code(f"@{self.labels[-4]}: IADDI 0 0 0")

    def for_condition(self, node):
        if (isinstance(node[0], tuple)) and (node[0][0] == "register"):
            register = node[0][1]

            self.comment(f"# FOR LOOP CONDITION #")
            self.code(f"LNOTI {register} 0 {register}")
            self.code(f"JMPI {register} 0 @{self.labels[-1]}")
            self.exprRegisters.append(register)
        else:
            raise MemoryError("ERROR: expression register not found for for_condition")
        
    def for_update_start(self, node):
        # skip evaluating assign stmt first, then come back to it after loop block is evaluated
        # at end of assign stmt evaluation, jmp back to the condition of loop
        self.code(f"\nIJMPI 1 0 @{self.labels[-3]}")
        self.code(f"@{self.labels[-2]}: IADDI 0 0 0")

    def for_update_end(self, node):
        self.code(f"\nIJMPI 1 0 @{self.labels[-4]}")
        self.code(f"@{self.labels[-3]}: IADDI 0 0 0")

    def for_stmt(self, node):
        self.code(f"\nIJMPI 1 0 @{self.labels[-2]}")
        self.code(f"@{self.labels[-1]}: IADDI 0 0 0")
        self.comment(f"## FOR END ##")

        self.exit_scope()
        self.labels.pop()
        self.labels.pop()
        self.labels.pop()
        self.labels.pop()

    
    ## DOT MATRIX DISPLAY FUNCTIONS ##
    def putpixel(self, node):
        if ((isinstance(node[0], tuple)) and (node[0][0] == "register") and (isinstance(node[1], tuple)) and (node[1][0] == "register")):
            register1 = node[0][1]
            register2 = node[1][1]

            self.comment(f"# PUT PIXEL")
            self.code(f"PIXEL {register1} {register2} 0")

            self.exprRegisters.append(register2)
            self.exprRegisters.append(register1)
        else:
            raise MemoryError("ERROR: expression register not found for putpixel")

    def color(self, node):
        if ((isinstance(node[0], tuple)) and (node[0][0] == "register") and (isinstance(node[1], tuple)) and (node[1][0] == "register") and (isinstance(node[2], tuple)) and (node[2][0] == "register")):
            register1 = node[0][1]
            register2 = node[1][1]
            register3 = node[2][1]

            self.comment(f"# COLOR")
            self.code(f"SHLI {register1} 8 {register1}")
            self.code(f"ADD {register1} {register2} {register1}")
            self.code(f"COLOR {register1} {register3} 0")
            
            self.exprRegisters.append(register3)
            self.exprRegisters.append(register2)
            self.exprRegisters.append(register1)
        else:
            raise MemoryError("ERROR: expression register not found for color")
        
    def fill(self, node):
        self.comment(f"# FILL")
        self.code(f"IFILLI 0 0 0")


    ## UTILITY FUNCTIONS ##
    def exit(self, node):
        self.comment(f"# EXIT")
        self.code(f"HALT 0 0 0")


    def generate_code(self):
        # DEBUG: Requires result variable to be declared in code | Displays value of result on R15
        var_address = self.get_variable_address("result")

        self.comment(f"# DEBUG: Load variable result into R15")
        self.code(f"ILOADI {var_address} 0 R15")

        self.code("\nHALT 0 0 0\n") # End of program
        return "\n".join(self.output)
