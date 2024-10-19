from lark import Lark

# Load the grammar from a .lark file
with open('grammar.lark') as f:
    grammar = f.read()

# Create the parser
parser = Lark(grammar)

# Input code to parse
input_code = """
int16 a = 10;
int32 b = -30000;
"""

# Parse the code
tree = parser.parse(input_code)
print(tree.pretty())
