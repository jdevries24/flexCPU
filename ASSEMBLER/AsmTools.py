class ASM_ERROR(Exception):

    def __init__(self,line,mess):
        self.message = "".join(["ERROR AT(",str(line),") ",str(mess)])

class CharQueu:

    def __init__(self,str):
        self.list = list(str)
        self.i = 0

    def peek(self):
        if self.i == len(self.list):
            return ""
        return self.list[self.i]

    def __len__(self):
        return len(self.list) - self.i

    def dequeu(self):
        letter = self.list[self.i]
        self.i += 1
        return letter

class stringTools:

    def readStr(Q):
        acm = []
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == '"':
                acm.append(nextChar)
                return acm
            if nextChar == '\\':
                if(len(Q) != 0):
                    acm.append(nextChar)
                    acm.append(Q.dequeu())
                else:
                    return
            else:
                acm.append(nextChar)
        return ["ERROR"]

    def runSingleLineComment(Q):
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == "\n":
                return "\n"
        return ""

    def RunMultiLine(Q):
        acm = []
        ask = False
        while(len(Q) > 1):
            nextChar = Q.dequeu()
            if nextChar == '\n':
                acm.append('\n')
            if (nextChar == "/") and ask:
                return acm
            if (nextChar == "*"):
                ask = True
            else:
                ask = False
        return acm

    def split(string,dell):
        Q = CharQueu(string)
        acm = []
        subacm = []
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == '"':
                subacm.append('"')
                subacm += stringTools.readStr(Q)
            elif nextChar == dell:
                acm.append("".join(subacm))
                subacm = []
            else:
                subacm.append(nextChar)
        if subacm != []:
            acm.append("".join(subacm))
        return acm

    def stripComments(string):
        Q = CharQueu(string)
        acm = []
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == '"':
                acm.append('"')
                acm += stringTools.readStr(Q)
            else:
                peek = nextChar + Q.peek()
                if peek == "//":
                    Q.dequeu()
                    acm.append(stringTools.runSingleLineComment(Q))
                elif peek == "/*":
                    Q.dequeu()
                    acm += stringTools.RunMultiLine(Q)
                else:
                    acm.append(nextChar)
        return acm

    def strToCharList(string):
        Q = CharQueu(string)
        acm = []
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == "\\":
                if len(Q) > 0:
                    acm.append("'" + nextChar + Q.dequeu() + "'")
            else:
                acm.append("'" + nextChar + "'")
        return acm

    def upper(string):
        Q = CharQueu(string)
        acm = []
        while(len(Q) > 0):
            nextChar = Q.dequeu()
            if nextChar == '"':
                acm.append(nextChar)
                acm += stringTools.readStr(Q)
            else:
                acm.append(nextChar.upper())
        return "".join(acm)

class ASMTools:

    def output_debug(row):
        pc = row[0]
        value = row[1]
        line = row[2]
        if len(value) == 0:
            return "             "+line
        if line[0] in("@","."):
            return ASMTools.intToHexStr(pc,6) + "       " + line
        if len(value) == 1:
            return ASMTools.intToHexStr(pc,6) + " " + ASMTools.intToHexStr(value[0],2) + "    " + line
        base = ASMTools.intToHexStr(pc,6) + " " + ASMTools.intToHexStr(value[0],2) + " " + ASMTools.intToHexStr(value[1],2) + " " + line
        for i,v in enumerate(value[2:]):
            if (i % 2) == 0:
                base += "\n      " 
            base +=  " " + ASMTools.intToHexStr(v,2)
        return base


    def intToHexStr(number,hexStrMinLen):
        hexBase = hex(number)[2:]
        hexBase = "".join(["0" for i in range(hexStrMinLen - len(hexBase))]) + hexBase
        return hexBase.upper()

    def charToInt(char):
        if len(char) == 1:
            return ord(char)
        elif len(char) > 1:
            conCharLookup = {"0":0,
            "b":8,"t":9,"n":0xA,"v":0xB,"f":0xC,"r":0xD}
            if char[0] == "\\":
                if char[1] in conCharLookup.keys():
                    return conCharLookup[char[1]]
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    def ilist_to_blist(lst):
        return ','.join([ASMTools.intToHexStr(i,2) for i in lst])

    def strToInt(str):
        str = str.upper()
        is_negative = False
        if str[0] == '-':
            str = str[1:]
            is_negative = True
        value = 0
        if (len(str) >= 3) and (str[0] == "'") and (str[-1] == "'"):
            return ASMTools.charToInt(str[1:-1])
        if (len(str) < 3) or (str[:2] not in ('0B','0X')):
            value = int(str)
        else:
            if str[:2] == '0B':
                value = int(str,2)
            elif str[:2] == '0X':
                value = int(str,16)
        if is_negative:
            return value * -1
        return value


    def i24_to_s24(number):
        value = 0
        if(number < 0):
            number = number * -1
            return number | 0x800000
        else:
            return number

    def i16_to_s16(number):
        if(number < 0):
            number = number * -1
            return number | 0x8000
        else:
            return number

    def i8_to_s8(number):
        if(number < 0):
            number = number * -1
            return number | 0x80
        else:
            return number

    def i32_to_bytes(number):
        return [(number >> 24) & 0xff,(number >> 16) & 0xff,(number >> 8) & 0xff,number & 0xff]

    def i24_to_bytes(number):
        return [(number >> 16) & 0xff,(number >> 8) & 0xff,number & 0xff ]
    
    def i16_to_bytes(number):
        return [(number >> 8) & 0xff,number & 0xff]

    def i8_to_bytes(number):
        return [number & 0xff]

    def is_number(op):
        if op[0] in ("@",".","$","~"):
            return False
        return ASMTools.is_valid_oprand(op)

    def is_valid_oprand(op):
        if (len(op) == 0) or op == "-":
            return False
        if op[0] in ("@",".","$"):
            return True
        if op[0] == '-':
            op = op[1:]
        op = op.upper()
        if len(op) < 3:
            return op.isdigit()
        elif len(op) > 4:
            if op.isdigit():
                return True
            if op[:2] == "0X":
                hexchars = "0123456789ABCDEF"
                for letter in op[2:]:
                    if letter not in hexchars:
                        return False
                return True
            if op[:2] == "0B":
                for letter in op[2:]:
                    if not ((letter == "0") or (letter == "1")):
                        return False
                    return True
            return False


if __name__ == "__main__":
    print(ASMTools.strToInt("0b100"))