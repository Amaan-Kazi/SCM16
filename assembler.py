from pyparsing import Word, alphas, alphanums, Group, Optional, Suppress, OneOrMore, nums, Literal

## TODO ##
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
register = Word("R", nums)
immediate = Word(nums)

def validateOpcode(tokens):
    modifiedToken = str(tokens[0])
    immediate1Flag = False
    immediate2Flag = False

    if (modifiedToken.startswith("I")):
        immediate1Flag = True
        modifiedToken = modifiedToken[1:]

    if (modifiedToken.endswith("I")):
        immediate2Flag = True
        modifiedToken = modifiedToken[:-1]

    if modifiedToken in alu_opcodes:
        return ('ALU', modifiedToken, immediate1Flag, immediate2Flag)
    elif modifiedToken in cond_opcodes:
        return ('COND', modifiedToken, immediate1Flag, immediate2Flag)
    elif modifiedToken in ram_opcodes:
        return ('RAM', modifiedToken, immediate1Flag, immediate2Flag)
    else:
        raise ValueError(f"Invalid OPCODE: {modifiedToken}")

def validateSourceRregister(tokens):
    reg_number = tokens[0][1:]  # Get the number part after 'R'
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 7):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R7 for Source.")
    return tokens[0]

def validateDestRegister(tokens):
    reg_number = tokens[0][1:]
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 8):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R8 for Destination.")
    return tokens[0]

def validateImmediate(tokens):
    if (not tokens[0].isdigit()) or (int(tokens[0]) < 0) or (int(tokens[0]) > 65535):
        raise ValueError(f"Invalid Immediate: {tokens[0]}. Valid range (both inclusive) is from 0 to 65535")
    return tokens[0]

instruction = Group(
    opcode.setParseAction(validateOpcode) +
    (register.setParseAction(validateDestRegister) | immediate.setParseAction(validateImmediate)) +
    (register.setParseAction(validateSourceRregister) | immediate.setParseAction(validateImmediate)) +
    register.setParseAction(validateDestRegister)
)

example_instruction_1 = "IADDI R1 R2 R1"
example_instruction_2 = "JMPI 2007 R7 R8"
example_instruction_3 = "ILOAD R5 R6 R7"

parsed_instruction_1 = instruction.parseString(example_instruction_1)
parsed_instruction_2 = instruction.parseString(example_instruction_2)
parsed_instruction_3 = instruction.parseString(example_instruction_3)

print(parsed_instruction_1.asList())
print(parsed_instruction_2.asList())
print(parsed_instruction_3.asList())
