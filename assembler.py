from pyparsing import Word, alphas, alphanums, Group, Optional, Suppress, OneOrMore, nums, Literal

## TODO ##
## implement IMD values
## implement RAM

"""
opcode_list = {
    # ALU
    'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
    'SHL', 'SHR', 'ASHR',
    'AND', 'OR', 'XOR', 'NOT',

    # COND
    'JMP', 'BEQ', 'BNE',
    'BLT', 'BLTU', 'BLE', 'BLEU',
    'BGT', 'BGTU', 'BGE', 'BGEU',

    # RAM
    'LOAD', 'STORE'
}

registers = {
    'R0': '000',  # Register 0 (R0) - Zero register
    'R1': '001',  # Register 1 (R1)
    'R2': '010',  # Register 2 (R2)
    'R3': '011',  # Register 3 (R3)
    'R4': '100',  # Register 4 (R4)
    'R5': '101',  # Register 5 (R5)
    'R6': '110',  # Register 6 (R6)
    'R7': '111',  # Register 7 (R7)
    'R8': '000',  # Special jump register (JMP) - Value can only be stored, not read
}
"""

alu_opcodes = { 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'SHL', 'SHR', 'ASHR', 'AND', 'OR', 'XOR', 'NOT' }
cond_opcodes = { 'JMP', 'BEQ', 'BNE', 'BLT', 'BLTU', 'BLE', 'BLEU', 'BGT', 'BGTU', 'BGE', 'BGEU' }
ram_opcodes = { 'LOAD', 'STORE' }

opcode = Word(alphas)
sourceRegister1 = Word("R", nums)
sourceRegister2 = Word("R", nums)
destRegister = Word("R", nums)

def opcode_category(tokens):
    if tokens[0] in alu_opcodes:
        return ('ALU', tokens[0])
    elif tokens[0] in cond_opcodes:
        return ('COND', tokens[0])
    elif tokens[0] in ram_opcodes:
        return ('RAM', tokens[0])
    else:
        raise ValueError(f"Invalid OPCODE: {tokens[0]}")

def validate_source_register(tokens):
    reg_number = tokens[0][1:]  # Get the number part after 'R'
    # Check for source registers (R0 to R7)
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 7):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R7 for Source.")
    return tokens[0]  # Return the original register token if valid

def validate_dest_register(tokens):
    reg_number = tokens[0][1:]  # Get the number part after 'R'
    # Check for source registers (R0 to R7)
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 8):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R8 for Destination.")
    return tokens[0]  # Return the original register token if valid

instruction = Group(
    opcode.setParseAction(opcode_category) +
    sourceRegister1.setParseAction(validate_source_register) +
    sourceRegister2.setParseAction(validate_source_register) +
    destRegister.setParseAction(validate_dest_register)
)

example_instruction_1 = "ADD R1 R2 R1"
example_instruction_2 = "JMP R6 R7 R8"
example_instruction_3 = "LOAD R5 R6 R7"

parsed_instruction_1 = instruction.parseString(example_instruction_1)
parsed_instruction_2 = instruction.parseString(example_instruction_2)
parsed_instruction_3 = instruction.parseString(example_instruction_3)

print(parsed_instruction_1.asList())
print(parsed_instruction_2.asList())
print(parsed_instruction_3.asList())
