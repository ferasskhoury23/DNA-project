from itertools import combinations
from math import log2, ceil
import fileManager as fm


"""
analyze_input - Project 2.0

The input is json file while the keys are the symbols (X1 , X2 .....) the values are the Shortmers 
In this file we implemented function that helps building the combinatorial alphabet with some other relative functions
"""
class InputAnalyze:
    shortmers_dict: dict
    alphabet_list: list
    alphabet_dict: dict
    list_of_lines: list
    dict_of_lines: dict
    num_of_copies: int
    numOfShortmers: int
    shortmerSize: int
    number_of_alphabets: int
    shortmers_file_path: str
    sequence_design_file_path: str
    def __init__(self , num_of_copies , shortmers_file_path , sequence_design_file_path):
        self.shortmers_file_path = shortmers_file_path
        self.sequence_design_file_path = sequence_design_file_path
        self.num_of_copies = num_of_copies
        self.shortmers_dict = fm.json_to_dict(shortmers_file_path)
        self.numOfShortmers, self.shortmerSize = number_size_of_shortmers_(self.shortmers_dict)
        self.alphabet_list, self.alphabet_dict = create_combinatorial_alphabet(self.shortmers_dict, 5)
        self.number_of_alphabets = len(self.alphabet_dict)
        self.list_of_lines, self.dict_of_lines = dna_input(sequence_design_file_path)
        fm.dump_alphabets(self.alphabet_dict , 'files/alphabets.json')
    def print_input_stats(self):
        print("--------------------------------Input Statistics----------------------------------")
        print(f"num of shortmers is : {self.numOfShortmers}")
        print("shortmer size is : ", self.shortmerSize)
        print(f"number of alphabets is : {self.number_of_alphabets} , therfore we need {ceil(log2(self.number_of_alphabets))} bits")
        print("--------------------------------Input stats finished----------------------------------------------------")




#this function return number,size (pair) of shortmers given a dict
def number_size_of_shortmers_(data_dict):
    return len(data_dict) , len(data_dict['X1'])


'''This function creates the alphabet out of the shortmers given the size of every letter's subset.
The function returns a list,dictionary pair , containing all the combinations of all possible alphabets'''
def create_combinatorial_alphabet(shortmers_dict , num_shortmers_per_symbol):
    shortmers_keys = list(shortmers_dict.keys())
    alphabet_list = list(combinations(shortmers_keys, num_shortmers_per_symbol))
    alphabet_as_dict = {f'Z{i + 1}': alphabet_list[i] for i in range(len(alphabet_list))}
    return (alphabet_list, alphabet_as_dict)


'''This function loads the DNA sequences
returns a list of lists where each list contains the whole DNA sequence(each line is a list) '''
def dna_input(file_path):
    list_of_lists = []
    dna_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            sequences = line.strip().split(',')
            list_of_lists.append(sequences[1:])
            dna_dict[sequences[0]] = sequences[1:]
    return list_of_lists, dna_dict