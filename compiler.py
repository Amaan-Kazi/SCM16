from lark import Lark
from compiler.codegenerator import CodeGenerator

# Load the grammar from a .lark file
with open('grammar.lark') as file:
    grammar = file.read()

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
visitor.transform(parseTree)  # Traverse the parse tree

generated_code = visitor.generate_code()  # Get the generated code
print("Generated Code:")
print(generated_code)

with open(f"SCMA/{str(scmCodeFile)}.scma", "w") as file:
    file.write(generated_code)

print(int((60 * 2) - (210 % (450 / 3))))
print("\n--- Compiled Succesfully ---\n")
