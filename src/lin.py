import argparse
import sys

argparser = argparse.ArgumentParser(
    description="Exact matching using the naive method")
argparser.add_argument("genome", type=argparse.FileType('r'))
argparser.add_argument("reads", type=argparse.FileType('r'))
args = argparser.parse_args()

def fasta_translator(file):
    output_dict = {}
    start = True
    for i in file:
        if i[0] == ">":
            if  not start:
                output_dict[name] = seq
            name = i[1:].strip()
            seq = ""
            if start:
                start = False
        else:
            seq += i.strip()
    output_dict[name] = seq
    return output_dict

def fastq_translator(file):
    output_dict = {}
    for i in file:
        if i[0] == "@":
            name = i[1:].strip()
        else:
            seq = i.strip()
            output_dict[name] = seq
    return(output_dict)

def border_array_algorithm(read):
    border_array = [0]
    for i in range(1, len(read)):
        b = border_array[i - 1]
        while True:
            if read[b] == read[i]:
                border_array.append(b + 1)
                break
            elif b == 0:
                border_array.append(0)
                break
            else:
                b = border_array[b-1]
    return(border_array)

def border_array_search(read, reference, read_border_array):
    read_len = len(read)
    if read_len == 0 or len(reference) == 0:
        return([])
    read = read + "0"
    previous_border = 0
    matches = []
    for i in range(len(reference)):
        while True:
            if read[previous_border] == reference[i]:
                previous_border += 1
                break
            elif previous_border == 0:
                break
            else:
                previous_border = read_border_array[previous_border - 1]
        if previous_border == read_len:
            matches.append(i - len(read) + 2)
    return(matches)

def matches_to_SAM(read_file, reference_file):
    read_name = []
    reference_name = []
    match_index = []
    CIGARS = []
    match_string = []

    fasta_dict, fastq_dict = fasta_translator(reference_file), fastq_translator(read_file)

    for j in fastq_dict:
        read_array = border_array_algorithm(fastq_dict[j])
        for i in fasta_dict:
            matches_temp = border_array_search(fastq_dict[j], fasta_dict[i], read_array)
            if matches_temp:
                for match in matches_temp: # Each iteration makes a SAM row
                    read_name.append(j)
                    reference_name.append(i)
                    match_index.append(match + 1)
                    CIGARS.append(str(len(fastq_dict[j])) + "M")
                    match_string.append(fastq_dict[j])
    output = (read_name, reference_name, match_index, CIGARS, match_string)
    return output

def print_SAM(SAM):
    for i in range(len(SAM[0])):
        sys.stdout.write(SAM[0][i] + "\t" + SAM[1][i] + "\t" + str(SAM[2][i]) + "\t" + SAM[3][i] + "\t" + SAM[4][i] + "\n")

SAM = matches_to_SAM(args.reads, args.genome)

print_SAM(SAM)