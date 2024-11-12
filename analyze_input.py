import math
from itertools import combinations
from math import log2
import fileManager as fm

'''
analyze_input - Final Version

The input is json file while the keys are the symbols (X1 , X2 .....) the values are the Shortmers 
In this file we implemented function that helps building the combinatorial alphabet with some other relative functions
'''


class InputAnalyze:
    shortmers_dict: dict #each key is a symbol and the value is 'ACGT' sequence
    alphabet_list: list
    alphabet_dict: dict #each key is number of segma (Z255) and the value is a list of shortmers that defines the segma
    list_of_lines: list
    dict_of_lines: dict #each key is a barcode and the value is the dna input sequence
    num_of_copies: int
    numOfShortmers: int
    number_of_shortmers_per_symbol: int
    shortmerSize: int
    number_of_alphabets: int
    code_distance: int
    shortmers_file_path: str
    sequence_design_file_path: str
    def __init__(self , num_of_copies , shormters_per_letter,  shortmers_file_path , sequence_design_file_path):
        self.number_of_shortmers_per_symbol = shormters_per_letter
        self.shortmers_file_path = shortmers_file_path
        self.sequence_design_file_path = sequence_design_file_path
        self.num_of_copies = num_of_copies
        self.shortmers_dict = fm.json_to_dict(shortmers_file_path)
        (self.numOfShortmers, self.shortmerSize) = number_size_of_shortmers_(self.shortmers_dict)
        (self.alphabet_list, self.alphabet_dict) = create_combinatorial_alphabet(self.shortmers_dict, self.number_of_shortmers_per_symbol)  #num_shortmers_per_symbol should come from input
        self.number_of_alphabets = len(self.alphabet_dict)
        (self.list_of_lines, self.dict_of_lines) = dna_input(sequence_design_file_path)
        self.code_distance = find_minimum_distance(self.shortmers_dict)
        fm.dump_alphabets(self.alphabet_dict , 'files/alphabets.json')
    def print_input_stats(self):
        print("--------------------------------------------Input Statistics---------------------------------------- \n")
        print(f"Num of Shortmers is : {self.numOfShortmers} \n")
        print("Shortmer size is : ", self.shortmerSize, " \n")
        print("Code Hamming Distance", self.code_distance, " \n")
        print(f"Number of Alphabets is : {self.number_of_alphabets} , therefore we need {math.floor(log2(self.number_of_alphabets))} bits \n")
        print("-------All input has been collected and analyzed, it's now time to proceed with the simulation------ \n")


'''
this function return number,size (pair) of shortmers given a dict
'''
def number_size_of_shortmers_(data_dict):
    return (len(data_dict) , len(data_dict['X1']))


'''
This function creates the alphabet out of the shortmers given the size of every letter's subset.
The function returns a list,dictionary pair , containing all the combinations of all possible alphabets
'''
def create_combinatorial_alphabet(shortmers_dict , num_shortmers_per_symbol):
    shortmers_keys = list(shortmers_dict.keys())
    alphabet_list = list(combinations(shortmers_keys, num_shortmers_per_symbol))
    alphabet_as_dict = {f'Z{i + 1}': alphabet_list[i] for i in range(len(alphabet_list))}
    return (alphabet_list, alphabet_as_dict)


'''
This function loads the DNA sequences
returns a list of lists where each list contains the whole DNA sequence(each line is a list)
also builds a dictionary where each key is the barcode and the values are the strands 
'''
def dna_input(file_path):
    list_of_lists = []
    dna_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            sequences = line.strip().split(',')
            list_of_lists.append(sequences[1:])
            dna_dict[sequences[0]] = sequences[1:]
    return (list_of_lists, dna_dict)


'''
Calculate the Hamming distance between two sequences.
'''
def hamming_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of the same length")
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


'''
Find the minimum Hamming distance between any two shortmers in the dictionary.
'''
def find_minimum_distance(shortmer_dict):
    min_distance = float('inf')
    keys = list(shortmer_dict.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            key1, key2 = keys[i], keys[j]
            seq1, seq2 = shortmer_dict[key1], shortmer_dict[key2]
            distance = hamming_distance(seq1, seq2)
            if distance < min_distance:
                min_distance = distance

    return min_distance
