import pandas as pd
import numpy as np

# Load the design file
file_path = 'design.csv'
design_df = pd.read_csv(file_path)

# Provided shortmers and combinatorial alphabet symbols
shrink_dict_3_mer = {
    'AAT': 'X1', 'ACA': 'X2', 'ATG': 'X3', 'AGC': 'X4',
    'TAA': 'X5', 'TCT': 'X6', 'TTC': 'X7', 'TGG': 'X8',
    'GAG': 'X9', 'GCC': 'X10', 'GTT': 'X11', 'GGA': 'X12',
    'CAC': 'X13', 'CCG': 'X14', 'CTA': 'X15', 'CGT': 'X16'
}

# Reverse the dictionary for symbol replacement
reverse_shrink_dict = {v: k for k, v in shrink_dict_3_mer.items()}


#Function to replace combinatorial symbols with shortmers
def replace_symbols(sequence, alphabet_symbols):
    for symbol, replacement in alphabet_symbols.items():
        sequence = sequence.replace(symbol, replacement)
    return sequence


#Function to generate reads with normal distribution
def generate_reads(sequence, mean_reads=30, std_dev=5):
    num_reads = int(np.random.normal(mean_reads, std_dev))
    reads = [sequence for _ in range(num_reads)]
    return reads


#Process the design file
all_reads = []

for index, row in design_df.iterrows():
    barcode = row['barcode']
    sequence = row['sequence']

    # Replace symbols with shortmers
    processed_sequence = replace_symbols(sequence, reverse_shrink_dict)

    # Generate reads
    reads = generate_reads(processed_sequence)
    all_reads.extend(reads)

# Output the generated reads
for read in all_reads[:10]:  # Display the first 10 reads for brevity
    print(read)
