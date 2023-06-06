from lookups import OPCODE_LOOKUP,MEMORY_SIZES,register_lookup
from AsmTools import *



def hex_line(line_no,binnary,IM = None):
    line = "l" + ASMTools.intToHexStr(line_no,6) + "\no" + ASMTools.ilist_to_blist(binnary)
    if IM != None:
        line += "," + str(IM)
    return line


class ASSEMBLER:

    def NO_VAR(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        return [opcode]

    def SRC_INS(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        src = register_lookup[ops[1]] << 4
        return [opcode,src]


    def MATH(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        src = register_lookup[ops[1]] << 4
        dest = register_lookup[ops[2]]
        sd = src | dest
        return [opcode,sd]

    def LOAD_STORE(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        if len(ops) < 4: ops.append('0')
        src = register_lookup[ops[1]] << 4
        dest = register_lookup[ops[2]]
        sd = src | dest
        value = ASMTools.strToInt(ops[3])
        if value == 0:
            return [opcode,sd]
        else:
            if abs(value) >= 0xc000:
                raise ASM_ERROR(line,"fetch oprand out of range")
            if abs(value) >= 0xc0:
                return [opcode,sd + 8] + ASMTools.i16_to_bytes(ASMTools.i16_to_s16(value))
            else:
                return [opcode + 4,sd,ASMTools.i8_to_s8(value) & 0xff]

    def MATH_IM(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        src = register_lookup[ops[1]] << 4
        dest = register_lookup[ops[2]]
        sd = src | dest
        if ASMTools.is_number(ops[3]):
            value = ASMTools.strToInt(ops[3])
            if (value < 0) or (value >= 0x10000):
                raise ASM_ERROR(line," value offset is out of bounds")
            if value >= 0x100:
                return [opcode + 0x10,sd] + ASMTools.i16_to_bytes(value)
            else:
                return [opcode,sd,value & 0xff]
        raise ASM_ERROR(line,"Non valid inc size")

    def BRANCH(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        if ASMTools.is_number(ops[1]):
            value = ASMTools.strToInt(ops[1])
            if abs(value) > 0xc000:
                raise ASM_ERROR(line," value offset is out of bounds")
            value = ASMTools.i24_to_s24(value)
            return [opcode] + ASMTools.i16_to_bytes(value)
        else:
            return [opcode] + ASSEMBLER.i16_branch(pc,line,ops[1],st,object_table)

    def LEA(pc,line,ops,st,object_table):
        opcode = OPCODE_LOOKUP[ops[0]]
        dest = register_lookup[ops[1]]
        if ASMTools.is_number(ops[2]):
            value = ASMTools.strToInt(ops[2])
            if abs(value) > 0xc000:
                raise ASM_ERROR(line," value offset is out of bounds")
            value = ASMTools.i16_to_s16(value)
            return [opcode,dest] + ASMTools.i16_to_bytes(value)
        else:
            return [opcode,dest] + ASSEMBLER.i16_branch(pc,line,ops[2],st,object_table)

    def i16_branch(pc,line,addr,st,object_table):
        offset = 0
        if addr[0] == ".":
            if addr not in st.keys():
                raise ASM_ERROR(line," local addr not found")
            offset = st[addr] - pc
        elif addr[0] == "@":
            if addr not in st.keys():
                object_table.append([pc,2,16,addr])
            else:
                offset = st[addr] - pc
        if abs(offset) >= 0xc000:
            raise ASM_ERROR(line," addr out of bounds")
        offset = ASMTools.i16_to_s16(offset)
        return ASMTools.i16_to_bytes(offset)

    def ADDRESS(pc,line,ops,st,object_table):
        if len(ops) < 2:
            return []
        if ops[1] == "ZERO":
            size = ASMTools.strToInt(ops[2])
            return [0 for i in range(size)]
        size = MEMORY_SIZES[ops[1]]
        bytes = []
        for v in ops[2:]:
            value = 0
            if (len(v) >= 3) and (v[0] == "'") and (v[-1] == "'"):
                value = ASMTools.charToInt(v[1:-1])
            else:
                value = ASMTools.strToInt(v)
            if size == 4:
                bytes += ASMTools.i32_to_bytes(value)
            elif size == 2:
                bytes += ASMTools.i16_to_bytes(value)
            else:
                bytes.append(value & 0xff)
        return bytes

    def LOAD_STR_SIZE(ops):
        if len(ops) <= 3:
            return 2
        else:
            if ASMTools.strToInt(ops[3]) == 0:
                return 2
            return 3
            

    def MATH_IM_SIZE(ops):
        offset = ASMTools.strToInt(ops[3])
        if offset >= 0x100:
            return 4
        else:
            return 3


ASSEMBLER_LOOKUP = {
"NOP":ASSEMBLER.NO_VAR,
"STRB":ASSEMBLER.LOAD_STORE,
"STRH":ASSEMBLER.LOAD_STORE,
"LDAB":ASSEMBLER.LOAD_STORE,
"LDAH":ASSEMBLER.LOAD_STORE,
"LDAZXB":ASSEMBLER.LOAD_STORE,
"LDAZXH":ASSEMBLER.LOAD_STORE,
"ADD":ASSEMBLER.MATH,
"ADC":ASSEMBLER.MATH,
"SUB":ASSEMBLER.MATH,
"SBC":ASSEMBLER.MATH,
"AND":ASSEMBLER.MATH,
"ORR":ASSEMBLER.MATH,
"XOR":ASSEMBLER.MATH,
"NEG":ASSEMBLER.MATH,
"INC":ASSEMBLER.MATH_IM,
"ADCI":ASSEMBLER.MATH_IM,
"DEC":ASSEMBLER.MATH_IM,
"SBC":ASSEMBLER.MATH_IM,
"ANDI":ASSEMBLER.MATH_IM,
"ORRI":ASSEMBLER.MATH_IM,
"CMP":ASSEMBLER.MATH,
"SCMP":ASSEMBLER.MATH,
"BZF":ASSEMBLER.BRANCH,
"BCF":ASSEMBLER.BRANCH,
"BLT":ASSEMBLER.BRANCH,
"BEQ":ASSEMBLER.BRANCH,
"BGT":ASSEMBLER.BRANCH,
"BNE":ASSEMBLER.BRANCH,
"BRC":ASSEMBLER.BRANCH,
"BRI":ASSEMBLER.BRANCH,
"BRA":ASSEMBLER.SRC_INS,
"CAL":ASSEMBLER.BRANCH,
"CAA":ASSEMBLER.SRC_INS,
"RET":ASSEMBLER.NO_VAR,
"IRQ":ASSEMBLER.NO_VAR,
"NMI":ASSEMBLER.NO_VAR,
"RIN":ASSEMBLER.NO_VAR,
"LEA":ASSEMBLER.LEA,
"HCF":ASSEMBLER.NO_VAR}