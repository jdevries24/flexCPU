from NANO_INS import *
def int_to_hex(i,size = 2):
    h = hex(i)[2:]
    for i in range(size - len(h)):
        h = "0" + h
    return h

class NA:

    def __init__(self,lines):
        self.nc = 0
        self.op_locs = [0 for i in range(260)]
        self.nano_code = []
        self.lines = lines

    def run(self,nc_fname,loc_fname):
        for I,line in enumerate(self.lines):
            #print(I)
            self.read_line(line)
        self.out_logisim(nc_fname,self.nano_code,8)
        self.out_logisim(loc_fname,self.op_locs,2)

    def add_locs(self,line):
        line = line[1:]
        for hexes in line.split(','):
            self.op_locs[int(hexes,16)] = self.nc

    def read_ins(self,line):
        value = 0
        for ins in line.split(','):
            num,pos = NANO_INS[ins]
            value |= (num << pos)
        self.nano_code.append(value)

    def read_line(self,line):
        if (line == "") or line[0] == '#':
            return
        if (line[0] == "@"):
            self.add_locs(line)
        else:
            self.read_ins(line)
            self.nc += 1

    def out_logisim(self,fname,arr,num_size):
        base = "v2.0 raw"
        hexes = []
        for i,num in enumerate(arr):
            if (i % 8) == 0:
                hexes.append('\n')
            hexes.append(int_to_hex(num,num_size))
        with open(fname,'w') as OUT:
            OUT.write(base + " ".join(hexes))
            print(base + " ".join(hexes))

with open("NC") as IN:
    n = NA(IN.read().split('\n'))
    n.run("nano_code.hex","loc_code.hex")
        
