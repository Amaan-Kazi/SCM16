from lark import Lark

# Load the grammar from a .lark file
with open('grammar.lark') as f:
    grammar = f.read()

# Create the parser
parser = Lark(grammar)

# Input code to parse
input_code = """
int16 a = 10;
int16 b = -30000;
int16 c = a + b; // works
"""

# Parse the code
tree = parser.parse(input_code)
print(tree.pretty())
