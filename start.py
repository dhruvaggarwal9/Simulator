# import time
import sys
registers = [['zero', '0x0001000', 0], ['ra', '0x0001001', 0], ['sp', '0x0001002', 256], ['gp', '0x0001003', 0], ['tp', '0x0001004', 0], ['t0', '0x0001005', 0], ['t1', '0x0001006', 0], ['t2', '0x0001007', 0], ['s0', '0x0001008', 0], ['s1', '0x0001009', 0], ['a0', '0x000100a', 0], ['a1', '0x000100b', 0], ['a2', '0x000100c', 0], ['a3', '0x000100d', 0], ['a4', '0x000100e', 0], ['a5', '0x000100f', 0], ['a6', '0x0001010', 0], ['a7', '0x0001011', 0], ['s2', '0x0001012', 0], ['s3', '0x0001013', 0], ['s4', '0x0001014', 0], ['s5', '0x0001015', 0], ['s6', '0x0001016', 0], ['s7', '0x0001017', 0], ['s8', '0x0001018', 0], ['s9', '0x0001019', 0], ['s10', '0x000101a', 0], ['s11', '0x000101b', 0], ['t3', '0x000101c', 0], ['t4', '0x000101d', 0], ['t5', '0x000101e', 0], ['t6', '0x000101f', 0]]
mem={
    "0x00010000":"0b00000000000000000000000000000000",
    "0x00010004":"0b00000000000000000000000000000000",
    "0x00010008":"0b00000000000000000000000000000000",
    "0x0001000c":"0b00000000000000000000000000000000",
    "0x00010010":"0b00000000000000000000000000000000",
    "0x00010014":"0b00000000000000000000000000000000",
    "0x00010018":"0b00000000000000000000000000000000",
    "0x0001001c":"0b00000000000000000000000000000000",
    "0x00010020":"0b00000000000000000000000000000000",
    "0x00010024":"0b00000000000000000000000000000000",
    "0x00010028":"0b00000000000000000000000000000000",
    "0x0001002c":"0b00000000000000000000000000000000",
    "0x00010030":"0b00000000000000000000000000000000",
    "0x00010034":"0b00000000000000000000000000000000",
    "0x00010038":"0b00000000000000000000000000000000",
    "0x0001003c":"0b00000000000000000000000000000000",
    "0x00010040":"0b00000000000000000000000000000000",
    "0x00010044":"0b00000000000000000000000000000000",
    "0x00010048":"0b00000000000000000000000000000000",
    "0x0001004c":"0b00000000000000000000000000000000",
    "0x00010050":"0b00000000000000000000000000000000",
    "0x00010054":"0b00000000000000000000000000000000",
    "0x00010058":"0b00000000000000000000000000000000",
    "0x0001005c":"0b00000000000000000000000000000000",
    "0x00010060":"0b00000000000000000000000000000000",
    "0x00010064":"0b00000000000000000000000000000000",
    "0x00010068":"0b00000000000000000000000000000000",
    "0x0001006c":"0b00000000000000000000000000000000",
    "0x00010070":"0b00000000000000000000000000000000",
    "0x00010074":"0b00000000000000000000000000000000",
    "0x00010078":"0b00000000000000000000000000000000",
    "0x0001007c":"0b00000000000000000000000000000000",  
}
program_line = 1
# registers = {"zero":x0, "ra":r2, "sp":r3, "gp":0, "tp":0, "t0":0, "":0, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31}
def sign_extend(bits, size = 32, type_of_bit = "signed"):
    if type_of_bit == "unsigned":
        return "0"*(size-len(bits)) + bits
    elif type_of_bit in ("signed", "1s"):
        return bits[0]*(size-len(bits)) + bits
    elif type_of_bit == "2s":
        return bits[0]*(size-len(bits)) + bits
    return bits

