from lark import Lark
from compiler.codegenerator import CodeGenerator

# Load the grammar from a .lark file
with open('grammar.lark') as f:
    grammar = f.read()

# Create the parser
parser = Lark(grammar)

scmCodeFile = input("SCMCODE File Name [in /SCMCODE, no extension]: ")
print("\n")

with open(f"SCMCODE/{str(scmCodeFile)}.scmcode", "r") as file:
    scmCode = file.read()

# Parse the code
parseTree = parser.parse(scmCode)
print(parseTree.pretty())

print("----------------------------")

# Create a visitor and visit the parse tree
visitor = CodeGenerator()
visitor.visit(parseTree)  # Traverse the parse tree
generated_code = visitor.generate_code()  # Get the generated code
print("Generated Code:")
print(generated_code)
