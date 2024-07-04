import json
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import random

"""    
analyze_input - Project 1.0

The input is json file while the keys are the symbols (X1 , X2 .....) the values are the Shortmers 
In this file we implemented function that helps building the combinatorial alphabet with some other relative functions
"""

# This Function loads the shortmers for sa specific file given a path
def analyze_shortmers(path):
    with open(path, 'r') as file:
        data_dict = json.load(file)
        return data_dict

# This Function return number of shortmers give a dict
def number_of_shortmers(data_dict):
    return len(data_dict)

# This Function returns the size of shortmer give a dict
def shortmer_size(data_dict):
    return len(data_dict['X1'])

# This Function creates the alphabet out of the shortmers given the size of every letter's subset
def create_combinatorial_alphabet(shortmers_dict , num_shortmers_per_symbol):
    shortmers_keys = list(shortmers_dict.keys())
    return list(combinations(shortmers_keys, num_shortmers_per_symbol))

# This Function make the alphabet as a dict keys is indexes of letters (Z1 , Z1080 ...) values is the subset of values
def alphabet_as_dict(alphabet):
    return {f'Z{i + 1}': alphabet[i] for i in range(len(alphabet))}

# This Function loads the DNA sequences
def dna_input(file_path):
    list_of_lists = []
    with open(file_path, 'r') as file:
        for line in file:
            list_of_lists.append(line.strip().split(','))

    return list_of_lists



# This Function Visualizes the dictionary in a formatted style with keys and values aligned in columns
def visualize_dictionary(data):
    num_columns = 2
    num_rows = len(data) // num_columns + (len(data) % num_columns > 0)
    keys = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    text_properties = dict(horizontalalignment='center', verticalalignment='center', fontsize=12,
                           fontfamily='monospace')
    fig.patch.set_facecolor('white')
    ax.set_title('Shormters', fontsize=20, color='black', pad=20)

    for i in range(len(data)):
        row = i % num_rows
        col = i // num_rows
        x = col * 0.5
        y = 1 - (row / num_rows) - 0.05
        color = 'red'

        ax.text(x, y, f"$X_{{{i + 1}}}$ =  {values[i]}", color=color, **text_properties)

    plt.grid(visible=False)
    plt.box(True)
    plt.tight_layout()
    plt.show()


# This Function Visualizes a subset of the given dictionary of shortmers in a decorated matrix.
def visualize_alphabet(data, num_letters=20):
    if num_letters > len(data):
        raise ValueError("num_letters is greater than the number of available letters in the data.")

    # Visualize random letters
    letters_to_visualize = random.sample(list(data.keys()), num_letters)
    shortmers = sorted(list(next(iter(data.values()))))  # Assuming all sets have the same shortmers

    matrix = np.zeros((len(shortmers), num_letters))

    for col, letter in enumerate(letters_to_visualize):
        for row, shortmer in enumerate(shortmers):
            if shortmer in data[letter]:
                matrix[row, col] = 1

    fig, ax = plt.subplots()
    ax.matshow(matrix, cmap='Greys')

    ax.set_xticks(np.arange(len(letters_to_visualize)))
    ax.set_yticks(np.arange(len(shortmers)))

    ax.set_xticklabels(letters_to_visualize, rotation=90)
    ax.set_yticklabels(shortmers)

    ax.set_xlabel('Letters')
    ax.set_ylabel('Shortmers')

    plt.show()



