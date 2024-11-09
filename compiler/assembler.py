from pyparsing import Word, alphas, alphanums, Optional, Suppress, nums

def Assemble(code:str):
    alu_opcodes = {
        'ADD': 0, 'SUB': 1, 'MUL':  2,  'DIV': 3, 'MOD': 4,
        'SHL': 5, 'SHR': 6, 'ASHR': 7,
        'AND': 8, 'OR':  9, 'XOR':  10, 'NOT': 11
    }

    cond_opcodes = {
        'JMP': 0, 'BEQ':  1, 'BNE': 2,
        'BLT': 3, 'BLTU': 4, 'BLE': 5, 'BLEU': 6,
        'BGT': 7, 'BGTU': 8, 'BGE': 9, 'BGEU': 10
    }

    ram_opcodes = {
        'LOAD': 0,
        'STORE': 1
    }

    io_opcodes = {
        'PRINT': 0, 'SCRL':  1,
        'PIXEL': 2, 'COLOR': 3, 'FILL': 4,
        'KWAIT': 5, 'KREAD': 6
    }

    opcode      = Word(alphas)
    register    = Word("R", nums)
    immediate   = Word(nums)
    sourceLabel = Suppress("@") + Word(alphanums) + Suppress(":")
    destLabel   = Suppress("@") + Word(alphanums)

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
            return ("Opcode", 'ALU', str(tokens[0]), alu_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
        elif modifiedToken in cond_opcodes:
            return ("Opcode", 'COND', str(tokens[0]), cond_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
        elif modifiedToken in ram_opcodes:
            return ("Opcode", 'RAM', str(tokens[0]), ram_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
        elif modifiedToken in io_opcodes:
            return ("Opcode", 'IO', str(tokens[0]), io_opcodes[modifiedToken], immediate1Flag, immediate2Flag)
        elif modifiedToken == "HALT":
            return ("HALT", "HALT", "1111", immediate1Flag, immediate2Flag)
        else:
            raise ValueError(f"Invalid OPCODE: {modifiedToken}")

    def validateRegister(tokens):
        reg_number = tokens[0][1:]  # Get the number part after 'R'
        if (not reg_number.isdigit()) or (int(reg_number) < 0) or (int(reg_number) > 15):
            raise ValueError(f"Invalid register: {tokens[0]}. Valid registers are R0 to R15")
        return ("Register", reg_number)

    def validateImmediate(tokens):
        if (not tokens[0].isdigit()) or (int(tokens[0]) < 0) or (int(tokens[0]) > 65535):
            raise ValueError(f"Invalid Immediate: {tokens[0]}. Valid range (both inclusive) is from 0 to 65535")
        return ("Immediate", tokens[0])

    def addLabel(tokens):
        global labels
        labelName = str(tokens[0])

        return ("Label", labelName)

    def addPrePassLabel(tokens):
        global labels
        labelName = str(tokens[0])

        if labelName in labels:
            raise ValueError(f"Label '{labelName}' is already defined.")

        labels[labelName] = instructionNo # address of instruction
        return ("Label", labelName)

    def validateLabel(tokens):
        global labels
        labelName = str(tokens[0])
        return ("Label", labelName)

    opcode.setParseAction(validateOpcode)
    register.setParseAction(validateRegister)
    immediate.setParseAction(validateImmediate)
    destLabel.setParseAction(validateLabel)

    instruction = Optional(sourceLabel)
    instruction += opcode
    instruction += (register | immediate | destLabel)
    instruction += (register | immediate | destLabel)
    instruction += (register | immediate | destLabel)

    sourceLabel.setParseAction(addPrePassLabel)
    
    l = 0

    for line in code.strip().split("\n"):
        l += 1
        i = 0

        line = line.strip()

        if not line or line.startswith('#'):
            continue
        
        try:
            parsed_instruction = instruction.parseString(line)
        except Exception as e:
            print(f"\nERROR on Pre Pass [Line {l:05}, Instruction {instructionNo}] \n{line}\n{e}\n")
            exit()

        instructionNo += 4

    instructionNo = 0
    fileContents = ""
    sourceLabel.setParseAction(addLabel)

    l = 0

    for line in code.strip().split("\n"):
        l += 1
        i = 0

        imd1 = False
        imd2 = False

        # Remove any leading/trailing whitespace characters (including newline)
        line = line.strip()

        # Skip lines that start with a '#' (comments) or empty lines
        if not line or line.startswith('#'):
            continue

        try:
            parsed_instruction = instruction.parseString(line)
        
            if (parsed_instruction[i][0] == "Label"):
                i += 1
            intOpcode = 0

            if (parsed_instruction[i][1] == "HALT"):
                intOpcode = 65535
                intOpcode += parsed_instruction[i][3]

                temp = 0
                fileContents += f"{hex(int(intOpcode)):<6} {hex(temp):<6} {hex(temp):<6} {hex(temp):<6} # HALT \n"
                instructionNo += 4
                continue

            if (parsed_instruction[i][4] == True):
                intOpcode += 32768 # 2 ^ 15
                imd1 = True

            if (parsed_instruction[i][5] == True):
                intOpcode += 16384 # 2 ^ 14
                imd2 = True

            if (parsed_instruction[i][1] == "ALU"):
                intOpcode += 0 # 00
            elif (parsed_instruction[i][1] == "COND"):
                intOpcode += 4096 # 01
            elif (parsed_instruction[i][1] == "RAM"):
                intOpcode += 8192 # 10
            elif (parsed_instruction[i][1] == "IO"):
                intOpcode += 12288 # 11
            
            intOpcode += parsed_instruction[i][3]
            fileContents += f"{hex(int(intOpcode)):<6} "
            i += 1

            if (imd1):
                if (parsed_instruction[i][0] == "Immediate"):
                    fileContents += f"{hex(int(parsed_instruction[i][1])):<6} "
                elif (parsed_instruction[i][0] == "Label"):
                    if not parsed_instruction[i][1] in labels:
                        raise ValueError(f"Label '{parsed_instruction[i][1]}' is not defined.")
                    else:
                        fileContents += f"{hex(int(labels[parsed_instruction[i][1]])):<6} "
                else:
                    raise ValueError(f"OPCODE {parsed_instruction[i-1][2]} requires source 1 to be an immediate value")
            else:
                if (parsed_instruction[i][0] == "Register"):
                    fileContents += f"{hex(int(parsed_instruction[i][1])):<6} "
                else:
                    raise ValueError(f"OPCODE {parsed_instruction[i-1][2]} requires source 1 to be a register")
            
            i += 1

            if (imd2):
                if (parsed_instruction[i][0] == "Immediate"):
                    fileContents += f"{hex(int(parsed_instruction[i][1])):<6} "
                elif (parsed_instruction[i][0] == "Label"):
                    if not parsed_instruction[i][1] in labels:
                        raise ValueError(f"Label '{parsed_instruction[i][1]}' is not defined.")
                    else:
                        fileContents += f"{hex(int(labels[parsed_instruction[i][1]])):<6} "
                else:
                    raise ValueError(f"OPCODE {parsed_instruction[i-2][2]} requires source 2 to be an immediate value")
            else:
                if (parsed_instruction[i][0] == "Register"):
                    fileContents += f"{hex(int(parsed_instruction[i][1])):<6} "
                else:
                    raise ValueError(f"OPCODE {parsed_instruction[i-2][2]} requires source 2 to be a register")

            i += 1
            if (parsed_instruction[i][0] == "Label"):
                if not parsed_instruction[i][1] in labels:
                    raise ValueError(f"Label '{parsed_instruction[i][1]}' is not defined.")
                else:
                    fileContents += f"{hex(int(labels[parsed_instruction[i][1]])):<6} # {line} \n"
            else:
                fileContents += f"{hex(int(parsed_instruction[i][1])):<6} # {line} \n"

            instructionNo += 4
        except Exception as e:
            print(f"\nERROR [Line {l:05}, Instruction {instructionNo}] \n{line}\n{e}\n")
            exit()

    return fileContents
