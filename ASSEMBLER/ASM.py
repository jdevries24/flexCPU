from lexer_and_parser import parseASM
from Syntax_Checker import *
from assembler import *
from AsmTools import ASM_ERROR
from lookups import INS_SIZES,MEMORY_SIZES
from Output import *
INS_LIST = list(OPCODE_LOOKUP.keys())

class ASM:

    def __init__(self,lines,matrix):
        self.symbol_table = {}
        self.var_table = {}
        self.lines = lines
        self.matrix = matrix
        self.object_table = []
        self.outmatrix = []

    def replace_var(self,row):
        row2 = []
        for r in row:
            if r == "":
                row2.append("")
                continue
            if r[0] == "$":
                if r not in self.var_table.keys():
                    raise ASM_ERROR("","cannot find symbol " + r)
                row2.append(self.var_table[r])
                continue
            row2.append(r)
        return row2

    def ins_size(self,line,row):
        if row[0] in ("INC","DEC","ADCI","SBCI","ANDI","ORRI","XORI"):
            return ASSEMBLER.MATH_IM_SIZE(row)
        if row[0] in ("LDA","LDAH","LDAB","STR","STRH","STRB","LDASH","LDAB"):
            return ASSEMBLER.LOAD_STR_SIZE(row)
        return INS_SIZES[row[0]]

    def mem_size(self,line,row):
        if len(row) < 3:
            return 0
        if row[1] == "ZERO":
            return int(row[2])
        size = MEMORY_SIZES[row[1]]
        return size * (len(row) - 2)

    def first_pass(self):
        pc = 0
        for line,row in zip(self.lines,self.matrix):
            if (row == []) or (row[0] == ""):
                continue
            mem = row[0]
            if mem[0] == "$":
                self.var_table.update({mem:" ".join(row[1:])})
            elif (mem[0] == ".") or (mem[0] == "@"):
                if "$" in line:
                    row = self.replace_var(row)
                self.symbol_table.update({mem:pc})
                pc += self.mem_size(line,row)
            elif mem in INS_LIST:
                if "$" in line:
                    row = self.replace_var(row)
                SYNTAX_LOOKUP[mem](line,row)
                #print(line,self.ins_size(line,row))
                pc += self.ins_size(line,row)
            else:
                raise ASM_ERROR(line,"INS NOT FOUND")
    
    def secound_pass(self):
        pc = 0
        for line,row in zip(self.lines,self.matrix):
            if (row == []) or (row[0] == ""):
                continue
            mem = row[0]
            if mem[0] == "$":
                continue
            if "$" in line:
                row = self.replace_var(row)
            if mem[0] in (".","@"):
                binnary = ASSEMBLER.ADDRESS(pc,line,row,self.symbol_table,self.object_table)
                if len(binnary) > 0:
                    self.outmatrix.append([pc,binnary,line])
                    pc += len(binnary)
                else:
                    self.outmatrix.append([pc,[],line])
            else:
                binnary = ASSEMBLER_LOOKUP[row[0]](pc,line,row,self.symbol_table,self.object_table)
                self.outmatrix.append([pc,binnary,line])
                pc += len(binnary)
    
    def output_debug(self,file_name):
        with open(file_name,'w') as OUT:
            OUT.write("\n".join([ASMTools.output_debug(row) for row in self.outmatrix]))

    def output_exe(self,file_name):
        Output_system.write_exe(self.outmatrix,file_name)

    def output_logisim(self,file_name):
        Output_system.write_logisim(self.outmatrix,file_name)

    def output_object(self,file_name):
        addrs = []
        for k in self.symbol_table.keys():
            if k[0] == "@":
                addrs.append([self.symbol_table[k],k])
        Output_system.write_object(self.outmatrix,addrs,self.object_table,file_name)



with open("example.s") as IN:
    lines,mat = parseASM(IN.read())
    a = ASM(lines,mat)
    a.first_pass()
    a.secound_pass()
    a.output_debug("example.d")
    a.output_logisim("example.hex")