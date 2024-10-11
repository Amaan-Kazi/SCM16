from pyparsing import Word, alphas, alphanums, Group, Optional, Suppress, OneOrMore, nums, Literal

## TODO ##
## Convert to int: source and destination words
## convert ints to hex and output to file

alu_opcodes = {
    'ADD': 0, 'SUB': 1, 'MUL': 2, 'DIV': 3, 'MOD': 4,
    'SHL': 5, 'SHR': 6, 'ASHR': 7,
    'AND': 8, 'OR': 9, 'XOR': 10, 'NOT': 11
}

cond_opcodes = {
    'JMP': 0, 'BEQ': 1, 'BNE': 2,
    'BLT': 3, 'BLTU': 4, 'BLE': 5, 'BLEU': 6,
    'BGT': 7, 'BGTU': 8, 'BGE': 9, 'BGEU': 10
}

ram_opcodes = {
    'LOAD': 0,
    'STORE': 1
}

opcode = Word(alphas)
register = Word("R", nums)
immediate = Word(nums)
sourceLabel = Suppress("@") + Word(alphanums) + Suppress(":")
destLabel = Suppress("@") + Word(alphanums)

labels = {}
instructionNo = 0

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
        return ("Opcode", 'ALU', modifiedToken, alu_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
    elif modifiedToken in cond_opcodes:
        return ("Opcode", 'COND', modifiedToken, cond_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
    elif modifiedToken in ram_opcodes:
        return ("Opcode", 'RAM', modifiedToken, ram_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
    else:
        raise ValueError(f"Invalid OPCODE: {modifiedToken}")

def validateSourceRregister(tokens):
    reg_number = tokens[0][1:]  # Get the number part after 'R'
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 7):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R7 for Source.")
    return ("Register", tokens[0])

def validateDestRegister(tokens):
    reg_number = tokens[0][1:]
    if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 8):
        raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R8 for Destination.")
    return ("Register", tokens[0])

def validateImmediate(tokens):
    if (not tokens[0].isdigit()) or (int(tokens[0]) < 0) or (int(tokens[0]) > 65535):
        raise ValueError(f"Invalid Immediate: {tokens[0]}. Valid range (both inclusive) is from 0 to 65535")
    return ("Immediate", tokens[0])

def addLabel(tokens):
    global labels
    labelName = str(tokens[0])

    if labelName in labels:
        raise ValueError(f"Label '{labelName}' is already defined.")

    labels[labelName] = instructionNo + 4 # address of next instruction
    return ("Label", labelName)

def validateLabel(tokens):
    global labels
    labelName = str(tokens[0])

    if not labelName in labels:
        raise ValueError(f"Label '{labelName}' is not defined.")
    return ("label", tokens[0])

instruction = Optional(sourceLabel.setParseAction(addLabel))
instruction += opcode.setParseAction(validateOpcode)
instruction += (register.setParseAction(validateDestRegister) | immediate.setParseAction(validateImmediate))
instruction += (register.setParseAction(validateSourceRregister) | immediate.setParseAction(validateImmediate))
instruction += (register.setParseAction(validateDestRegister) | immediate.setParseAction(validateImmediate) | destLabel.setParseAction(validateLabel))

asmFile = input("Assembly File Name [in /ASM, no extension]: ")
print("\n")

with open(f"ASM/{str(asmFile)}.assembly", "r") as file:
    l = 0
    binary = ""

    for line in file:
        l += 1
        i = 0

        # Remove any leading/trailing whitespace characters (including newline)
        line = line.strip()

        # Skip lines that start with a '#' (comments) or empty lines
        if not line or line.startswith('#'):
            continue

        try:
            parsed_instruction = instruction.parseString(line)
            print(parsed_instruction)
        except Exception as e:
            print(f"\nERROR [Line {l}, Instruction {instructionNo}] \n{line}\n{e}\n")
            exit()

        if (parsed_instruction[i][0] == "Label"):
            print(parsed_instruction[i])
            i += 1
        intOpcode = 0

        if (parsed_instruction[i][4] == True):
            intOpcode += 32768 # 2 ^ 15

        if (parsed_instruction[i][5] == True):
            intOpcode += 16384 # 2 ^ 14

        if (parsed_instruction[i][1] == "ALU"):
            intOpcode += 0 # 00
        elif (parsed_instruction[i][1] == "COND"):
            intOpcode += 4096 # 01
        elif (parsed_instruction[i][1] == "RAM"):
            intOpcode += 8192 # 10
        elif (parsed_instruction[i][1] == "IO"):
            intOpcode += 12288 # 11
        
        intOpcode += parsed_instruction[i][3]

        print(intOpcode)
        instructionNo += 4
