import sys
import re

# code = sys.stdin.read().splitlines()

with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code
    code = f.read().splitlines()

# with open('exp_output.txt') as f:  # here output.txt is an output file with machine code
#     exp_output = f.read().splitlines()

register = {
    "x0": "00000", "x1": "00001", "x2": "00010", "x3": "00011", "x4": "00100", "x5": "00101", "x6": "00110", "x7": "00111", "x8": "01000","x9": "01001",
  "x10": "01010","x11": "01011", "x12": "01100","x13": "01101","x14": "01110", "x15": "01111", "x16": "10000","x17": "10001","x18": "10010","x19": "10011",
  "x20": "10100","x21": "10101","x22": "10110","x23": "10111","x24": "11000","x25": "11001","x26": "11010","x27": "11011",
  "x28": "11100","x29": "11101","x30": "11110","x31": "11111"
}


operations = {
    "lui": ['u', "0110111"],
    "auipc": ['u', "0010111"],
    # "jal": ['uj', "1101111"],
    # "jalr": ['i', "1100111"],
    "beq": ['sb', "1100011"],
    "bne": ['sb', "1100011"],
    "blt": ['sb', "1100011"],
    "bge": ['sb', "1100011"],
    "bltu": ['sb', "1100011"],
    "bgeu": ['sb', "1100011"],
    "lb": ['i', "0000011"],
    "lh": ['i', "0000011"],
    "lw": ['i', "0000011"],
    "lbu": ['i', "0000011"],
    "lhu": ['i', "0000011"],
    "sb": ['s', "0100011"],
    "sh": ['s', "0100011"],
    "sw": ['s', "0100011"],
    "addi": ['i', "0010011"],
    "slti": ['i', "0010011"],
    "sltiu": ['i', "0010011"],
    "xori": ['i', "0010011"],
    "ori": ['i', "0010011"],
    "andi": ['i', "0010011"],
    "add": ['r', "0110011"],
    "sub": ['r', "0110011"],
    "sll": ['r', "0110011"],
    "slt": ['r', "0110011"],
    "sltu": ['r', "0110011"],
    "xor": ['r', "0110011"],
    "srl": ['r', "0110011"],
    "sra": ['r', "0110011"],
    "or": ['r', "0110011"],
    "and": ['r', "0110011"],
    "loadnoc": ['s', "0110011"],
    "storenoc": ['i', "0000011"]
}

func3={
    "beq":"000",
    "bne":"001",
    "blt":"100",
    "bge":"101",
    "lb":"000",
    "lw":"010",
    "lbu":"100",
    "sb":"000",
    "sw":"010",
    "addi":"000",
    "slti":"010",
    "andi":"111",
    "add":"000",
    "sub":"000",
    "sll":"001",
    "slt":"010",
    "sltu":"011",
    "xor":"100",
    "srl":"101",
    "sra":"101",
    "and":"111",
    "or":"110",
    "loadnoc":"010",
    "storenoc":"010"
}

func7={
    "add":"0000000",
    "sub":"0100000",
    "sll":"0000000",
    "slt":"0000000",
    "sltu":"0000000",
    "xor":"0000000",
    "srl":"0000000",
    "sra":"0100000",
    "and":"0000000",
    "or": "0000000"
}

def dec_to_binary(n, length):
    n = int(n)
    binarycode = ""

    while n > 0:
        binarycode += str(n % 2)
        n = int(n/2)

    binarycode = binarycode[::-1]
    x = "0"*(length-len(binarycode))
    finalcode = x+binarycode
    return finalcode

def hex_to_binary(hex_number):
    binary_length=32
    try:
        # Convert the hexadecimal number to binary
        binary = bin(int(hex_number, 16))[2:]

        # Ensure the binary representation has the desired length
        if len(binary) < binary_length:
            binary = '0' * (binary_length - len(binary)) + binary
        elif len(binary) > binary_length:
            raise ValueError("Binary representation exceeds the desired length")

        return binary
    except ValueError:
        return "Invalid input"

def custom_split(input_string):
    delimiters = (' ', ',', '(', ')')
    # Create a regular expression pattern to match any of the delimiters
    pattern = '|'.join(map(re.escape, delimiters))
    # Use re.split() to split the input string based on the delimiters
    split_string = re.split(pattern, input_string)
    # Remove empty strings from the list
    split_string = [item for item in split_string if item]
    return split_string

