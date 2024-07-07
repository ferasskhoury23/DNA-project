import random
import analyze_input
import simulation
import fileManager as fm

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


if __name__ == '__main__':
    stats_dict = {}
    #num_of_copies = pick_number(5 , 20)
    num_of_copies = 3
    shortmers_file_path = 'files/input_shortmers.json'
    sequence_design_file_path = 'files/sequence_design_file.dna'

    Input = analyze_input.InputAnalyze(num_of_copies,shortmers_file_path,sequence_design_file_path)
    Input.print_input_stats()
    print("---------------------got all the input , and it is analyzed , now simulate.----------------")

    result_with_symbols, stats_dict = simulation.run(Input,stats_dict)
    result_with_sequence = simulation.run_shortmers(Input)

    print("-------------------------------------------------------------------------------------------")
    print("finished the simulation :")

    dict_sym_str = fm.dump_out_symbols('files/output_symbols_str.json', result_with_symbols, Input.list_of_lines ,True)
    dict_seq_str = fm.dump_out_sequences('files/output_sequence_str.json', result_with_sequence, Input.list_of_lines ,  True)
    #dict_sym = fm.dump_out_symbols('files/output_symbols.json', result_with_symbols, Input.list_of_lines )
    #dict_seq = fm.dump_out_sequences('files/output_sequence.json', result_with_sequence, Input.list_of_lines)
    fm.dump_out_statistics('files/output_statistics.json' , stats_dict)

