try:
    import tkinter as tk
    import tkinter.filedialog
except:
    a = 0
import os
import sys

class code_instructions():
    # dict1 = {"rs": 0, "rd": 0, "rt": 0, "imm": 0, "PC": 0, "sp": 0}
    operations_3_order = ["add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and", "lw", "addi", "sltiu", "jalr", "beq", "bne", "blt", "bge", "bltu", "bgeu", "lw", "mul"]
    operations_2_order = ["sw", "lw", "auipc", "lui", "jal", "rvrs"]
    operations_1_order = []
    operations_0_order = ["rst", "halt"]
    operations_all = [operations_0_order, operations_1_order, operations_2_order, operations_3_order]
    Instructions = {"R":{"add":["0110011","000","0000000"],"sub":["0110011","000","0100000"],"sll":["0110011","001","0000000"],"slt":["0110011","010","0000000"],"sltu":["0110011","011","0000000"],"xor":["0110011","100","0000000"],"srl":["0110011","101","0000000"],"or":["0110011","110","0000000"],"and":["0110011","111","0000000"]},"I":{"lw":["0000011","010"],"addi":["0010011","000"],"sltiu":["0010011","011"],"jalr":["1100111","000"]},"S":{"sw":["0100011","010"]},"B":{"beq":["1100011","000"],"bne":["1100011","001"],"blt":["1100011","100"],"bge":["1100011","101"],"bltu":["1100011","110"],"bgeu":["1100011","111"]},"U":{"lui":["0110111"],"auipc":["0010111"]},"J":{"jal":["1101111"]}, "BONUS" : {"rst":["0000000","000"],"rvrs":["0000000","001"],"halt":["0000000","010"],"mul":["0000000","011"]}}
    dic_operations_type = {"R": ["add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and"], "I":["lw", "addi", "sltiu", "jalr"], "S":["sw"], "U":["auipc", "lui"], "J":["jal"], "B":["beq", "bne", "blt", "bgeu", "bge", "bltu"], "BONUS" : ["rvrs", "rst", "halt", "mul"]}
    registers_list=['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1','a0','a1','a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']
