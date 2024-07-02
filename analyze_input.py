import json
from itertools import combinations
"""    
the input is json file while the keys are the symbols (X1 , X2 .....) the values are the sequences 


"""
data = {
    'X1': 'AAT',
    'X2': 'ACA',
    'X3': 'ATG',
    'X4': 'AGC',
    'X5': 'TAA',
    'X6': 'TCT',
    'X7': 'TTC',
    'X8': 'TGG',
    'X9': 'GAG',
    'X10': 'GCC',
    'X11': 'GTT',
    'X12': 'GGA',
    'X13': 'CAC',
    'X14': 'CCG',
    'X15': 'CTA',
    'X16': 'CGT'}

'''
def analyze_input(path):
    with open(path , 'r') as file:
        data_dict = json.load(file)
        return data_dict
'''
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


if __name__ == '__main__':
    numOfShort = number_of_shortmers(data)
    print(numOfShort)
    shortSize = shortmer_size(data)
    print(shortSize)
    print("-------------------------------------------------------------------------------------------")
    alphabet = create_combinatorial_alphabet(data , 4)
    #my_dict = {f'Z{i + 1}': value for index, value in enumerate(alphabet)}

    my_dict = {f'Z{i + 1}': alphabet[i] for i in range(len(alphabet))}
    print(my_dict)
