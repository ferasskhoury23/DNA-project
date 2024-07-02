import json
from itertools import combinations

"""    
the input is json file while the keys are the symbols (X1 , X2 .....) the values are the sequences 
"""
def analyze_shortmers(path):
    with open(path , 'r') as file:
        data_dict = json.load(file)
        return data_dict

def number_of_shortmers(data_dict):
    return len(data_dict)

def shortmer_size(data_dict):
    return len(data_dict['X1'])


def create_combinatorial_alphabet(shortmers_dict , num_shortmers_per_symbol):
    shortmers_keys = list(shortmers_dict.keys())
    return list(combinations(shortmers_keys, num_shortmers_per_symbol))

"""
keys is indexes of segma (Z1 , Z1080 ...)
values is the segmot
"""
def alphabet_as_dict(alphabet):
    return {f'Z{i + 1}': alphabet[i] for i in range(len(alphabet))}



def dna_input(file_path):
    list_of_lists = []
    with open(file_path, 'r') as file:
        for line in file:
            list_of_lists.append(line.strip().split(','))

    return list_of_lists





