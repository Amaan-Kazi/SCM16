from lark import Lark
from compiler.codegenerator import CodeGenerator
from compiler.assembler import Assemble


## PARSER ##

with open('./compiler/grammar.lark') as file:
    grammar = file.read()

parser = Lark(grammar)

scmCodeFile = input("SCMCODE File Name [in /code/SCMCODE, no extension]: ")
print("\n")

with open(f"code/SCMCODE/{str(scmCodeFile)}.scmcode", "r") as file:
    scmCode = file.read()

parseTree = parser.parse(scmCode)
print(parseTree.pretty())

print("--------------------------------------------------------")


## CODE GENERATOR ##

transformer = CodeGenerator()
transformer.transform(parseTree)

generated_code = transformer.generate_code()
print(f"Generated Code [code/SCMA/{str(scmCodeFile)}.scma]:")
print(generated_code)

with open(f"code/SCMA/{str(scmCodeFile)}.scma", "w") as file:
    file.write(generated_code)

print("\n--------------------------------------------------------")


## ASSEMBLER ##

assembled_code = Assemble(generated_code)
print(f"Assembled Code [code/ASM/{str(scmCodeFile)}.assembly]:\n")
print(assembled_code)

with open(f"code/ASM/{str(scmCodeFile)}.assembly", "w") as file:
    file.write(assembled_code)

print("\n--- Compiled Succesfully ---\n")