def decimal_to_binary(decimal, num_bits = 32, type_of_bit = "signed"):
    if type_of_bit == "unsigned":
        binary = bin(decimal)[2:].zfill(num_bits)
        return binary
    if type_of_bit in ("signed", "1s"):
        if decimal >= 0:
            binary = decimal_to_binary(decimal, num_bits, "unsigned")
        else:
            binary = decimal_to_binary(abs(decimal), num_bits, "unsigned")
            binary = binary.replace("0", "2")
            binary = binary.replace("1", "0")
            binary = binary.replace("2", "1") 
        return binary
    if decimal >= 0:
        binary = bin(decimal)[2:].zfill(num_bits)
    else:
        positive_binary = bin(abs(decimal))[2:].zfill(num_bits)
        positive_binary = positive_binary.replace("0","2")
        positive_binary = positive_binary.replace("1","0")
        positive_binary = positive_binary.replace("2","1")
        inverted_binary = positive_binary
        invertedvalue = binary_to_decimal(inverted_binary, "unsigned")
        binary = decimal_to_binary(invertedvalue + 1, num_bits, "unsigned")
    return binary

def print1(registers):
    for i in registers:
        print(i[0],":",i[2])

def binary_to_decimal(binary, type_of_bit = "signed"):
    sum = 0
    if type_of_bit == "unsigned":
        for i in reversed(range(len(binary))):
            if binary[i] == "1":
                sum += 2**(len(binary)-1-i)
        return sum
    elif type_of_bit in ("signed", "1s"):
        if binary[0] == "1":
            binary = binary.replace("0", "2")
            binary = binary.replace("1", "0")
            binary = binary.replace("2", "1")
            return -binary_to_decimal(binary, "unsigned")
        else:
            return binary_to_decimal(binary, "unsigned")
    elif type_of_bit == "2s":
        if binary[0] == "1":
            binary = binary.replace("0", "2")
            binary = binary.replace("1", "0")
            binary = binary.replace("2", "1")
            return -(binary_to_decimal(binary, "unsigned") + 1)
        else:
            return binary_to_decimal(binary, "unsigned")
    else:
        return binary_to_decimal(binary, "signed")
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
    # print(binary)
    deci = 0
    deci = int(binary, 2)
    return deci


def R_Type(line , instruction, registers):
    global mem
    global program_line
    rd = line[-12:-7]
    rs1 = line[-20:-15]
    rs2 = line[-25:-20]
    if instruction == "add":
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] + registers[detectregister(rs2)][2] #sext
    if instruction == "sub":
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] - registers[detectregister(rs2)][2]
    if instruction == "sll":
        value = registers[detectregister(rs2)][2]
        if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
        else:
            binary_value = bin(value)[2:].zfill(32)
        x = binary_value [-5:]
        y = int(x, 2)
        result = binary_to_decimal(decimal_to_binary(registers[detectregister(rs1)][2])[y:]+'0'*y,type_of_bit='2s')
        registers[detectregister(rs1)][2] = result
    if instruction == "srl":
        value = registers[detectregister(rs2)][2]
        if value < 0:
            binary_value = bin(value & 0xFFFFFFFF)[2:] 
        else:
            binary_value = bin(value)[2:].zfill(32)
        x = binary_value [-5:]
        y = int(x, 2)
        result = binary_to_decimal('0'*y+decimal_to_binary(registers[detectregister(rs1)][2])[:32-y])
        registers[detectregister(rs1)][2] = result
    if instruction == "slt":
        if registers[detectregister(rs1)][2] < registers[detectregister(rs2)][2]: #sext
            registers[detectregister(rd)][2] =1
    if instruction == "sltu":
        if decimal_to_two_unsigned_to_decimal(registers[detectregister(rs1)][2]) < decimal_to_two_unsigned_to_decimal(registers[detectregister(rs2)][2]):
            registers[detectregister(rd)][2] =1
    if instruction == "xor" :
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] ^registers[detectregister(rs2)][2]
    if instruction == "or" :
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] | registers[detectregister(rs2)][2]
    if instruction == "and" :
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] & registers[detectregister(rs2)][2]
    program_line += 1
    
def twos_complement_to_decimal(binary):
    if binary[0] == '1':  
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal = -((int(inverted_binary, 2)) + 1)
    else:
        decimal = int(binary, 2)
    return decimal

def decimal_to_hexadecimal(decimal):
    hexadecimal = hex(decimal)[2:]  # Slice to remove '0x' prefix
    return hexadecimal