class Assembler:
    def __init__(self,a=1, textfiledir = "", outputdir = "bin.txt"):
        self.root = tk.Tk()
        self.a = a
        self.outputdir = outputdir
        self.filedirectory = textfiledir
        path = os.path.realpath(__file__).split("\\")[:-1]
        self.folderdirectory = ""
        for i in path:
            self.folderdirectory += i + "\\"
        self.root.title("Assembler")
        # self.variables = code_instructions.dict1
        self.registers_list=code_instructions.registers_list
        self.dict = code_instructions.dic_operations_type
        self.lastline = 0
        self.labelcount = 0
        self.labels = {}
        if a==1:
            self.code_ground = tk.Label(self.root, text="Code", font="Arial 12 bold", fg="black")
            self.code_ground.grid(row=0, column=0)
            self.output_ground = tk.Label(self.root, text="Output", font="Arial 12 bold", fg="black")
            self.output_ground.grid(row=0, column=2)
            self.text = tk.Text(self.root, height=60, width=100, wrap="word")
            self.text.grid(row=1, column=0)
            self.outtext = tk.Text(self.root, state="disabled", height=60, width=70, wrap="word")
            self.seperator = tk.Frame(self.root, width=20, height=60)
            self.seperator.grid(row=0, column=1)
            self.outtext.grid(row=1, column=2)
            self.menu_bar = tk.Menu(self.root)
            self.root.config(menu=self.menu_bar)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.file_menu.add_command(label="New", command=self.new_file)
            self.file_menu.add_command(label="Open", command=self.open_file)
            self.file_menu.add_command(label="Save", command=self.save_file)
            self.file_menu.add_command(label="Save As", command=self.saveas_file)
            self.file_menu.add_command(label="Exit", command=self.exit)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)
            # self.defset_menu = tk.Menu(self.menu_bar, tearoff=0)
            # self.defset_menu.add_command(label="rs", command = lambda: self.change_val("rs"))
            # self.defset_menu.add_command(label="rd", command = lambda: self.change_val("rd"))
            # self.defset_menu.add_command(label="rt", command = lambda: self.change_val("rt"))
            # self.menu_bar.add_cascade(label = "Default Settings", menu=self.defset_menu)
            self.menu_bar.add_cascade(label="Run", command=lambda: self.output(self.text.get(1.0, tk.END)))
            self.root.config(menu=self.menu_bar)
        else:
            if self.filedirectory == "":
                self.outputprint("No file selected\n")
            else:
                self.output(self.read_file())
    def commentsremover(self, fullcode, sym = "//"):
        # fullcode = fullcode.replace("\t", "")
        if fullcode == "":
            return ""
        try:
            while fullcode != "" and fullcode[-1] in [" ","\t"]:
                fullcode = fullcode[:-1]
        except:
            print(fullcode)
            print(type(fullcode))
        fullcode = fullcode.split("\n")
        if fullcode == [""]:
            return ""
        while fullcode != [""] and fullcode[-1] == "":
            fullcode.pop()
        for i in range(len(fullcode)):
            fullcode[i] = fullcode[i].split(sym)[0]
            smallcode = fullcode[i]
            if smallcode == "":
                continue
            while smallcode != "" and smallcode[-1] in [" ","\t"]:
                smallcode = smallcode[:-1]
            fullcode[i] = smallcode
            # for j in range(len(smallcode), 0, -1):
            #         if smallcode[j-1] == "":
            #             smallcode.pop(j-1)
            #         else:
            #             break
            # fullcode[i] = " ".join(smallcode)
        return "\n".join(fullcode)
    def inputerrorcheck(self, fullcode):
        fullcode = self.commentsremover(fullcode)
        fullcode = fullcode.split("\n")
        error = ""
        for i in range(len(fullcode)):
            smallcode = fullcode[i]
            spacecount = 0
            for j in range(len(smallcode)):
                if smallcode[j] == " ":
                    spacecount += 1
                if spacecount > 1:
                    error += smallcode + "\n" + " "*j + "^\n"
                    error += f"Error on line {i} -> Invalid spacing in code instruction on line {i}\n\n"
                    break
        return error   
    def labelcheck(self, code, line):
        label = ""
        for i in reversed(range(0,len(code))):
            if code[i]==':':
                label =  code[:i]
                break
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', " "]
        for i in label:
            if i in symbols:
                self.outputprint(f"(Line {line}) -> Invalid label on line {line}\n")
                raise Exception(f"(Line {line}) -> Invalid label on line {line}\n")
        return label
    def searchlabel(self, label, fromline):
        a = "0"
        lablesno = self.labelcount
        tabcount = lablesno
        try:
            fullcode = self.commentsremover(self.read_file())
        except:
            print(self.read_file())
        fullcode = fullcode.split("\n")[fromline:]
        for i in range(len(fullcode)):
            labelfound = self.labelcheck(fullcode[i], fromline+i)
            lablesno += 1
            tabcount += 1
            temptabcount = 0
            for j in range(len(labelfound)):
                if labelfound[j] == "\t":
                    temptabcount += 1
                else:
                    break
            if temptabcount > tabcount:
                self.outputprint(f"(Line {fromline+i}) -> Invalid Tab Count on line {fromline+i}\n")
                raise Exception(f"(Line {fromline+i}) -> Invalid Tab Count on line {fromline+i}\n")
            elif temptabcount < tabcount:
                tabcount = temptabcount
                lablesno -= 1
            else:
                pass
            if labelfound == "":
                continue
            while (labelfound[0] == "\t"):
                labelfound = labelfound[1:]
            while (labelfound[0] == " "):
                self.outputprint(f"(Line {fromline+i}) -> Invalid spacing on line {fromline+i}\n")
                raise Exception(f"(Line {fromline+i}) -> Invalid spacing on line {fromline+i}\n")
            if labelfound == label:
                self.labels[label] = fromline+i+1
                a = "1"
        if a == "0":
            self.outputprint(f"Label {label} not found\n")
            raise Exception(f"Label {label} not found\n")        
    def output(self, code):
        self.labelcount = 0
        self.labels = {}
        if self.a==1:
            self.outtext.config(state="normal")
            self.outtext.delete("1.0", tk.END)
            self.outtext.config(state = "normal")
        else:
            print("Output::\n")
        # basicerror = self.inputerrorcheck(fullcode)
        # if basicerror != "":
        #     self.outputprint(basicerror)
        #     raise Exception(basicerror)
        if self.outputdir == "":
            outdir = self.folderdirectory + "bin.txt"
        else:
            outdir = self.outputdir
        with open(outdir, "w") as file:
            code = code.split("\n")
            while code[-1] == "" and code != [""]:
                code.pop()
            self.lastline = len(code)
            for i in range(1, len(code)+1):
                codesmall = code[i-1]
                text = self.code_assembler(codesmall, i)
                if text != "":
                    self.outputprint(f"Line {i} -> {codesmall} -> \n")
                    self.outputprint(f"{text}\n")
                    file.write(text + "\n")
        file.close()
        self.outputprint("bin created Successfully!\n"+f"at ::\t {self.outputdir}\n\n")
    def code_extracter(self, code, line): #returns the instruction
        codesmall = code.split(" ")
        instruction = ""
        if len(codesmall) == 1:
            if codesmall[0] in code_instructions.operations_all[0]:
                return codesmall[0]
            if self.a == 1:
                self.outtext.config(state="normal")
            self.outputprint(f"(Line {line}) -> Invalid instruction on line {line}\n")
            raise Exception(f"(Line {line}) -> Invalid instruction on line {line}\n")
        order = len(codesmall[1].split(","))
        if order > 3:
            if self.a == 1:
                self.outtext.config(state="normal")
            self.outputprint(f"(Line {line}) -> Invalid number of attributes/parameters. On line {line}\n")
            raise Exception(f"(Line {line}) -> Invalid number of attributes/parameters. On line {line}\n")
        for i in code_instructions.operations_all[order]:
            if codesmall[0] == i:
                instruction = i
                break
        if instruction == "":
            if self.a == 1:
                self.outtext.config(state="normal")
            self.outputprint(f"(Line {line}) -> Invalid instruction for {order} attributes/parameters.\n")
            raise Exception(f"(Line {line}) -> Invalid instruction for {order} attributes/parameters. On line {line}\n")
        return instruction
    def get_type(self, instruction, line):
        for i in self.dict:
            if instruction in self.dict[i]:
                # if i == "BONUS":
                #     self.outputprint(f"Warning: (Line {line}) -> Bonus type instruction is not added. Error not enough Information.\n")
                return i
        self.outputprint(f"(Line {line}) -> Invalid instruction on line {line}\n")
        raise Exception(f"(Line {line}) -> Invalid instruction on line {line}\n")
    def int_to_binary(self, value, line, le = 32):
        if type(value) != int:
            self.outputprint(f"Error! on Line {line} : Invalid Value: Value not integer\n")
            raise Exception(f"Error! on Line {line} : Invalid Value: Value not integer")
        binary_str = ""
        for i in range(le-1, -1, -1):
            bit_value = 1 << i
            if value & bit_value:
                binary_str += "1"
            else:
                binary_str += "0"
        return binary_str
    def reverse_string(self, s):
        return s[::-1]
    def immediate(self, value, instr_type, line):
        binary_representation = self.int_to_binary(value, line)
        binary_representation = self.reverse_string(binary_representation)
        if instr_type == 'I':
            return self.reverse_string(binary_representation[0:12])
        elif instr_type == 'S':
            return self.reverse_string(binary_representation[5:12])
        elif instr_type == 'U':
            return self.reverse_string(binary_representation[12:32])
        elif instr_type == 'J':
            return binary_representation[20] + self.reverse_string(binary_representation[1:11]) + binary_representation[11] + self.reverse_string(binary_representation[12:20])
        elif instr_type == 'B':
            return binary_representation[12] + self.reverse_string(binary_representation[5:11])  + self.reverse_string(binary_representation[1:5]) + binary_representation[11]
        else:
            return ""
    def decimal_to_binary(self ,n ,line ,le=5):
        if type(n)!=int:
            self.outputprint(f"Error! on Line {line} : Invalid Value: Value not integer\n")
            raise Exception(f"Error! on Line {line} : Invalid Value: Value not integer\n")
        if n < (-(2**(le-1)-1)) and n > (2**(le-1)-1):
            self.outputprint(f"Error! on Line {line} : Value out of range\n")
            raise Exception(f"Error! on Line {line} : Value out of range\n")
        binary=''
        m=n
        if (m==0):
            binary=binary+str(0)
        else:
            while (m!=0):
                r=m%2
                binary=str(r)+binary
                m=int(m/2)
        if(len(binary)==le):
            return (binary)
        else:
            binary='0'*(le-len(binary))+binary
            return binary
    def register_encoding(self, register_name, line):
        registers_list=self.registers_list
        if (register_name=='fp'):
            return self.decimal_to_binary(8, line)
        elif (register_name in registers_list):
            for i in range(32):
                if (registers_list[i]==register_name):
                    return self.decimal_to_binary(i, line)
        else:
            self.outputprint(f"Error! on Line {line} : Invalid Register Name\n")
            raise Exception(f"Error! on Line {line} : Invalid Register Name")
    def getopcode(self, Instruction_type,ins):
        return code_instructions.Instructions[Instruction_type][ins][0]
    def getfunc3(self, Instruction_type,ins):
        return code_instructions.Instructions[Instruction_type][ins][1]
    def getfunct7(self, Instruction_type,ins):
        return code_instructions.Instructions[Instruction_type][ins][2]
    def code_assembler(self, code, line=0):
        tabcount = 0
        # spacecount = 0
        code = self.commentsremover(code)
        if code == "":
            return ""
        for i in range(len(code)):
            if code[i] == "\t":
                tabcount += 1
            # elif code[i] == " ":
            #     spacecount += 1
            #     if spacecount%4!=0:
            #         self.outputprint(f"(Line {line}) -> Invalid spacing on line {line}\n")
            #         raise Exception(f"(Line {line}) -> Invalid spacing on line {line}\n")
            #     tabcount = spacecount/4
            else:
                break
        if tabcount > self.labelcount:
            self.outputprint(f"(Line {line}) -> Invalid Tab Count on line {line}\n")
            raise Exception(f"(Line {line}) -> Invalid Tab Count on line {line}\n")
        elif tabcount < self.labelcount:
            self.labelcount = tabcount
        else:
            pass
        for i in range(len(code)):
            if code[i] != "\t":
                code = code[i:]
                break
        label = self.labelcheck(code, line)
        if label != "":
            self.labelcount += 1
            self.labels[label] = line
            code = code.split(label + ":")[1]
        for i in range(len(code)):
            if code[i] not in [" ", "\t"]:
                code = code[i:]
                break
        if code == "":
            return ""
        if self.inputerrorcheck(code) != "":
            print(self.inputerrorcheck(code))
            self.outputprint(self.inputerrorcheck(code))
            raise Exception(self.inputerrorcheck(code))
        instruction = self.code_extracter(code, line)
        instype = self.get_type(instruction, line)
        if code == "addi x0,x0,0":
            return ""
        if line == self.lastline:
            if code != "beq zero,zero,0x00000000" and code != "beq zero,zero,0" and code!="halt":
                self.outputprint(f"(Line {line}) -> Invalid Syntax: Last line should be halt\n")
                raise Exception(f"(Line {line}) -> Invalid Syntax: Last line should be halt\n")
        if instype=="R":
            opcode = self.getopcode(instype, instruction)
            func3 = self.getfunc3(instype, instruction)
            func7 = self.getfunct7(instype, instruction)
            stringtoprint = ""
            stringtoprint = opcode + stringtoprint
            code = code.split(" ")[1]
            code = code.split(",")
            for i in range(len(code)):
                if code[i] in ["", " "]:
                    code.pop(i)
            stringtoprint = self.register_encoding(code[0], line) + stringtoprint
            # j = 0
            # for i in self.dict["R"]:
            #     if instruction == i:
            #         break
            #     j += 1
            stringtoprint = func3 + stringtoprint
            for i in range(1, len(code)):
                stringtoprint = self.register_encoding(code[i], line) + stringtoprint
            stringtoprint = func7 + stringtoprint
            return stringtoprint

        elif instype=="I":
            if instruction == "lw" and "(" in code and ")" in code:
                code = code.replace("(", ",")
                code = code.replace(")", "")
                code = code.split(",")
                code.append(code[-2])
                code.pop(-3)
                code = ",".join(code)
            opcode = self.getopcode(instype, instruction)
            func3 = self.getfunc3(instype, instruction)
            stringtoprint = ""
            stringtoprint = opcode + stringtoprint
            code = code.split(" ")[1]
            code = code.split(",")
            for i in range(len(code)):
                if code[i] in ["", " "]:
                    code.pop(i)
            try:
                immval = int(code[2])
            except Exception as e:
                self.outputprint(f"(Line {line}) -> Invalid immediate value on line {line}\n")
                raise Exception(f"(Line {line}) -> Invalid immediate value on line {line}\n")
            imm = self.immediate(immval, instype, line)
            stringtoprint = self.register_encoding(code[0], line) + stringtoprint
            # j = 0
            # for i in self.dict["R"]:
            #     if instruction == i:
            #         break
            #     j += 1
            stringtoprint = func3 + stringtoprint
            for i in range(1, len(code)-1):
                stringtoprint = self.register_encoding(code[i], line) + stringtoprint
            stringtoprint = imm + stringtoprint
            return stringtoprint

        elif instype=="S":
            opcode = self.getopcode(instype, instruction)
            func3 = self.getfunc3(instype, instruction)
            code = code.split(" ")[1]
            code = code.split(",")
            if "(" in code[1] and ")" in code[1]:
                code.append(code[1].split("(")[0])
                code[1] = (code[1].split("(")[1])
                code[1] = code[1].split(")")[0]
            else:
                self.outputprint(f"(Line {line}) -> Invalid Syntax: Bracket Missing for store instruction/Immediate on line {line}\n")
                raise Exception(f"(Line {line}) -> Invalid Syntax: Bracket Missing for store instruction/Immediate on line {line}\n")
            try:
                immval = int(code[2])
            except:
                self.outputprint(f"(Line {line}) -> Invalid immediate value on line {line}\n")
                raise Exception(f"(Line {line}) -> Invalid immediate value on line {line}\n")
            code.pop(2)
            stringtoprint = opcode
            stringtoprint = func3 + self.int_to_binary(immval, line, 12)[-5:] + stringtoprint
            for i in reversed(range(0, len(code))):
                stringtoprint = self.register_encoding(code[i], line) + stringtoprint
            stringtoprint = self.int_to_binary(immval, line, 12)[:-5] + stringtoprint
            return stringtoprint
        
        elif instype=="U":
            opcode = self.getopcode(instype, instruction)
            code = code.split(" ")[1].split(",")
            try:    immval = int(code[1])
            except:
                self.outputprint(f"(Line {line}) -> Invalid immediate value on line {line}\n")
                raise Exception(f"(Line {line}) -> Invalid immediate value on line {line}\n")
            
            imm = self.immediate(immval, instype, line)
            stringtoprint = ""
            stringtoprint += imm
            stringtoprint += self.register_encoding(code[0], line)
            stringtoprint += opcode
            return stringtoprint
        
        elif instype=="J":
            opcode = self.getopcode(instype, instruction)
            code = code.split(" ")[1].split(",")
            immval=0
            try:
                immval += int(code[1])
            except:
                if code[1] in self.labels:
                    immval += self.labels[code[1]] - line + self.emptylinecheck(line)-self.emptylinecheck(self.labels[code[1]])
                if code[1] not in self.labels:
                    self.searchlabel(code[1], line)
                    immval += self.labels[code[1]] - line + self.emptylinecheck(line)-self.emptylinecheck(self.labels[code[1]])
                immval *= 4
            stringtoprint = self.immediate(immval,instype, line) + self.register_encoding(code[0], line) + opcode
            return stringtoprint
        
        elif instype=="B":
            opcode = self.getopcode(instype, instruction)
            func3 = self.getfunc3(instype, instruction)
            if line == self.lastline:
                if (code == "beq zero,zero,0x0000000"):
                    code = "beq zero,zero,0"
                elif (code == "beq zero,zero,0"):
                    code = "bne zero,zero,0"
                else:
                    self.outputprint(f"(Line {line}) -> Invalid Syntax: Last line should be halt\n")
                    raise Exception(f"(Line {line}) -> Invalid Syntax: Last line should be halt\n")
            code = code.split(" ")[1].split(",")
            immval = 0
            try:
                immval += int(code[2])
            except:
                if code[2] in self.labels:
                    immval += self.labels[code[2]] - line + self.emptylinecheck(line)-self.emptylinecheck(self.labels[code[2]])
                if code[2] not in self.labels:
                    self.searchlabel(code[2], line)
                    immval += self.labels[code[2]] - line + self.emptylinecheck(line)-self.emptylinecheck(self.labels[code[2]])
                immval *= 4

            imm = self.immediate(immval, "B", line)
            immv1 = imm[-5:]
            immv2 = imm[:-5]
            stringtoprint = ""
            stringtoprint = opcode + stringtoprint
            stringtoprint = func3 + immv1 + stringtoprint
            for i in (range(0, len(code)-1)):
                stringtoprint = self.register_encoding(code[i],line) + stringtoprint
            stringtoprint = immv2 + stringtoprint
            return stringtoprint
        elif instype=="BONUS":
            opcode = self.getopcode(instype, instruction)
            func3 = self.getfunc3(instype, instruction)
            if instruction == "halt":
                return "0"*(32-15)+func3+"00000"+opcode
            elif instruction == "rst":
                return "0"*(32-15)+func3+"00000"+opcode
            elif instruction == "rvrs":
                code = code.split(" ")[1].split(",")
                return "0"*12+ self.register_encoding(code[1], line)+ func3 + self.register_encoding(code[0],line) +opcode
            elif instruction == "mul":
                stringtoprint = ""
                stringtoprint = opcode + stringtoprint
                code = code.split(" ")[1]
                code = code.split(",")
                stringtoprint = self.register_encoding(code[0], line) + stringtoprint
                code.pop(0)
                stringtoprint = func3 + stringtoprint
                for i in range(len(code)):
                    stringtoprint = self.register_encoding(code[i], line) + stringtoprint
                stringtoprint = "0"*7 + stringtoprint
                return stringtoprint
            
    def emptylinecheck(self, line):
        fullcode = self.commentsremover(self.read_file())
        fullcode = fullcode.split("\n")[:line]
        emptlylinecount = 0
        for i in range(len(fullcode)):
            if fullcode[i] == "":
                emptlylinecount += 1
        return emptlylinecount
    def new_file(self):
        self.newroot = tk.Tk()
        self.newroot.title("Do you want to save the file?")
        self.newroot.geometry("400x100")
        self.newroot.resizable(False, False)
        self.newroot.button = tk.Button(self.newroot, text="Yes", command=self.button1)
        self.newroot.button.pack()
        self.newroot.button = tk.Button(self.newroot, text="No", command=self.button2)
        self.newroot.button.pack()
    def button1(self):
        self.save_file()
        self.newroot.destroy()
    def button2(self):
        self.clear_text()
        self.newroot.destroy()
    def clear_text(self):
        self.filedirectory = ""
        self.text.delete("1.0", tk.END)
    def open_file(self, extension="txt"):
        file = tk.filedialog.askopenfile(parent=self.root, title="Select a file to open", filetypes=[("Text File", f"*.{extension}"), ("All files", "*.*")])
        if file:
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", file.read())
        self.filedirectory = file.name
    def outputprint(self, text):
        if (self.a == 1):
            self.outtext.config(state="normal")
            self.outtext.insert("end",text)
        else:
            print(text)
    def read_file(self, file=""):
        if self.a == 1:
            return self.text.get("1.0", tk.END)
        elif file == "" and self.a == 0:
            with open(self.filedirectory, "r") as file:
                return file.read()
        else:
            with open(file, "r") as file:
                return file.read()
    def save_file(self):
        if self.filedirectory == "":
            self.saveas_file()
        else:
            file = open(self.filedirectory, "w")
            file.write(self.text.get("1.0", tk.END))
            file.close()
    def saveas_file(self, extension="txt"):
        file = tk.filedialog.asksaveasfile(parent=self.root, title="Select a file to save", defaultextension=extension, filetypes=[("Text file", f"*.{extension}"), ("All files", "*.*")])
        if file:
            file.write(self.text.get("1.0", tk.END))
            file.close()
        self.filedirectory = file.name    
    def exit(self):
        self.root.destroy()

