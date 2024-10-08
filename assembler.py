from pyparsing import Word, alphas, alphanums, Group, Optional, Suppress, OneOrMore, nums, Literal

# Define the instruction set
instructions = {
    'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'SHL', 'SHR', 'ASHR',
    'AND', 'OR', 'XOR', 'NOT', 'JMP', 'BEQ', 'BNE', 'BLT',
    'BLTU', 'BLE', 'BLEU', 'BGT', 'BGTU', 'BGE', 'BGEU',
    'LOAD', 'STORE', 'MOV'
}

# Define register
register = Word("R", alphanums)

# Define immediate value
immediate = Word(nums)

# Define instruction structure
instruction = (
    Word(alphas).setResultsName("instruction") +  # Instruction
    register.setResultsName("source1") +  # Source Register 1
    register.setResultsName("source2") +  # Source Register 2 or IMD2
    Optional(register.setResultsName("dest"), "")  # Destination Register
)

# Parse a line
result = instruction.parseString("ADD R1 R2 R3")
# Flatten the output
output = [result.instruction] + [result.source1, result.source2] + ([result.dest] if result.dest else [])
print(output)
