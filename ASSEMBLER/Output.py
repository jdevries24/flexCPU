class Output_system:

    def i32_to_bytes(i32):
        return [(i32 >> 24) & 255,(i32 >> 16) & 255,(i32 >> 8) & 255,i32 & 255]


    def str_to_bytes(string):
        return [ord(char) for char in string]
    
    def output_addr(pos,name):
        return Output_system.i32_to_bytes(pos) + [len(name) & 255] + Output_system.str_to_bytes(name)
    
    def output_pos_ref(pc,offset_from_pc,size,name):
        pc = Output_system.i32_to_bytes(pc)
        offset_from_pc = offset_from_pc & 255
        size = size & 255
        return pc + [offset_from_pc,size,len(name) & 255] + Output_system.str_to_bytes(name)

    def output_addrs(addrs):
        acm = []
        for addr in addrs:
            acm += Output_system.output_addr(addr[0],addr[1])
        return Output_system.i32_to_bytes(len(acm)) + acm

    def output_pos_refs(offsets):
        acm = []
        for off in offsets:
            acm += Output_system.output_pos_ref(off[0],off[1],off[2],off[3])
        return Output_system.i32_to_bytes(len(acm)) + acm

    def output_header(addrs,offsets):
        acm = Output_system.output_addrs(addrs) + Output_system.output_pos_refs(offsets)
        return Output_system.i32_to_bytes(len(acm)) + acm

    def output_machine_code(outmatrix):
        acm = []
        for row in outmatrix:
            acm += row[1]
        return acm

    def write_exe(outmatrix,file_name):
        binary = Output_system.output_machine_code(outmatrix)
        Output_system.write_binary(binary,file_name)

    def write_object(outmatrix,addr,offsets,output_file):
        binary = Output_system.output_machine_code(outmatrix)
        header = Output_system.output_header(addr,offsets)
        print(header)
        Output_system.write_binary(header + Output_system.i32_to_bytes(len(binary)) + binary,output_file)

    def write_binary(num_matrix,output_file_name):
        with open(output_file_name,"wb") as OUT:
            print(bytes(num_matrix))
            OUT.write(bytes(num_matrix))

    def write_logisim(outmatrix,file_name):
        binary = Output_system.output_machine_code(outmatrix)
        hexes = []
        for i,num in enumerate(binary):
            if (i % 8) == 0:
                hexes.append('\n')
            hexstr = hex(num)[2:]
            if len(hexstr) != 2:
                hexstr = "0" + hexstr
            hexes.append(hexstr)
        with open(file_name,'w') as OUT:
            OUT.write("v2.0 raw"+" ".join(hexes))


