import json
from itertools import combinations
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import log2 , ceil
import fileManager as fm
"""    
analyze_input - Project 1.0

The input is json file while the keys are the symbols (X1 , X2 .....) the values are the Shortmers 
In this file we implemented function that helps building the combinatorial alphabet with some other relative functions
"""
class InputAnalyze:
    shortmers_dict : dict
    alphabet_list : list
    alphabet_dict : dict
    list_of_lines : list
    num_of_copies : int
    numOfShortmers : int
    shortmerSize : int
    number_of_alphabets : int
    shortmers_file_path : str
    sequence_design_file_path : str
    def __init__(self , num_of_copies , shortmers_file_path , sequence_design_file_path):
        self.shortmers_file_path = shortmers_file_path
        self.sequence_design_file_path = sequence_design_file_path
        self.num_of_copies = num_of_copies
        self.shortmers_dict = analyze_shortmers(shortmers_file_path)
        self.numOfShortmers , self.shortmerSize = number_size_of_shortmers_(self.shortmers_dict)
        self.alphabet_list , self.alphabet_dict = create_combinatorial_alphabet(self.shortmers_dict, 5)
        self.number_of_alphabets = len(self.alphabet_dict)
        self.list_of_lines = dna_input(sequence_design_file_path)
        fm.dump_alphabets(self.alphabet_dict , 'files/alphabets.json')
    def print_input_stats(self):
        print("--------------------------------Input Statistics----------------------------------")
        print(f"num of shortmers is : {self.numOfShortmers}")
        print("shortmer size is : ", self.shortmerSize)
        print(f"number of alphabets is : {self.number_of_alphabets} , therfore we need {ceil(log2(self.number_of_alphabets))} bits")
        print("--------------------------------Input stats finished----------------------------------------------------")



#This function reads the shortmers json file given a path , and returns it as a dict
def analyze_shortmers(path):
    with open(path, 'r') as file:
        data_dict = json.load(file)
        return data_dict

#this function return number,size (pair) of shortmers given a dict
def number_size_of_shortmers_(data_dict):
    return len(data_dict) , len(data_dict['X1'])


'''This function creates the alphabet out of the shortmers given the size of every letter's subset.
The function returns a list,dictionary pair , containing all the combinations of all possible alphabets'''
def create_combinatorial_alphabet(shortmers_dict , num_shortmers_per_symbol):
    shortmers_keys = list(shortmers_dict.keys())
    alphabet_list = list(combinations(shortmers_keys, num_shortmers_per_symbol))
    alphabet_as_dict = {f'Z{i + 1}': alphabet_list[i] for i in range(len(alphabet_list))}
    return alphabet_list,alphabet_as_dict


'''This function loads the DNA sequences
returns a list of lists where each list contains the whole DNA sequence(each line is a list) '''
def dna_input(file_path):
    list_of_lists = []
    with open(file_path, 'r') as file:
        for line in file:
            list_of_lists.append(line.strip().split(','))

    return list_of_lists


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

def visualize_alphabet(alphabet, shortmers_dict):
       # Create a set of all shortmers
    all_shortmers = sorted(set(shortmer for shortmers in alphabet.values() for shortmer in shortmers))

    # Create a DataFrame with shortmers as rows and sigmas as columns
    df = pd.DataFrame(0, index=all_shortmers, columns=alphabet.keys())

    # Fill the DataFrame with presence (1) of shortmers
    for sigma, shortmers in alphabet.items():
        for shortmer in shortmers:
            df.at[shortmer, sigma] = 1

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df, cmap="Greys", cbar=False, linewidths=.5, linecolor='black')
    plt.xlabel('Sigma')
    plt.ylabel('Shortmer')
    plt.title('Shortmer Presence Across Sigmas')
    plt.show()

