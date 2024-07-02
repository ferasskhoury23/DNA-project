import random
from itertools import combinations
import numpy as np
import pandas as pd

#comb(n,k)  n b7ar k (n nCr k) returns the number itself
#combinations returns the whole combinations themselfs

# Load the design file
file_path = 'design.csv'
design_df = pd.read_csv(file_path)

dna_components = ['A', 'C', 'G', 'T']


def replace_symbols(sequence, alphabet_symbols):
    for symbol, replacement in alphabet_symbols.items():
        sequence = sequence.replace(symbol, replacement)
    return sequence



# Generate a set of shortmers
def generate_shortmers(shortmer_length, num_shortmers):   # fix repetition
    shortmers = []
    for _ in range(num_shortmers):
        shortmer = ''.join(random.choices(dna_components, k=shortmer_length))
        shortmers.append(shortmer)
    return shortmers


shortmers = generate_shortmers()

# Create combinatorial alphabet symbols (each symbol is a set of num_shortmers_per_symbol shortmers)
def create_combinatorial_alphabet(shortmers, num_shortmers_per_symbol):
    return list(combinations(shortmers, num_shortmers_per_symbol))

print(create_combinatorial_alphabet(generate_shortmers(3 , 16) , 5))
print("------------------------------------------------------------------")







# Design file consists of sequences designed over the combinatorial alphabet
def create_design_file(alphabet, num_sequences):
    design_file = []
    for _ in range(num_sequences):
        sequence = random.choice(alphabet)
        design_file.append(sequence)
    return design_file
    #return [random.choice(alphabet) for _ in range(num_sequences)]




# Step 2: Simulate DNA Reads
# Generate DNA sequences from combinatorial alphabet symbols
def generate_dna_sequences(design_file):
    dna_sequences = []
    for sequence in design_file:
        dna_sequence = ''.join(sequence)
        dna_sequences.append(dna_sequence)
    return dna_sequences
    #return [''.join(sequence) for sequence in design_file]



# Generate reads following a normal distribution around a mean
def generate_reads(dna_sequences, mean_reads, std_dev):
    reads = []
    for sequence in dna_sequences:
        num_reads = max(1, int(np.random.normal(mean_reads, std_dev)))
        reads.extend([sequence] * num_reads)
    return reads



# Main simulation function
def simulate_combinatorial_dna(shortmer_length, num_shortmers, num_shortmers_per_symbol, num_sequences, mean_reads=30, std_dev=5):
    shortmers = generate_shortmers(shortmer_length, num_shortmers)
    alphabet = create_combinatorial_alphabet(shortmers, num_shortmers_per_symbol)
    design_file = create_design_file(alphabet, num_sequences)
    print("design_file is : ", design_file)
    dna_sequences = generate_dna_sequences(design_file)
    print("dna_sequences is : ", dna_sequences)
    reads = generate_reads(dna_sequences, mean_reads, std_dev)
    return reads


# Example usage
shortmer_length = 3  # length of each shortmer
num_shortmers = 16  # number of shortmers
num_shortmers_per_symbol = 5  # number of shortmers per alphabet symbol
num_sequences = 2  # number of sequences in the design file

reads = simulate_combinatorial_dna(shortmer_length, num_shortmers, num_shortmers_per_symbol, num_sequences)

print("Generated Reads:")
for read in reads:
    print(read)
