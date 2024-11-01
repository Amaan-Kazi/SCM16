from lark import Lark

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
