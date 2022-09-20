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


def naive_algorithm(read, reference):
    matches = []
    if len(read) == 0 or len(reference) == 0:
        return(matches)
    for i in range(len(reference)- len(read) + 1):
        for j in range(len(read)):
            if not read[j] == reference[i + j]:
                break
        else:
            matches.append(i)
    return(matches)

#fasta_dict, fastq_dict = fasta_translator(args.genome), fastq_translator(args.reads)

def matches_to_SAM(read_file, reference_file):
    read_name = []
    reference_name = []
    match_index = []
    CIGARS = []
    match_string = []

    fasta_dict, fastq_dict = fasta_translator(reference_file), fastq_translator(read_file)

    for j in fastq_dict:
        for i in fasta_dict:
            matches_temp = naive_algorithm(fastq_dict[j], fasta_dict[i])
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

#print(fastq_dict)

#for i in range(len(SAM[0])):
#    read = SAM[4][i]
#    read_len = len(read)
#    reference = fasta_dict[SAM[1][i]][SAM[2][i]-1:SAM[2][i]-1+read_len]
#    assert read == reference

