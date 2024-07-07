import json

def list_to_str(lst):
    return ', '.join(lst)

'''
helper to change the values of the dict to strings
'''
def generate_copies_dict(translations_dict):
    result_dict = {}
    for key, translations in translations_dict.items():
        result_list = []
        for translation in translations:
            # Join the list of strings into a single string without spaces
            translation_string = ''.join(translation)
            result_list.append(translation_string)
        result_dict[key] = result_list
    return result_dict



'''
dumps the simulation output to a file , with symbols
'''
def dump_out_symbols(file_path , result , list_of_lines , as_string = False):
    my_dict = {}
    for line, res in zip(list_of_lines, result):
        my_dict[list_to_str(line)] = res
    if (as_string):
        my_dict = generate_copies_dict(my_dict)
    try:
        # Attempt to open the file in 'w' mode (exclusive creation)
        with open(file_path, 'w') as f:
            json.dump(my_dict, f, indent=4)
        if as_string:
            print(f"The simulation output (with symbols) is written to '{file_path}' AS STRINGS")
        else:
            print(f"The simulation output (with symbols) is written to '{file_path}'")
        return my_dict
    except FileExistsError:
        print(f"The file '{file_path}' already exists. Creation failed.")
        return None

'''
dumps the simulation output to a file , with sequences
'''
def dump_out_sequences(file_path , result , list_of_lines  ,as_string = False):
    my_dict = {}
    for line, res in zip(list_of_lines, result):
        my_dict[list_to_str(line)] = res
    if(as_string):
        my_dict = generate_copies_dict(my_dict)
    try:
        # Attempt to open the file in 'w' mode (exclusive creation)
        with open(file_path, 'w') as f:
            json.dump(my_dict, f, indent=4)
        if(as_string):
            print(f"The simulation output (with the whole sequences) is written to '{file_path}' AS STRINGS")
        else:
            print(f"The simulation output (with the whole sequences) is written to '{file_path}'")
        return my_dict
    except FileExistsError:
        print(f"The file '{file_path}' already exists. Creation failed.")
        return None


def dump_out_statistics(file_path , stats_dict):
    try:
        with open(file_path, 'w') as f:
            json.dump(stats_dict, f, indent=4)
            print(f"The simulation stats  is written to '{file_path}'")
    except FileExistsError:
        print(f"The file '{file_path}' already exists. Creation failed.")
        return None


# This Function creates a file with the alphabet that we created out of the shortmers
def dump_alphabets(alphabets , file_path):
    with open(file_path, 'w') as f:
        json.dump(alphabets, f, indent=4)
    print(f"The alphabet is written to '{file_path}'.")
