
def checkBaudrateHelp(bd):
    bd_table = [110,1200,2400,9600,14400,19200,38400,57600,76800,115200,230400,460800]

    if(bd == "-h" or bd == "--help"):
        print("Parameter: <brudrate>")
        print("PL011 officially supported baudrates:")
        print("[1] 110\n\
[2] 1200\n\
[3] 2400\n\
[4] 9600\n\
[5] 14400\n\
[6] 19200\n\
[7] 38400\n\
[8] 57600\n\
[9] 76800\n\
[10] 115200\n\
[11] 230400\n\
[12] 460800")
        print("You may use the index instead of the true baudrate. You may also use other baudrates values without any warranty")
        return -1; 

    bd_int = int(bd)
    if(bd_int <= 12):
        return bd_table[bd_int-1]
    else:
        return bd_int