def S_Type(line , instruction, registers):
    global program_line
    global mem
    if instruction == "sw":
        rs2 = line[-25:-20]
        rs1 = line[-20:-15]
        imm = str(line[-32:-25])+str(line[-12:-7])
        mem["0x000" + decimal_to_hexadecimal((registers[detectregister(rs1)][2]+binary_to_decimal(imm, "2s")))] = "0b"+decimal_to_binary(registers[detectregister(rs2)][2], 32, "2s")
        # registers[detectregister(rs2)][2] = twos_complement_to_decimal(str((mem[f"0x000{str(decimal_to_hexadecimal(4*(registers[detectregister(rs1)][2]+twos_complement_to_decimal(str(imm)))))}"])[-32:]))
        program_line += 1
        # print("0x000" + decimal_to_hexadecimal((registers[detectregister(rs1)][2]+binary_to_decimal(imm, "2s"))))
        # print(int("0x000" + decimal_to_hexadecimal((registers[detectregister(rs1)][2]+binary_to_decimal(imm, "2s"))), 16))

def output_mem():
    global mem
    stringval = ""
    for i in range (32):
        stringval += (f'0x000{str(decimal_to_hexadecimal(65536+(4*i)))}:{mem[f"0x000{str(decimal_to_hexadecimal(65536+(4*i)))}"]}') + "\n"
    # print(stringval)
    return stringval
def J_Type(line , instruction, registers):
    global program_line
    global mem
    rd = line[-12:-7]
    imm = reverse(str(line[1:11]))+str(line[11])+reverse(str(line[12:20]))+str(line[0])
    imm = reverse(imm)
    immval = int(binary_to_decimal(imm)/2)
    if instruction == "jal":
        registers[detectregister(rd)][2] = (program_line + 1)*4 # (storing address of next instruction as return address in rd)
        program_line = program_line + immval
        # print(program_line)
        # PC = PC + sext({imm+'0'} (updating PC to label)    
def I_Type(line, instruction, registers):
    global program_line
    global mem
    imm = line[0:12]
    rs1 = line[12:17]
    rd = line[20:25]
    if instruction == "addi":
        registers[detectregister(rd)][2] = registers[detectregister(rs1)][2] + binary_to_decimal(imm, "2s")
        # print(registers[detectregister(rd)][0] + " :\t" + str(registers[detectregister(rd)][2]))
        program_line += 1
    elif instruction == "sltiu":
        if binary_to_decimal(registers[detectregister(rs1)][2], "unsigned") < binary_to_decimal(imm, "unsigned"):
            registers[detectregister(rd)][2] = 1
        else:
            registers[detectregister(rd)][2] = 0
        program_line += 1
    elif instruction == "lw":
        mc = mem["0x000" + decimal_to_hexadecimal((registers[detectregister(rs1)][2]+binary_to_decimal(imm, "2s")))]
        mc = mc.replace("0b", "")
        registers[detectregister(rd)][2] = binary_to_decimal(mc, "2s")
        program_line += 1
    elif instruction == "jalr":
        # registers[5][2] = (program_line + 1)*4
        # if detectregister(rd) != 0:
        registers[detectregister(rd)][2] = (program_line+1)*4
        # print(registers[detectregister(rd)][0] + " :\t" + str(registers[detectregister(rd)][2]))
        program_line = int(registers[detectregister(rs1)][2]/4) + int(binary_to_decimal(imm, "2s")/4)
        # print(program_line)     


def U_Type(line , instruction, registers):
    global mem
    global program_line
    rd = line[-12:-7]
    if instruction=="auipc":
        registers[detectregister(rd)][2] = detectregister(line[:-12]+'000000000000') + (program_line)*4
    if instruction=="lui":
        registers[detectregister(rd)][2] = detectregister(line[:-12]+'000000000000')
    program_line += 1


def reverse(string):
    string = string[::-1]
    return string