def typeR(value, rs2, rs1, rd):
    machinecode = func7[value] + register[rs2] + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode

def typeI(value, imm, rs1, rd):
    imm = dec_to_binary(imm, 12)
    machinecode = imm + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode

def typeS(value, imm, rs2, rs1):
    imm = dec_to_binary(imm, 12)
    machinecode = imm[0:7] + register[rs2] + register[rs1] + func3[value] + imm[7:11] + imm[11] + operations[value][1]
    return machinecode

def typeSB(value, imm, rs2, rs1):
    imm = dec_to_binary(imm, 13)
    machinecode = imm[12] + imm[10:4:-1] + register[rs2] + register[rs1] + func3[value] + imm[4:0:-1] + imm[11] + operations[value][1]
    return machinecode

def typeU(value, imm, rd):
    imm = hex_to_binary(imm[2:])
    machinecode = imm[31:11:-1] + register[rd] + operations[value][1]
    return machinecode

# Excluded for now
def typeUJ(value, imm, rd):
    machinecode = imm[20] + imm[10:1] + imm[11] + imm[19:12] + register[rd] + operations[value][1]
    return machinecode

def typeLOADNOC(value,imm,rs1,rs2):
    imm = dec_to_binary(imm, 12)
    machinecode = imm[0:7] + register[rs2] + register[rs1] + func3[value] + imm[7:11] + imm[11] + operations[value][1]
    return machinecode


def typeSTORENOC(value,imm,rs1,rd):
    imm = dec_to_binary(imm, 12)
    machinecode = imm + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode


# -------------------------------------------PRINTING STARTS----------------------------------------------------------------------------

i = 0
line_list_arr = []
output = []

for line in code:
    temp_list = custom_split(line)

    if temp_list[0] == "lw" or temp_list[0]=="storenoc" :
        temp = temp_list[3]
        temp_list[3] = temp_list[2]
        temp_list[2] = temp

    line_list_arr.append(temp_list)
    # print(temp_list)
    

# print(line_list_arr)


for line_list in line_list_arr:
    # print(line_list)
    if line_list[0] in operations.keys():

        if operations[line_list[0]][0] == "r":
            output.append(typeR(line_list[0], line_list[3], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "i":
            output.append(typeI(line_list[0], line_list[3], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "s":
            output.append(typeS(line_list[0], line_list[2], line_list[1], line_list[3]))

        elif operations[line_list[0]][0] == "sb":
            output.append(typeSB(line_list[0], line_list[3], line_list[2], line_list[1])) 

        elif operations[line_list[0]][0] == "u":
            output.append(typeU(line_list[0], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "uj":
            output.append(typeUJ(line_list[0], line_list[2], line_list[1]))
    
    else:
        output.append("Invalid Instruction")

    
for i in output:
    print(i)

# -------------------------------------------PRINTING ENDS----------------------------------------------------------------------------

# -------------------------------------------WRITING STARTS----------------------------------------------------------------------------

# Function to convert 32-bit binary to 8-bit hexadecimal
def binary32_to_8bit_hex(binary_string):
    # Make sure the binary string is 32 bits long
    if len(binary_string) != 32:
        raise ValueError("Input must be a 32-bit binary number.")

    # Split the 32-bit binary into four 8-bit segments
    segments = [binary_string[i:i + 8] for i in range(0, 32, 8)]

    # Convert each 8-bit segment to hexadecimal
    hex_values = [format(int(segment, 2), '02X') for segment in segments]

    # Concatenate the 8-bit hexadecimal segments
    hex_result = ''.join(hex_values)

    return hex_result

with open("output.hex", "w") as file:
    # Convert and write the 8-bit hexadecimal values to the file
    for binary_string in output:
        hex_value = binary32_to_8bit_hex(binary_string)
        file.write(hex_value + "\n")

# -------------------------------------------TESTING STARTS----------------------------------------------------------------------------

# for i in range(len(output)):
#     if output[i] == exp_output[i]:
#         print("Test case passed on line ", i)
#     else:
#         print("Test case failed on line ", i)
#         print("Input:           ", code[i])
#         print("Actual output:   ", output[i])
#         print("Expected output: ", exp_output[i])

# -------------------------------------------TESTING ENDS----------------------------------------------------------------------------