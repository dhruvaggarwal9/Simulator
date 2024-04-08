registers = [['zero', '0b00000000000000000000000000000000', 0], ['ra', '0b00000000000000000000000000000001', 0], ['sp', '0b00000000000000000000000000000010', 0], ['gp', '0b00000000000000000000000000000011', 0], ['tp', '0b00000000000000000000000000000100', 0], ['t0', '0b00000000000000000000000000000101', 0], ['t1', '0b00000000000000000000000000000110', 0], ['t2', '0b00000000000000000000000000000111', 0], ['s0', '0b00000000000000000000000000001000', 0], ['s1', '0b00000000000000000000000000001001', 0], ['a0', '0b00000000000000000000000000001010', 0], ['a1', '0b00000000000000000000000000001011', 0], ['a2', '0b00000000000000000000000000001100', 0], ['a3', '0b00000000000000000000000000001101', 0], ['a4', '0b00000000000000000000000000001110', 0], ['a5', '0b00000000000000000000000000001111', 0], ['a6', '0b00000000000000000000000000010000', 0], ['a7', '0b00000000000000000000000000010001', 0], ['s2', '0b00000000000000000000000000010010', 0], ['s3', '0b00000000000000000000000000010011', 0], ['s4', '0b00000000000000000000000000010100', 0], ['s5', '0b00000000000000000000000000010101', 0], ['s6', '0b00000000000000000000000000010110', 0], ['s7', '0b00000000000000000000000000010111', 0], ['s8', '0b00000000000000000000000000011000', 0], ['s9', '0b00000000000000000000000000011001', 0], ['s10', '0b00000000000000000000000000011010', 0], ['s11', '0b00000000000000000000000000011011', 0], ['t3', '0b00000000000000000000000000011100', 0], ['t4', '0b00000000000000000000000000011101', 0], ['t5', '0b00000000000000000000000000011110', 0], ['t6', '0b00000000000000000000000000011111', 0]]

# registers = {"zero":x0, "ra":r2, "sp":r3, "gp":0, "tp":0, "t0":0, "":0, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31}

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
        if value[2] < 0:
            binary_value = bin(value[2] & 0xFFFFFFFF)[2:] 
        else:
            binary_value = bin(value[2])[2:].zfill(32)
        binary_representations.append('0b' + binary_value +" ")
     return ''.join(binary_representations)

def detectregister(binary):
    return int(binary, 2)

def decimal_to_two_unsigned_to_decimal(decimal):
    num_bits=32
    if decimal >= 0:
        binary = bin(decimal)[2:].zfill(num_bits)
    else:
        positive_binary = bin(abs(decimal))[2:].zfill(num_bits)
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
        binary = bin(int(inverted_binary, 2) + 1)[2:].zfill(num_bits)
    print(binary)
    deci = 0
    deci = int(binary, 2)
    
    return deci


def R_Type(line , instruction, registers):
     rd = line[-12:-7]
     rs1 = line[-20:-15]
     rs2 = line[-25,-20]
     if instruction == "add":
         registers[detectregister(rd)][2] = registers[detectregister[rs1]][2] + registers[detectregister[rs2]][2] #sext
     if instruction == "sub":
         registers[detectregister(rd)][2] = 0 - registers[detectregister[rs2]][2]
     if instruction == "sll":
         value = registers[detectregister[rs2]][2]
         if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
         else:
            binary_value = bin(value)[2:].zfill(32)
         x = binary_value [-5:]
         y = int(x, 2)
         result = registers[detectregister[rs1]][2] << y
         registers[detectregister[rs1]][2] = result
     if instruction == "srl":
         value = registers[detectregister[rs2]][2]
         if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
         else:
            binary_value = bin(value)[2:].zfill(32)
         x = binary_value [-5:]
         y = int(x, 2)
         result = registers[detectregister[rs1]][2] >> y
         registers[detectregister[rs1]][2] = result
     if instruction == "slt":
         if registers[detectregister[rs1]][2] < registers[detectregister[rs2]][2]: #sext
             registers[detectregister[rd]][2] =1
     if instruction == "sltu":
         if decimal_to_two_unsigned_to_decimal(registers[detectregister[rs1]][2]) < decimal_to_two_unsigned_to_decimal(registers[detectregister[rs2]][2]):
             registers[detectregister[rd]][2] =1
     if instruction == "xor" :
         registers[detectregister(rd)][2] = registers[detectregister[rs1]][2] ^registers[detectregister[rs2]][2]
     if instruction == "or" :
         registers[detectregister(rd)][2] = registers[detectregister[rs1]][2] | registers[detectregister[rs2]][2]
     if instruction == "and" :
         registers[detectregister(rd)][2] = registers[detectregister[rs1]][2] & registers[detectregister[rs2]][2]
    
def input():
    with open("File1.txt","r") as f:
            data=f.read()
            line=data.split('\n')
            for i in range(len(line)):
                check_insta = check_inst(line)
                if check_insta[1]=='bonus':
                    bonus(line[i],check_insta[0],registers)
                elif check_insta[1]=='r':
                    R_Type(line[i],check_insta[0],registers)
                elif check_insta[1]=='i':
                    I_Type(line[i],check_insta[0],registers)
                elif check_insta[1]=='s':
                    S_Type(line[i],check_insta[0],registers)
                elif check_insta[1]=='b':
                    B_Type(line[i],check_insta[0],registers)
                elif check_insta[1]=='u':
                    U_Type(line[i],check_insta[0],registers)
                elif check_insta[1]=='j':
                    J_Type(line[i],check_insta[0],registers)
