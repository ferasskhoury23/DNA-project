import json
import numpy as np

""" Generate a list with num_copies of the given element. Args: -
    element: The element to generate copies of. - num_copies: Number of copies to generate. Returns: - List containing num_copies of the element. """
def generate_copies(sequence, num_copies):
    return [sequence] * num_copies


def normalize(list_of_shortmers, num_of_copies):
    mean = 0.3
    std_dev = 0.1

    # Generate "num_of_copies" normally distributed values
    normal_values = np.random.normal(mean, std_dev, num_of_copies)

    # Normalize the values to map to the 3 items
    normalized_indices = (normal_values - normal_values.min()) / (normal_values.max() - normal_values.min())
    mapped_indices = (normalized_indices * (len(list_of_shortmers) - 1)).astype(int)

    # Create the "num_of_copies" copies
    copies = [list_of_shortmers[i] for i in mapped_indices]
    #print("Generated copies:")
    #print(copies)
    return copies


def run(list_of_lists , num_of_copies , dict):
    tmp = []
    result = []

    for _ in list_of_lists:
        # Initialize tmp as a list of empty lists, one for each copy
        tmp = [[] for _ in range(num_of_copies)]


    for line in list_of_lists:
        for sequence in line:

            if sequence.startswith('Z'):
                listNormal = normalize( dict[sequence], num_of_copies)
                for j in range(num_of_copies):
                     tmp[j].append( listNormal[j])
            else:
                for k in range(num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result


def run_shortmers(list_of_lists , num_of_copies , dict , data):
    tmp = []
    result = []

    for _ in list_of_lists:
        # Initialize tmp as a list of empty lists, one for each copy
        tmp = [[] for _ in range(num_of_copies)]


    for line in list_of_lists:
        for sequence in line:

            if sequence.startswith('Z'):
                listNormal = normalize( dict[sequence], num_of_copies)
                for j in range(num_of_copies):
                     tmp[j].append( data[listNormal[j]])
            else:
                for k in range(num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result



# Define a function to convert keys (lists) to strings for JSON serialization
def list_to_str(lst):
    return ', '.join(lst)


def dump_out_symbols(file_path , result , list_of_lines):
    my_dict = {}
    for line, res in zip(list_of_lines, result):
        my_dict[list_to_str(line)] = res
    try:
        # Attempt to open the file in 'x' mode (exclusive creation)
        with open(file_path, 'w') as f:
            json.dump(my_dict, f, indent=4)
        print(f"The simulation output (with symbols) is written to '{file_path}'")

    except FileExistsError:
        print(f"The file '{file_path}' already exists. Creation failed.")


def dump_out_sequences(file_path , result , list_of_lines):
    my_dict = {}
    for line, res in zip(list_of_lines, result):
        my_dict[list_to_str(line)] = res
    try:
        # Attempt to open the file in 'x' mode (exclusive creation)
        with open(file_path, 'w') as f:
            json.dump(my_dict, f, indent=4)
        print(f"The simulation output (with the whole sequences) is written to '{file_path}'")

    except FileExistsError:
        print(f"The file '{file_path}' already exists. Creation failed.")

