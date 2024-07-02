import random
from itertools import combinations
import numpy as np
import pandas as pd

#comb(n,k)  n b7ar k (n nCr k) returns the number itself
#combinations returns the whole combinations themselfs


dna_components = ['A', 'C', 'G', 'T']

def load_design(file_path):
    design_df = pd.read_csv(file_path)


#Generate a set(list) of shortmers
def generate_shortmers(shortmer_length, num_shortmers):   # fix repetition
    shortmers = []
    for _ in range(num_shortmers):
        shortmer = ''.join(random.choices(dna_components, k=shortmer_length))
        shortmers.append(shortmer)
    return shortmers




# Create combinatorial alphabet symbols (each symbol is a set of num_shortmers_per_symbol shortmers)
def create_combinatorial_alphabet(shortmers, num_shortmers_per_symbol):
    return list(combinations(shortmers, num_shortmers_per_symbol))



'''
def replace_symbols(sequence, alphabet):
  

def process_design_file:    
    for index, row in design_df.iterrows():
        barcode = row['barcode']
        sequence = row['sequence']
    
        # Replace symbols with shortmers
        processed_sequence = replace_symbols(sequence , alphabet)
    
'''


if __name__ == '__main__':
    # Load the design file
    load_design('design.csv')

    shortmers = generate_shortmers(3, 16)
    alphabet = create_combinatorial_alphabet(shortmers, 5)

    print("------------------------------------------------------------------")
    print("Alphabet: ", alphabet)
    print("------------------------------------------------------------------")

