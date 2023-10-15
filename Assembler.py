import sys
# code = sys.stdin.read().splitlines()

with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code
    code = f.read().splitlines()

listof_error = {
    "a": "Typos in instruction name or register name",
    "b": "Use of undefined variables",
    "c": "Use of undefined labels",
    "d": "Illegal use of FLAGS register",
    "e": "Illegal Immediate values",
    "f": "Misuse of labels as variables or vice-versa",
    "g": "Variables not declared at the beginning",
    "h": "Missing hlt instruction",
    "i": "hlt not being used as the last instruction",
    "j": "General Syntax Error"
}

register = {
    "R0": "00000", "R1": "00001", "R2": "00010", "R3": "00011", "R4": "00100", "R5": "00101", "R6": "00110", "R7": "00111", "R8": "01000","R9": "01001",
  "R10": "01010","R11": "01011", "R12": "01100","R13": "01101","R14": "01110", "R15": "01111", "R16": "10000","R17": "10001","R18": "10010","R19": "10011",
  "R20": "10100","R21": "10101","R22": "10110","R23": "10111","R24": "11000","R25": "11001","R26": "11010","R27": "11011",
  "R28": "11100","R29": "11101","R30": "11110","R31": "11111"
}

# registers = {
#     "R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110"
# }

operations = {
    "LUI": ['U', "0110111"],
    "AUIPC": ['U', "0010111"],
    # "JAL": ['UJ', "1101111"],
    # "JALR": ['I', "1100111"],
    "BEQ": ['SB', "1100011"],
    "BNE": ['SB', "1100011"],
    "BLT": ['SB', "1100011"],
    "BGE": ['SB', "1100011"],
    "BLTU": ['SB', "1100011"],
    "BGEU": ['SB', "1100011"],
    "LB": ['I', "0000011"],
    "LH": ['I', "0000011"],
    "LW": ['I', "0000011"],
    "LBU": ['I', "0000011"],
    "LHU": ['I', "0000011"],
    "SB": ['S', "0100011"],
    "SH": ['S', "0100011"],
    "SW": ['S', "0100011"],
    "ADDI": ['I', "0010011"],
    "SLTI": ['I', "0010011"],
    "SLTIU": ['I', "0010011"],
    "XORI": ['I', "0010011"],
    "ORI": ['I', "0010011"],
    "ANDI": ['I', "0010011"],
    "ADD": ['R', "0110011"],
    "SUB": ['R', "0110011"],
    "SLL": ['R', "0110011"],
    "SLT": ['R', "0110011"],
    "SLTU": ['R', "0110011"],
    "XOR": ['R', "0110011"],
    "SRL": ['R', "0110011"],
    "SRA": ['R', "0110011"],
    "OR": ['R', "0110011"],
    "AND": ['R', "0110011"]
  
}
func3={
    "BEQ":"000",
    "BNE":"001",
    "BLT":"100",
    "BGE":"101",
    "LB":"000",
    "LW":"010",
    "LBU":"100",
    "SB":"000",
    "SW":"010",
    "ADII":"000",
    "SLTI":"010",
    "ANDI":"111",
    "ADD":"000",
    "SUB":"000",
    "SLL":"001",
    "SLT":"010",
    "SLTU":"011",
    "XOR":"100",
    "SRL":"101",
    "SRA":"101",
    "AND":"111",
    "OR":"110"

}
func7={
     "ADD":"0000000",
    "SUB":"0100000",
    "SLL":"0000000",
    "SLT":"0000000",
    "SLTU":"0000000",
    "XOR":"0000000",
    "SRL":"0000000",
    "SRA":"0100000",
    "AND":"0000000",
    "OR": "0000000"
}

def decimaltobinary(n):
    n = int(n)
    binarycode = ""

    while n > 0:
        binarycode += str(n % 2)
        n = int(n/2)

    binarycode = binarycode[::-1]
    x = "0"*(8-len(binarycode))
    finalcode = x+binarycode
    return finalcode


def float_To_binary(my_number):
    places = 5
    my_number = float(my_number)
    whol, dec = str(my_number).split(".")
    dec = int (dec)
    whol = int(whol)
    res = bin(whol).lstrip("0b") + "."
    for _ in range(places):
            if (dec != 0):
                whol, dec = str((dec_converter(dec)) * 2).split(".")
                dec = int(dec)
                res += whol
            else:
                break

    ment = ""
    # print(res)
    a, b = res.split(".")
    c = a[1:]
    d = c+b
    e = len(c)

    if len(d) > 5:
        ment = d[:5]
    else:
        ment = d + "0"*(5-len(d))
    tt = e 
    if tt > 7:
        tt = 7
    g = bin(tt)[2:]
    # print(g)
    g = "0"*(3-len(g)) + g
    return (g + ment)


