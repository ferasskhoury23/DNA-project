import json
from itertools import combinations
import numpy as np


"""    
the input is json file while the keys are the symbols (X1 , X2 .....) the values are the sequences 
"""
def analyze_input(path):
    with open(path , 'r') as file:
        data_dict = json.load(file)
        return data_dict

def number_of_shortmers(data_dict):
    return len(data_dict)

def shortmer_size(data_dict):
    return len(data_dict['X1'])


def create_combinatorial_alphabet(data_dict , num_shortmers_per_symbol):
    shortmers_keys = list(data_dict.keys())
    return list(combinations(shortmers_keys, num_shortmers_per_symbol))

"""
keys is indexes of segma
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


""" Generate a list with num_copies of the given element. Args: -
    element: The element to generate copies of. - num_copies: Number of copies to generate. Returns: - List containing num_copies of the element. """
def generate_copies(sequence, num_copies):
    return [sequence] * num_copies


def normalize(list_of_shortmers, num_of_copies):
    mean = 0.3
    std_dev = 0.1

    # Generate "num_of_copies" normally distributed values
    normal_values = np.random.normal(mean, std_dev, num_of_copies)

    # Normalize the values to map to the 3 items
    normalized_indices = (normal_values - normal_values.min()) / (normal_values.max() - normal_values.min())
    mapped_indices = (normalized_indices * (len(list_of_shortmers) - 1)).astype(int)

    # Create the "num_of_copies" copies
    copies = [list_of_shortmers[i] for i in mapped_indices]
    print("Generated copies:")
    print(copies)
    return copies


def test(list_of_lists , num_of_copies , dict):
    tmp = []
    result = []

    for _ in list_of_lists:
        # Initialize tmp as a list of empty lists, one for each copy
        tmp = [[] for _ in range(num_of_copies)]


    for line in list_of_lists:
        for sequence in line:

            if sequence.startswith('Z'):
                listNormal = normalize( dict[sequence], num_of_copies)
                for j in range(num_of_copies):
                     tmp[j].append( listNormal[j])
            else:
                for k in range(num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)

    return result



if __name__ == '__main__':

    data = analyze_input('files/shortmers.json')
    numOfShort = number_of_shortmers(data)
    print(numOfShort)
    shortSize = shortmer_size(data)
    print(shortSize)
    print("-------------------------------------------------------------------------------------------")
    alphabet = create_combinatorial_alphabet(data , 5)

    my_dict = alphabet_as_dict(alphabet)

    #print(my_dict)
    list_of_lists = dna_input('files/sequence_design_file.dna')
    print(list_of_lists)

    print("-------------------------------------------------------------------------------------------")


    result = test(list_of_lists,4 , my_dict)

    print("-------------------------------------------------------------------------------------------")
    print("finished test")
    print(result)



