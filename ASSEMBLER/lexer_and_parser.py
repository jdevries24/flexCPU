from AsmTools import *

def parseASM(text):
    text = stringTools.stripComments(text)
    lines = stringTools.split(text,'\n')
    asm_matrix = lines_to_matrix(lines)
    return lines,asm_matrix

def lines_to_matrix(lines):
    mat = []
    for line in lines:
        if line == "":
            mat.append([])
            continue
        row = []
        segs = stringTools.split(line,' ')
        row.append(segs[0])
        for seg in segs[1:]:
            row += split_seg(seg)
        mat.append(row)
    return mat

def split_seg(seg):
    segs = stringTools.split(seg,',')
    new_segs = []
    for s in segs:
        if (s == "") or ((s[0] != '"') and (s[-1] != '"')):
            new_segs.append(s)
        else:
            new_segs += stringTools.strToCharList(s[1:-1])
    return new_segs
        