def B_Type(line , instruction, registers):
    global program_line
    global mem
    rs2 = line[7:12]
    rs1 = line[12:17]
    immv1 = line[0:7]
    immv2 = line[20:25]
    imm = immv1+immv2
    imm = reverse(reverse(imm[0:12]) + "0")
    immval = int(binary_to_decimal(imm, "2s")/4)
    # print(immval)
    if (immval < -program_line or immval > len(line)):
        imm = immv1+immv2
        imm = imm = reverse(reverse(imm[1:12]) + "1")
        immval = int(binary_to_decimal(imm, "2s")/4) - 1
        if (immval < -program_line or immval > len(line)):
            print("Warning..")
            immval = 1
    # print(immval)
    # registers[5][2] = (program_line + 1)*4
    # imm = str(line[-32])+str(line[-8])+str(line[-31:-25])+str(line[-12:-8])
    if instruction == "beq":
        if registers[detectregister(rs1)][2] == registers[detectregister(rs2)][2]:
            program_line = program_line + immval
            # print(program_line)
        else:
            program_line += 1
    if instruction == "bne":
        if registers[detectregister(rs1)][2] != registers[detectregister(rs2)][2]:
            program_line = program_line + immval
        else:
            program_line += 1
    if instruction == "blt":
        if registers[detectregister(rs1)][2] < registers[detectregister(rs2)][2]:
            program_line = program_line + immval
        else:
            program_line += 1
    if instruction == "bge":
        if registers[detectregister(rs1)][2] >= registers[detectregister(rs2)][2]:
            program_line = program_line + immval
        else:
            program_line += 1
    if instruction == "bltu":
        if binary_to_decimal(registers[detectregister(rs1)][2], "unsigned") < binary_to_decimal(registers[detectregister(rs2)][2], "unsigned"):
            program_line = program_line + immval
        else:
            program_line += 1
    if instruction == "bgeu":
        if binary_to_decimal(registers[detectregister(rs1)][2], "unsigned") >= binary_to_decimal(registers[detectregister(rs2)][2], "unsigned"):
            program_line = program_line + immval
        else:
            program_line += 1
    # print(f"{instruction}: ", program_line)

def bonus(line, instruction, registers):
    global program_line
    if instruction == "rst":
        for i in range(32):
            registers[i][2] = 0
        program_line += 1
    if instruction == "halt":
        pass
    if instruction == "rvrs":
        rd = line[-12:-7]
        rs1 = line[-20:-15]
        registers[detectregister(rd)][2] = decimal_to_binary(reverse(detectregister(rs1)), 32, "2s")
        program_line += 1
    if instruction == "mul":
        rs2 = line[7:12]
        rs1 = line[12:17]
        rd = line[20:25]
        if registers[detectregister(rs1)][2]*registers[detectregister(rs2)][2] < 2**(32):
            registers[detectregister(rd)][2] = registers[detectregister(rs1)][2]*registers[detectregister(rs2)][2]
        program_line += 1
import os

def input1():
    # dir_path_input = os.path.dirname(os.path.realpath(__file__)) + "/Input_Sim.txt"         # comment this for auto
    dir_path_input = sys.argv[-2]                                                             # uncomment this for auto
    with open(dir_path_input,"r") as f:
        data=f.read()
        # print(data)
        f.close()
    # dir_path_output = os.path.dirname(os.path.realpath(__file__)) + "/Output_Sim.txt"        # comment this for auto
    dir_path_output = sys.argv[-1]                                                           # uncomment this for auto
    global program_line
    global mem
    # data = ""
    # data1 = data
    # print(data1)
    outdata = ""
    # while True:
    #     # data1 = input()
    #     if data1 == "":
    #         break
        # data += data1 + "\n"
    line=data.split("\n")
    if line[-1] == "":
        line.remove('')
    # line.append("00000000000000000000000001100011")
    program_line = 0
    while (program_line <= len(line)):
        program_line = int(program_line)
        i = program_line
        i = int(i)
        check_insta = check_inst(line[int(i)])
        # print(check_insta)
        if check_insta[1]=='bonus':
            bonus(line[i],check_insta[0],registers)
            if check_insta[0]=='rst':
                pass
            elif check_insta[0]=='halt':
                # print("0b" + decimal_to_binary(program_line*4), end = " ")
                registers[0][2] = 0
                outdata += "0b" + decimal_to_binary(program_line*4) + " " + output(registers) + "\n"
                # print(output(registers))
                break
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
        # print("0b" + decimal_to_binary(program_line*4), end = " ")
        registers[0][2] = 0
        outdata += "0b" + decimal_to_binary(program_line*4) + " " + output(registers) + "\n"
        # print1(registers)
        # print(output(registers))
    with open(dir_path_output, "w") as f:
        f.write(outdata)
        f.write(output_mem())
input1()
