import json


"""    
File Manager - Final Version
"""


'''
This function reads the json file given a path , and returns it as a dict
it is used to read the shortmers input and other uses 
'''
def json_to_dict(path):
    with open(path, 'r') as file:
        data_dict = json.load(file)
        return data_dict


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
dumps the simulation output to a json file .
returns it as a dict
'''
def dump_out_sim(file_path , result , list_of_lines ,barcode_dict ,with_symbols=False ,as_string=False):
    my_dict = {}
    for line, res in zip(list_of_lines, result):
        my_dict[find_key_by_value(barcode_dict, line)] = res
    if (as_string):
        my_dict = generate_copies_dict(my_dict)
    try:
        with open(file_path, 'w') as f:
            json.dump(my_dict, f, indent=4)
        if as_string:
            if with_symbols:
                print(f"The simulation output (with symbols) is written to '{file_path}' AS STRINGS")
            else:
                print(f"The simulation output (with the whole sequences) is written to '{file_path}' AS STRINGS")
        else:
            if with_symbols:
                print(f"The simulation output (with symbols) is written to '{file_path}'")
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


'''
this Function creates a json file from the alphabet dict we created
'''
def dump_alphabets(alphabets_dict , file_path):
    with open(file_path, 'w') as f:
        json.dump(alphabets_dict, f, indent=4)
    print(f"The alphabet is written to '{file_path}'.")

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def dict_to_json(dictionary, file_path):
    with open(file_path, 'w') as f:
        json.dump(dictionary, f, indent=4)