def dec_converter(num):
   while num > 1:
        num /= 10
   return num


def typeR(value, rs2, rs1, rd):
    machinecode = func7[value] + register[rs2] + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode

def typeI(value, imm, rs1, rd):
    machinecode = imm[11:0] + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode

def typeS(value, imm, rs2, rs1):
    machinecode = imm[11:5] + register[rs2] + register[rs1] + func3[value] + imm[4:0] + operations[value][1]
    return machinecode

def typeSB(value, imm, rs2, rs1):
    machinecode = imm[12] + imm[10:5] + register[rs2] + register[rs1] + func3[value] + imm[4:1] + imm[11] + operations[value][1]
    return machinecode

def typeU(value, imm, rd):
    machinecode = imm[31:12] + register[rd] + operations[value][1]
    return machinecode

def typeUJ(value, imm, rd):
    machinecode = imm[20] + imm[10:1] + imm[11] + imm[19:12] + register[rd] + operations[value][1]
    return machinecode

def typeB(value, r1, num):
    if value == "movf":
        x = float_To_binary(num)
    else:
        x = decimaltobinary(num)
        # print(x)
        # print(num)
    machinecode = operations[value][1]+register[r1]+x

    return machinecode


def typeC(value, r1, r2):
    machinecode = operations[value][1]+"00000"+register[r1]+register[r2]

    return machinecode


def typeD(value, r1, var):
    mem_address = decimaltobinary(variables[var])
    machinecode = operations[value][1]+register[r1]+mem_address

    return machinecode


def typeE(value, lbl):
    mem_address = decimaltobinary(labels[lbl + ":"])
    machinecode = operations[value][1] + "000" + mem_address

    return machinecode


def typeF(value):
    machinecode = operations[value][1] + "00000000000"

    return machinecode


# -------------------------------------------ALL ERRORS----------------------------------------------------------------------------

#typo in instruction, a
def typos(address, nameof_parameter, n):
    if(nameof_parameter not in operations.keys() and n == 1):
        print("Line number " + str(address) +
              " has an error of type: " + listof_error["a"])
        exit()
    elif(nameof_parameter not in register.keys() and n == 0):
        print("Line number " + str(address) +
              " has an error of type: " + listof_error["a"])
        exit()

# undefined use of variables, b


def undef_variable(address, nameof_var):
    print("Line number "+str(address) + " has an error of type: " +
          listof_error["b"] + " " + nameof_var)
    exit()

# undefined use of labels, c


def undef_label(address, nameof_var):
    print("Line number "+str(address) + " has an error of type: " +
          listof_error["c"] + " " + nameof_var)
    exit()

# illegal use of flags, d


def illegal_flags(address):
    print("Line number " + str(address) +
          " has an error of type: " + listof_error["d"])
    exit()

# illegal value (greater than 8 bits), e


def illegal_immvalue(address, immval):
    if(immval > 255 or immval < 0):
        print("Line number " + str(address) +
              " has an error of type: " + listof_error["e"])
        exit()

# label def as var ; var def as label, f


def label_var(address, name, n):
    if(name not in label) and n == 1:
        if(name in variable):
            print("Line number " + str(address) +
                  " has an error of type: " + listof_error["f"])
            exit()

    if(name not in variable) and n == 0:
        if(name in label):
            print("Line number " + str(address) +
                  " has an error of type: " + listof_error["f"])
            exit()

# variable not defined in the beginning, g


def notdefvariable_beg(address):
    print("Line number " + str(address) +
          " has an error of type: " + listof_error["g"])
    exit()

# halt missing, h


def miss_halt(address):
    print("Line number "+str(address) +
          " has an error of type: " + listof_error["h"])
    exit()

# last line not halt, i


def lastnot_hlt():
    print("Line number "+str(line_number) +
          " has an error of type: " + listof_error["i"])
    exit()

# General error, j


def generalError(address):
    print("Line number "+str(address) +
          " has an error of type: " + listof_error["j"])
    exit()

# Variable check


def errorVariables(flag, line):
    if flag:
        if line[1].isdigit():
            generalError(line_number)
        if len(line) == 2:
            if line[1] not in variable:
                variable.append(line[1])
            else:
                generalError(line_number)
        else:
            generalError(line_number)
    else:
        notdefvariable_beg(line_number)


variable = []
label = {}

var_flag = True
hlt_flag = True
assembly = {}
line_number = 0


# This 'for' loop mainly checks for all the error
# for line in code:

#     line_list = list(line.split())

#     if len(line_list) == 0:
#         continue

#     line_number += 1

#     if line_list[0] == "var":
#         errorVariables(var_flag, line_list)
#         continue
#     else:
#         var_flag = False

#     if hlt_flag == False:
#         lastnot_hlt()

