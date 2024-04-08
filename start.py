r0 = 0
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0
r6 = 0
r7 = 0
r8 = 0
r9 = 0
r10 = 0
r11 = 0
r12 = 0
r13 = 0
r14 = 0
r15 = 0
r16 = 0
r17 = 0
r18 = 0
r19 = 0
r20 = 0
r21 = 0
r22 = 0
r23 = 0
r24 = 0
r25 = 0
r26 = 0
r27 = 0
r28 = 0
r29 = 0
r30 = 0
r31 = 0

registers = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31]

def check_inst(line):
    if (line=="00000000000000000010000000000000"):
        return ["halt","bonus"]
    if (line=="00000000000000000000000000000000"):
        return ["rst","bonus"]
    opcode=line[-7:]
    funct3=line[-15:-12]
    funct7=line[:7]
    if opcode=="0000000" and funct3=="001":
        return ["rvrs","bonus"]
    if opcode=="0000000" and funct3=="011":
        return ["mul","bonus"]
    if opcode=="0110011":
        if funct3=="000":
            if funct7=="0000000":
                return ["add","r"]
            if funct7=="0100000":
                return ["sub","r"]
        if funct3=="001":
            return ["sll","r"]
        if funct3=="010":
            return ["slt","r"]
        if funct3=="011":
            return ["sltu","r"]
        if funct3=="100":
            return ["xor","r"]
        if funct3=="101":
            return ["srl","r"]
        if funct3=="110":
            return ["or","r"]
        if funct3=="111":
            return ["and","r"]
    if opcode=="0000011":
        return ["lw","i"]
    if opcode=="0010011":
        if funct3=="000":
            return ["addi","i"]
        if funct3=="011":
            return ["sltiu","i"]
    if opcode=="1100111":
        return ["jalr","i"]
    if opcode=="0100011":
        return ["sw","s"]
    if opcode=="1100011":
        if funct3=="000":
            return ["beq","b"]
        if funct3=="001":
            return ["bne","b"]
        if funct3=="100":
            return ["blt","b"]
        if funct3=="101":
            return ["bge","b"]
        if funct3=="110":
            return ["bltu","b"]
        if funct3=="111":
            return ["bgeu","b"]
    if opcode=="0110111":
        return ["lui","u"]
    if opcode=="0010111":
        return ["auipc","u"]
    if opcode=="1101111":
        return ["jal","j"]


def output(registers):
     binary_representations = []
     for value in registers:
        if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
        else:
            binary_value = bin(value)[2:].zfill(32)
        binary_representations.append('0b' + binary_value +" ")
     return ''.join(binary_representations)

def detectregister(binary):
    return int(binary, 2)


def R_Type(line , instruction, registers):
     rd = line[-12:-7]
     rs1 = line[-20:-15]
     rs2 = line[-25,-20]
     if instruction == "add":
         registers[detectregister(rd)] = registers[detectregister[rs1]] + registers[detectregister[rs2]] #sext
     if instruction == "sub":
         registers[detectregister(rd)] = 0 - registers[detectregister[rs2]]
     if instruction == "sll":
         value = registers[detectregister[rs2]]
         if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
         else:
            binary_value = bin(value)[2:].zfill(32)
         x = binary_value [-5:]
         y = int(x, 2)
         result = registers[detectregister[rs1]] << y
         registers[detectregister[rs1]] = result
     if instruction == "srl":
         value = registers[detectregister[rs2]]
         if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
         else:
            binary_value = bin(value)[2:].zfill(32)
         x = binary_value [-5:]
         y = int(x, 2)
         result = registers[detectregister[rs1]] >> y
         registers[detectregister[rs1]] = result
     if instruction == "slt":
         if registers[detectregister[rs1]] < registers[detectregister[rs2]]: #sext
             registers[detectregister[rd]] =1
     if instruction == "sltu":
         if registers[detectregister[rs1]] < registers[detectregister[rs2]]:
             registers[detectregister[rd]] =1
     if instruction == "xor" :
         registers[detectregister(rd)] = registers[detectregister[rs1]] ^registers[detectregister[rs2]]
     if instruction == "xor" :
         registers[detectregister(rd)] = registers[detectregister[rs1]] | registers[detectregister[rs2]]
     if instruction == "xor" :
         registers[detectregister(rd)] = registers[detectregister[rs1]] & registers[detectregister[rs2]]
         
