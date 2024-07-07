import random
import analyze_input
import simulation

from math import log2 , ceil
import fileManager as FM

"""    
The main - Project 2.0
"""
def pick_number(min , max):
    mean = 12.5
    std_dev = 2.5
    while True:
        number = random.gauss(mean, std_dev)
        if min <= number <= max:
            return round(number)

def printStatistics(numOfShort , shortSize , number_of_alphabets):
    print("------------------------------------------------statistics----------------------------------")
    print(f"num of shortmers is : {numOfShort}")
    print("shortmer size is : ", shortSize)
    print(f"number of alphabets is : {number_of_alphabets} , therfore we need {ceil(log2(number_of_alphabets))} bits")
    print("---------------------------------stats finished----------------------------------------------------")

if __name__ == '__main__':
    stats_dict = {}
    #num_of_copies = pick_number(5 , 20)
    num_of_copies = 3

    shortmers_dict = analyze_input.analyze_shortmers('files/input_shortmers.json')
    analyze_input.visualize_dictionary(shortmers_dict)
    numOfShort , shortSize = analyze_input.number_size_of_shortmers_(shortmers_dict)

    '''alphabet'''
    # dict and list of letters and its subset of shortmers
    alphabet_list , alphabet_dict = analyze_input.create_combinatorial_alphabet(shortmers_dict, 5)
    FM.dump_alphabets(alphabet_dict, 'files/input_alphabets.json')
    number_of_alphabets = len(alphabet_dict)

    '''stats and visualize'''
    printStatistics(numOfShort , shortSize , number_of_alphabets)
    analyze_input.visualize_alphabet(alphabet_dict, shortmers_dict)


    list_of_lines = analyze_input.dna_input('files/sequence_design_file.dna')
    print("---------------------got all the input , and it is analyzed , now simulate.----------------")

    result_with_symbols , stats_dict = simulation.run(list_of_lines, num_of_copies, alphabet_dict  , stats_dict)
    result_with_sequence= simulation.run_shortmers(list_of_lines, num_of_copies, alphabet_dict, shortmers_dict )


    print("-------------------------------------------------------------------------------------------")
    print("finished the simulation :")

    dict_sym_str = FM.dump_out_symbols('files/output_symbols_str.json', result_with_symbols, list_of_lines ,True)
    dict_seq_str = FM.dump_out_sequences('files/output_sequence_str.json', result_with_sequence, list_of_lines ,  True)

    dict_sym = FM.dump_out_symbols('files/output_symbols.json', result_with_symbols, list_of_lines )
    dict_seq = FM.dump_out_sequences('files/output_sequence.json', result_with_sequence, list_of_lines)
    FM.dump_out_statistics('files/output_statistics.json' , stats_dict)


'''
    #new simulation
    stats_dict_changed = {}
    num_of_copies_changed = int(num_of_copies * 0.5)
    print("Number of copies" , num_of_copies_changed)
    result_with_symbols_changed, stats_dict_changed = simulation.run(list_of_lines, num_of_copies_changed, alphabet_dict, stats_dict_changed)
'''

