import analyze_input
import simulation
import json
def dump_alphabets(alphabets , file_path):
    with open(file_path, 'w') as f:
        json.dump(alphabets, f, indent=4)
    print(f"The alphabet is written to '{file_path}'.")


if __name__ == '__main__':
    num_of_copies = 20
    shortmers_dict = analyze_input.analyze_shortmers('files/shortmers.json')

    numOfShort = analyze_input.number_of_shortmers(shortmers_dict)
    shortSize = analyze_input.shortmer_size(shortmers_dict)

    print(f"num of shortmers is : {numOfShort}")
    print("shortmer size is : ", shortSize)



    alphabet_list = analyze_input.create_combinatorial_alphabet(shortmers_dict, 5)

    # dict of segma and its group of shortmers
    alphabet_dict = analyze_input.alphabet_as_dict(alphabet_list)
    dump_alphabets(alphabet_dict , 'files/alphabets.json')
    print("-------------------------------------------------------------------------------------------")



    list_of_lines = analyze_input.dna_input('files/sequence_design_file.dna')
    #print(list_of_lines)
    print("------------------------got all the input , and it is analyzed , now simulate.----------------------------------------------------")


    result_with_symbols = simulation.run(list_of_lines,num_of_copies , alphabet_dict)
    result_with_sequence = simulation.run_shortmers(list_of_lines,num_of_copies , alphabet_dict , shortmers_dict)

    print("-------------------------------------------------------------------------------------------")
    print("finished the simulation :")

    simulation.dump_out_symbols('files/output_symbols.json', result_with_symbols , list_of_lines )
    simulation.dump_out_sequences('files/output_sequence.json', result_with_sequence, list_of_lines)