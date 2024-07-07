import numpy as np

""" 
    simulations - Project 2.0
    
    Generate a list with num_copies of the given element. Args: -
    element: The element to generate copies of. - num_copies: Number of copies to generate. Returns: - 
    List containing num_copies of the element. 
"""

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
    return copies


def clear_list(list , num_copies):
    tmp = []
    for _ in list:
        tmp = [[] for _ in range(num_copies)]
    return tmp

'''gets a list of the input lines , num of copies and the dict of alphabets 
    returns a list of list of lists that contains the shortmers
'''
def run(list_of_lines , num_of_copies , alphabet_dict , stats_dict):
    result = []
    for line in list_of_lines:
        tmp = clear_list(list_of_lines , num_of_copies)
        for sequence in line:
            if sequence.startswith('Z'):
                listNormal = normalize( alphabet_dict[sequence], num_of_copies)
                for j in range(num_of_copies):
                    update_stats(stats_dict, sequence, listNormal[j] , alphabet_dict)
                    tmp[j].append( listNormal[j])
            else:
                for k in range(num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result,stats_dict


'''gets a list of the input lines , num of copies and the dict of alphabets 
    returns a list of list of lists that contains the original alphabets
'''
def run_shortmers(list_of_lines , num_of_copies , alphabet_dict , data ):
    result = []
    for line in list_of_lines:
        tmp = clear_list(list_of_lines , num_of_copies)
        for sequence in line:
            if sequence.startswith('Z'):
                listNormal = normalize( alphabet_dict[sequence], num_of_copies)
                for j in range(num_of_copies):
                    tmp[j].append( data[listNormal[j]])
            else:
                for k in range(num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result


def update_stats(stats_dict, key, shortmer , alphabet_dict):
    if key in stats_dict:
        stats_dict[key][shortmer] += 1
    else:
        stats_dict.update({key:{value:0 for value in alphabet_dict[key]}})
        stats_dict[key][shortmer] += 1


