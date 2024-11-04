from lark import Visitor

class CodeGenerator(Visitor):
    def __init__(self):
        self.output = []  # Store the generated code lines

    def generate_code(self):
        return "\n".join(self.output)
