from pyparsing import Word, alphas, alphanums, Group, Optional, Suppress, OneOrMore, nums, Literal

alu_opcodes = {
    'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
    'SHL', 'SHR', 'ASHR',
    'AND', 'OR', 'XOR', 'NOT'
}

cond_opcodes = {
    'JMP', 'BEQ', 'BNE',
    'BLT', 'BLTU', 'BLE', 'BLEU',
    'BGT', 'BGTU', 'BGE', 'BGEU'
}

ram_opcodes = {
    'LOAD',
    'STORE'
}

opcode = Word(alphas)
register = Word("R", nums)
immediate = Word(nums)
sourceLabel = Suppress("@") + Word(alphanums) + Suppress(":")
destLabel = Suppress("@") + Word(alphanums)

labels = {}

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

def addLabel(tokens):
    global labels
    labelName = str(tokens[0])

    if labelName in labels:
        raise ValueError(f"Label '{labelName}' is already defined.")

    labels[labelName] = 0 # give address of next instruction later
    return labelName

def validateLabel(tokens):
    global labels
    labelName = str(tokens[0])

    if not labelName in labels:
        raise ValueError(f"Label '{labelName}' is not defined.")
    return tokens[0]

instruction = Group(
    Optional(sourceLabel.setParseAction(addLabel)) +
    opcode.setParseAction(validateOpcode) +
    (register.setParseAction(validateDestRegister) | immediate.setParseAction(validateImmediate)) +
    (register.setParseAction(validateSourceRregister) | immediate.setParseAction(validateImmediate)) +
    (register.setParseAction(validateDestRegister) | immediate.setParseAction(validateImmediate) | destLabel.setParseAction(validateLabel))
)

example_instruction_1 = "@asd: ADD R1 R2 R1"
example_instruction_2 = "@def: JMPI 2007 R7 @def"
example_instruction_3 = "ILOAD R5 R6 R7"

parsed_instruction_1 = instruction.parseString(example_instruction_1)
parsed_instruction_2 = instruction.parseString(example_instruction_2)
parsed_instruction_3 = instruction.parseString(example_instruction_3)

print(parsed_instruction_1.asList())
print(parsed_instruction_2.asList())
print(parsed_instruction_3.asList())
