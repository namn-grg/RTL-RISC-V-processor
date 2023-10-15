import sys
import re

# code = sys.stdin.read().splitlines()

with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code
    code = f.read().splitlines()

register = {
    "x0": "00000", "x1": "00001", "x2": "00010", "x3": "00011", "x4": "00100", "x5": "00101", "x6": "00110", "x7": "00111", "x8": "01000","x9": "01001",
  "x10": "01010","x11": "01011", "x12": "01100","x13": "01101","x14": "01110", "x15": "01111", "x16": "10000","x17": "10001","x18": "10010","x19": "10011",
  "x20": "10100","x21": "10101","x22": "10110","x23": "10111","x24": "11000","x25": "11001","x26": "11010","x27": "11011",
  "x28": "11100","x29": "11101","x30": "11110","x31": "11111"
}

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

def dec_to_binary(n):
    n = int(n)
    binarycode = ""

    while n > 0:
        binarycode += str(n % 2)
        n = int(n/2)

    binarycode = binarycode[::-1]
    x = "0"*(12-len(binarycode))
    finalcode = x+binarycode
    return finalcode

def hex_to_binary(hex_number):
    binary_length=12
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
    imm = dec_to_binary(imm)
    machinecode = imm[11:0] + register[rs1] + func3[value] + register[rd] + operations[value][1]
    return machinecode

def typeS(value, imm, rs2, rs1):
    imm = dec_to_binary(imm)
    machinecode = imm[11:5] + register[rs2] + register[rs1] + func3[value] + imm[4:0] + operations[value][1]
    return machinecode

def typeSB(value, imm, rs2, rs1):
    imm = dec_to_binary(imm)
    machinecode = imm[12] + imm[10:5] + register[rs2] + register[rs1] + func3[value] + imm[4:1] + imm[11] + operations[value][1]
    return machinecode

def typeU(value, imm, rd):
    imm = hex_to_binary(imm[2:])
    machinecode = imm[31:12] + register[rd] + operations[value][1]
    return machinecode

# Excluded for now
def typeUJ(value, imm, rd):
    machinecode = imm[20] + imm[10:1] + imm[11] + imm[19:12] + register[rd] + operations[value][1]
    return machinecode


# -------------------------------------------PRINTING STARTS----------------------------------------------------------------------------

for line in code:

    if len(line) == 0:
        continue

    line_list = custom_split(line)

for line in line_list:

    if line_list[0] in operations.keys():

        if operations[line_list[0]][0] == "R":
            print(typeR(line_list[0], line_list[3], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "I":
            print(typeI(line_list[0], line_list[3], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "S":
            print(typeS(line_list[0], line_list[2], line_list[1], line_list[3]))

        elif operations[line_list[0]][0] == "SB":
            print(typeSB(line_list[0], line_list[3], line_list[2], line_list[1])) 

        elif operations[line_list[0]][0] == "U":
            print(typeU(line_list[0], line_list[2], line_list[1]))

        elif operations[line_list[0]][0] == "UJ":
            print(typeUJ(line_list[0], line_list[2], line_list[1]))