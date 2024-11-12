import copy
import analyze_input
import simulation
import fileManager as fm
import error as er
import error_fixing as fix_test
import Utilities as ut

"""    
The main - Final Version
"""

if __name__ == '__main__':
    stats_dict = {}
    try:
        (shortmers_per_letter, num_of_copies, error_rate) = ut.parameters_from_input()
    except ValueError as e:
        print(f"{e}")
        exit(1)

    shortmers_file_path = 'files/input_shortmers.json'
    sequence_design_file_path = 'files/sequence_design_file.dna'
    Input = analyze_input.InputAnalyze(num_of_copies, shortmers_per_letter, shortmers_file_path, sequence_design_file_path)
    Input.print_input_stats()

    '''
    reconstruction
    simulate with symbols
    we use stats_dict only with symbols so that we can print stats for each shortmer used    
    '''
    (result_with_symbols, stats_dict) = simulation.run(Input, stats_dict)
    fm.dump_out_sim('files/output_symbols_str.json', result_with_symbols, Input.list_of_lines,Input.dict_of_lines, True, True)
    out_dict_list_of_shortmers = fm.dump_out_sim('files/output_symbols.json', result_with_symbols, Input.list_of_lines,Input.dict_of_lines, True)
    fm.dump_out_statistics('files/out1put_statistics.json', stats_dict)

    '''simulate with sequences'''
    result_with_sequence = simulation.run_shortmers(Input)
    dict_seq_str = fm.dump_out_sim('files/output_sequence_str.json', result_with_sequence, Input.list_of_lines,Input.dict_of_lines, False, True)
    original_dict = copy.deepcopy(dict_seq_str)
    fm.dump_out_sim('files/output_sequence.json', result_with_sequence, Input.list_of_lines,Input.dict_of_lines)

    strand_length_dict = ut.helper(dict_seq_str) #dictionary of strands lengths

    print("The simulation is complete, and we will now begin planning for error identification and subsequent fixes \n")
    error_dict = er.plant_error(dict_seq_str, num_of_copies, error_rate, out_dict_list_of_shortmers, Input.shortmers_dict)
    fm.dict_to_json(error_dict, "files/output_errors_cluster.json")

    '''Fixing the errors on each cluster'''
    after_fixing, strand_result = fix_test.fix_clusters(error_dict ,strand_length_dict , Input.shortmers_dict , num_of_copies ,Input.number_of_shortmers_per_symbol,Input.alphabet_dict)
    fm.dict_to_json(after_fixing, "files/final_result.json")
    fm.dict_to_json(strand_result, "files/result_strand.json")

    '''calculate Final result (Success rate)'''
    success_rate = fix_test.calculate_sucess_rate(after_fixing, original_dict)
    print(f"Success rate:{success_rate}  \n")

    print("------------finished the simulation and fixed the errors , open the json files to see the results----------")
