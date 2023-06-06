from lookups import register_lookup

register_keys = list(register_lookup.keys())

def ASM_E(line,message):
    return 'error at "' + line + '" ' + message
    
class SYNTAX_CHECKER:

    def MATH(line,ops):
        if len(ops) < 3:
            return ASM_E(line,"Not enough oprands")
        if len(ops) > 3:
            return ASM_E(line,"to much oprands")
        if ops[1] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")
        if ops[2] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")

    def SRC_REG(line,ops):
        if len(ops) < 2:
            return ASM_E(line,"Needs oprand")
        if len(ops) > 2:
            return ASM_E(line,"To Much oprands")
        if ops[1] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")
        
    def TWO_REG_IM(line,ops):
        if len(ops) < 4:
            return ASM_E(line,"Not enough oprands")
        if len(ops) > 4:
            return ASM_E(line,"to much oprands")
        if ops[1] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")
        if ops[2] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")

    def ONE_REG_IM(line,ops):
        if len(ops) < 3:
            return ASM_E(line,"Not enough oprands")
        if len(ops) > 3:
            return ASM_E(line,"to much oprands")
        if ops[1] not in register_keys:
            return ASM_E(line,ops[1] + " is not a register")

    def ONE_IM(line,ops):
        if len(ops) < 2:
            return ASM_E(line,"Needs oprand")
        if len(ops) > 2:
            return ASM_E(line,"To Much oprands")

    def LEA(line,ops):
        return SYNTAX_CHECKER.ONE_REG_IM(line,ops)

    def MATH_IM(line,ops):
        return SYNTAX_CHECKER.TWO_REG_IM(line,ops)

    def LOAD_STORE(line,ops):
        if len(ops) < 4:
            ops.append('0')
        return SYNTAX_CHECKER.TWO_REG_IM(line,ops)

    def NO_VAR(line,ops):
        if len(ops) > 1:
            return ASM_E(line,"Instruction takes no oprands")

    def BRANCH(line,ops):
        return SYNTAX_CHECKER.ONE_IM(line,ops)

    def SRC_INS(line,ops):
        return SYNTAX_CHECKER.ONE_REG_IM(line,ops)


SYNTAX_LOOKUP = {
"NOP":SYNTAX_CHECKER.NO_VAR,
"STRB":SYNTAX_CHECKER.LOAD_STORE,
"STRH":SYNTAX_CHECKER.LOAD_STORE,
"LDAB":SYNTAX_CHECKER.LOAD_STORE,
"LDAH":SYNTAX_CHECKER.LOAD_STORE,
"LDAZXB":SYNTAX_CHECKER.LOAD_STORE,
"LDAZXH":SYNTAX_CHECKER.LOAD_STORE,
"ADD":SYNTAX_CHECKER.MATH,
"ADC":SYNTAX_CHECKER.MATH,
"SUB":SYNTAX_CHECKER.MATH,
"SBC":SYNTAX_CHECKER.MATH,
"AND":SYNTAX_CHECKER.MATH,
"ORR":SYNTAX_CHECKER.MATH,
"XOR":SYNTAX_CHECKER.MATH,
"NEG":SYNTAX_CHECKER.MATH,
"INC":SYNTAX_CHECKER.MATH_IM,
"ADCI":SYNTAX_CHECKER.MATH_IM,
"DEC":SYNTAX_CHECKER.MATH_IM,
"SBC":SYNTAX_CHECKER.MATH_IM,
"ANDI":SYNTAX_CHECKER.MATH_IM,
"ORRI":SYNTAX_CHECKER.MATH_IM,
"CMP":SYNTAX_CHECKER.MATH,
"SCMP":SYNTAX_CHECKER.MATH,
"BZF":SYNTAX_CHECKER.BRANCH,
"BCF":SYNTAX_CHECKER.BRANCH,
"BLT":SYNTAX_CHECKER.BRANCH,
"BEQ":SYNTAX_CHECKER.BRANCH,
"BGT":SYNTAX_CHECKER.BRANCH,
"BNE":SYNTAX_CHECKER.BRANCH,
"BRC":SYNTAX_CHECKER.BRANCH,
"BRI":SYNTAX_CHECKER.BRANCH,
"BRA":SYNTAX_CHECKER.SRC_INS,
"CAL":SYNTAX_CHECKER.BRANCH,
"CAA":SYNTAX_CHECKER.SRC_INS,
"RET":SYNTAX_CHECKER.NO_VAR,
"IRQ":SYNTAX_CHECKER.NO_VAR,
"NMI":SYNTAX_CHECKER.NO_VAR,
"RIN":SYNTAX_CHECKER.NO_VAR,
"LEA":SYNTAX_CHECKER.LEA,
"HCF":SYNTAX_CHECKER.NO_VAR}

