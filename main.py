import math
import random
import analyze_input
import simulation
import fileManager as fm
import error as er
import Graphics as gr
import SMAIR_error_fixing as fix_test
"""    
The main - Project 3.0
started fixing the errors we planted in proj2.0
"""
def pick_number(min , max):
    mean = 12.5
    std_dev = 2.5
    while True:
        number = random.gauss(mean, std_dev)
        if min <= number <= max:
            return round(number)


#consider make a class of all user inputs : num of copies , files paths.

if __name__ == '__main__':
    stats_dict = {}
    num_of_copies = pick_number(5 , 20)
    print("number of copies is :", num_of_copies)
    error_rate = 0.05
    #num_of_copies = 4

    shortmers_file_path = 'files/input_shortmers.json'    #consider make the paths as class
    sequence_design_file_path = 'files/sequence_design_file.dna' #consider make the paths as class

    Input = analyze_input.InputAnalyze(num_of_copies, shortmers_file_path, sequence_design_file_path)
    Input.print_input_stats()
    print("---------------------got all the input , and it is analyzed , now simulate.----------------")

    '''
    simulate with symbols
    we use stats_dict only with symbols so that we can print stats for each shortmer used    
    '''
    (result_with_symbols, stats_dict) = simulation.run(Input, stats_dict)
    fm.dump_out_sim('files/output_symbols_str.json', result_with_symbols, Input.list_of_lines,Input.dict_of_lines, True, True)
    out_dict_list_of_shortmers = fm.dump_out_sim('files/output_symbols.json', result_with_symbols, Input.list_of_lines,Input.dict_of_lines, True)
    fm.dump_out_statistics('files/output_statistics.json', stats_dict)


    '''simulate with sequences'''
    result_with_sequence = simulation.run_shortmers(Input)
    dict_seq_str = fm.dump_out_sim('files/output_sequence_str.json', result_with_sequence, Input.list_of_lines,Input.dict_of_lines, False, True)
    fm.dump_out_sim('files/output_sequence.json', result_with_sequence, Input.list_of_lines,Input.dict_of_lines)




    print("-------------------------------------------------------------------------------------------")
    print("finished the simulation :")
    print("------------------------------------------------start errors:-------------------------------------")
    error_dict = er.plant_error(dict_seq_str, num_of_copies, error_rate, out_dict_list_of_shortmers, Input.shortmers_dict)
    fm.dict_to_json(error_dict, "files/output_errors_cluster.json")
    print("-------------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------------")



    '''simulation2
    stats_dict_2 = {}
    num_of_copies_2 = math.floor(num_of_copies/4)
    Input_2 = analyze_input.InputAnalyze(num_of_copies_2, shortmers_file_path, sequence_design_file_path)
    result_with_symbols_2, stats_dict_2 = simulation.run(Input_2, stats_dict_2)
    '''

    #gr.compare_shortmers(stats_dict , stats_dict_2)


    '''testing error fixing'''
    cluster = error_dict['AAA']
    print("the original cluster : " , cluster)
    fix = fix_test.fix_main(cluster , Input.shortmers_dict , num_of_copies , 40 , Input.code_distance ,Input.number_of_shortmers_per_symbol)

    with open("files/testing.txt", "w") as file:
        for element in fix:
            file.write(element + "\n")