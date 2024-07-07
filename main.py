import random
import analyze_input
import simulation
import json
from math import log2 , ceil

"""    
The main - Project 1.0
"""

# This Function creates a file with the alphabet that we created out of the shortmers
def dump_alphabets(alphabets , file_path):
    with open(file_path, 'w') as f:
        json.dump(alphabets, f, indent=4)
    print(f"The alphabet is written to '{file_path}'.")


def pick_number(min , max):
    mean = 12.5
    std_dev = 2.5
    while True:
        number = random.gauss(mean, std_dev)
        if min <= number <= max:
            return round(number)

if __name__ == '__main__':
    #num_of_copies = pick_number(5 , 20)
    num_of_copies = 3
    shortmers_dict = analyze_input.analyze_shortmers('files/shortmers.json')
    analyze_input.visualize_dictionary(shortmers_dict)

    numOfShort = analyze_input.number_of_shortmers(shortmers_dict)
    shortSize = analyze_input.shortmer_size(shortmers_dict)
    print("------------------------------------------------statistics----------------------------------")
    print(f"num of shortmers is : {numOfShort}")
    print("shortmer size is : ", shortSize)

    alphabet_list = analyze_input.create_combinatorial_alphabet(shortmers_dict, 5)



    # dict of letters and its subset of shortmers
    alphabet_dict = analyze_input.alphabet_as_dict(alphabet_list)

    #stats_dict = stats.convert_values_to_dict(alphabet_dict)
    stats_dict = {}
    number_of_alphabets = len(alphabet_dict)
    print(f"number of alphabets is : {number_of_alphabets} , therfore we need {ceil(log2(number_of_alphabets))} bits" )
    analyze_input.visualize_alphabet(alphabet_dict , shortmers_dict)
    dump_alphabets(alphabet_dict, 'files/alphabets.json')

    print("-------------------------------------------------------------------------------------------")

    list_of_lines = analyze_input.dna_input('files/sequence_design_file.dna')

    print("---------------------got all the input , and it is analyzed , now simulate.----------------")

    result_with_symbols , stats_dict = simulation.run(list_of_lines, num_of_copies, alphabet_dict  , stats_dict)
    result_with_sequence= simulation.run_shortmers(list_of_lines, num_of_copies, alphabet_dict, shortmers_dict )

    print(stats_dict)

    print("-------------------------------------------------------------------------------------------")
    print("finished the simulation :")

    dict_sym_str = simulation.dump_out_symbols('files/output_symbols_str.json', result_with_symbols, list_of_lines ,True)
    dict_seq_str = simulation.dump_out_sequences('files/output_sequence_str.json', result_with_sequence, list_of_lines ,  True)

    dict_sym = simulation.dump_out_symbols('files/output_symbols.json', result_with_symbols, list_of_lines )
    dict_seq = simulation.dump_out_sequences('files/output_sequence.json', result_with_sequence, list_of_lines)