#     if "FLAGS" in line_list:
#         if line_list[0] == "mov" and line_list[1] == "FLAGS" and line_list[2] in registers:
#             pass
#         else:
#             illegal_flags(line_number)
    
#     if line_list[0][-1] == ":":
#         label[line_list[0][0:-1]] = [True, line_number]
#         line_list.pop(0)

#     if line_list[0] == "mov":
#         if line_list[2][0] == "$":
#             line_list[0] = "mov1"
#         else:
#             line_list[0] = "mov2"

#     assembly[line_number] = line_list

#     if line_list[0] == "movf":
#         if line_list[1] in registers:
#             try:
#                 aa, bb = line_list[2][1:].split(".")
#                 continue
#             except:
#                 print("Immediate value is not of float type")
#                 exit()
#         else:
#             generalError(line_number)

#     if line_list[0] in operations.keys():

#         if operations[line_list[0]][0] == "A":
#             if len(line_list) == 4:
#                 for i in range(1, len(line_list)):
#                     typos(line_number, line_list[i], 0)
#             else:
#                 generalError(line_number)

#         elif operations[line_list[0]][0] == "B":
#             if len(line_list) == 3:
#                 typos(line_number, line_list[1], 0)
#                 if line_list[2][0] != "$":
#                     generalError(line_number)
#                 try:
#                     int(str(line_list[2])[1:])
#                 except:
#                     illegal_immvalue(line_number, 256)
#                 illegal_immvalue(line_number, int(str(line_list[2])[1:]))
#             else:
#                 generalError(line_number)

#         elif operations[line_list[0]][0] == "C":
#             if len(line_list) == 3:
#                 for i in range(1, len(line_list)):
#                     typos(line_number, line_list[i], 0)
#             else:
#                 generalError(line_number)

#         elif operations[line_list[0]][0] == "D":
#             if len(line_list) == 3:
#                 typos(line_number, line_list[1], 0)
#                 label_var(line_number, line_list[2], 0)

#                 if line_list[2] not in variable:
#                     undef_variable(line_number, line_list[2])
#             else:
#                 generalError(line_number)

#         elif operations[line_list[0]][0] == "E":
#             if len(line_list) == 2:
#                 label_var(line_number, line_list[1], 1)

#                 if line_list[1] not in label:
#                     label[line_list[1]] = [False, line_number]
#             else:
#                 generalError(line_number)

#         elif operations[line_list[0]][0] == "F":
#             if len(line_list) == 1:
#                 if hlt_flag == False:
#                     lastnot_hlt()
#                 hlt_flag = False
#             else:
#                 generalError(line_number)

#     else:
#         typos(line_number, line_list[0], 1)


# Check is there was hlt instruction at last
# if hlt_flag == True:
#     miss_halt(line_number)


# # Check for undefined variables
# for i in label:
#     if label[i][0] == False:
#         undef_label(label[i][1], i)


# -------------------------------------------PRINTING STARTS----------------------------------------------------------------------------

labels = {}
variables = {}


address = -1


for line in code:

    if len(line) == 0:
        continue

    line_list = list(line.split())

    if line_list[0] == "mov":
        if line_list[2][0] == "$":
            line_list[0] = "mov1"
        else:
            line_list[0] = "mov2"

    if (line_list[0] in operations and line_list[0] != "hlt"):
        address += 1

    elif (line_list[0] == "hlt"):
        address += 1
        labels[line_list[0]] = address

    elif (line_list[0][-1] == ":"):
        address += 1
        labels[line_list[0]] = address


for line in code:
    if (len(line) == 0):
        continue
    line_list = list(line.split())
    if line_list[0] == "var":
        address += 1
        variables[line_list[1]] = address


for line in code:

    if(len(line) == 0):
        continue

    line_list = list(line.split())

    if(len(line_list) > 1 and line_list[0] in labels):
        line_list.pop(0)

    if line_list[0] == "mov":
        if line_list[2][0] == "$":
            line_list[0] = "mov1"
        else:
            line_list[0] = "mov2"

    # if (len(line_list) > 1 and line_list[0] in labels and line_list[1] in operations):
    #     line_list.pop(0)

    # print(labels)

    # print(line_list)

    if line_list[0] in operations.keys():

        if operations[line_list[0]][0] == "A":

            print(typeR(line_list[0], line_list[1], line_list[2], line_list[3]))

        elif operations[line_list[0]][0] == "B":

            print(typeB(line_list[0], line_list[1], line_list[2][1:]))

        elif operations[line_list[0]][0] == "C":

            print(typeC(line_list[0], line_list[1], line_list[2]))

        elif operations[line_list[0]][0] == "D":

            print(typeD(line_list[0], line_list[1], line_list[2]))

        elif operations[line_list[0]][0] == "E":

            print(typeE(line_list[0], line_list[1]))

        elif operations[line_list[0]][0] == "F":

            print(typeF(line_list[0]))