def testcasegenerator():
    path = os.path.realpath(__file__).split("\\")[:-1]
    path = "\\".join(path)
    path = f"{path}\\testcase.txt"
    with open(path, "w") as file:
        for i in code_instructions.operations_all[3]:
            if i in code_instructions.Instructions["R"] or i in code_instructions.Instructions["BONUS"]:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        for l in code_instructions.registers_list:
                            file.write(f"{i} {j},{k},{l}\n")
            else:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        file.write(f"{i} {j},{k},-3\n")
        for i in code_instructions.operations_all[2]:
            if i in code_instructions.Instructions["BONUS"]:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        file.write(f"{i} {j},{k}\n")
            elif i in ["lw","sw"]:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        file.write(f"{i} {j},-3({k})\n")
            else:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        file.write(f"{i} {j},-3\n")
        for i in code_instructions.operations_all[1]:
            for j in code_instructions.registers_list:
                file.write(f"{i} {j}\n")
        for i in code_instructions.operations_all[0]:
            file.write(f"{i}\n")
    file.close()
    print("testcase.txt created successfully!")
    print(f"at ::\t {path}")
def bonustestcases():
    path = os.path.realpath(__file__).split("\\")[:-1]
    path = "\\".join(path)
    path = f"{path}\\bonustestcase.txt"
    with open(path, "w") as file:
        for i in code_instructions.operations_all[3]:
            if i in i in code_instructions.Instructions["BONUS"]:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        for l in code_instructions.registers_list:
                            file.write(f"{i} {j},{k},{l}\n")
        for i in code_instructions.operations_all[2]:
            if i in code_instructions.Instructions["BONUS"]:
                for j in code_instructions.registers_list:
                    for k in code_instructions.registers_list:
                        file.write(f"{i} {j},{k}\n")
        for i in code_instructions.operations_all[0]:
            if i in code_instructions.Instructions["BONUS"]:
                file.write(f"{i}\n")
    file.close()
    print("bonustestcase.txt created successfully!")   
    print(f"at ::\t {path}")
   
if __name__ == "__main__":
    # usrinput = input("Enter the file directory::\t\t")    # in case we want to put the txt manually

    # if usrinput == "":
    #     asmbly = Assembler(a=1, textfiledir="")      # incase we want to have the GUI version
    # else:
    #     asmbly = Assembler(a=0, textfiledir=usrinput)
    # folderdirectory = os.path.realpath(__file__).split("\\")[:-1]
    # folderdirectory = "\\".join(folderdirectory)
    # asmbly = Assembler(a=1, textfiledir="",outputdir=folderdirectory+"bin.txt")           #incase we want to have the GUI version
    asmbly = Assembler(a=0, textfiledir=sys.argv[-2], outputdir=sys.argv[-1])
    if asmbly.a == 1:
        asmbly.root.mainloop()
    # testcasegenerator()
    # bonustestcases()
