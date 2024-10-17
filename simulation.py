import numpy as np


""" 
    simulations - Final Version
    
    Generate a list with num_copies of the given element. Args: -
    element: The element to generate copies of. - num_copies: Number of copies to generate. Returns: - 
    List containing num_copies of the element. 
"""


'''
    gets our input data and returns :
    list of list of lists that contains the simulated output but only with shortmers symbols
'''
def run(InputAnalyze,stats_dict):
    result = []
    for line in InputAnalyze.list_of_lines:
        tmp = clear_list(InputAnalyze.list_of_lines , InputAnalyze.num_of_copies)
        for sequence in line:
            if sequence.startswith('Z'):
                listNormal = normalize( InputAnalyze.alphabet_dict[sequence], InputAnalyze.num_of_copies , 'uniform')
                for j in range(InputAnalyze.num_of_copies):
                    update_stats(stats_dict, sequence, listNormal[j] , InputAnalyze.alphabet_dict)
                    tmp[j].append( listNormal[j])
            else:
                for k in range(InputAnalyze.num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result,stats_dict

'''
gets our input data and returns :
a list of list of lists that contains the simulated output but with the whole sequences
'''
def run_shortmers(InputAnalyze):
    result = []
    for line in InputAnalyze.list_of_lines:
        tmp = clear_list(InputAnalyze.list_of_lines , InputAnalyze.num_of_copies)
        for sequence in line:
            if sequence.startswith('Z'):
                listNormal = normalize( InputAnalyze.alphabet_dict[sequence], InputAnalyze.num_of_copies , 'uniform')
                for j in range(InputAnalyze.num_of_copies):
                    tmp[j].append( InputAnalyze.shortmers_dict[listNormal[j]])
            else:
                for k in range(InputAnalyze.num_of_copies):
                    tmp[k].append(sequence)
        result.append(tmp)
    return result



def generate_copies(sequence, num_copies):
    return [sequence] * num_copies



'''
generates shortmers from the list o shorters  ,each shortmer is taken  on normalized probability
'''
'''def normalize(list_of_shortmers, num_of_copies): # add another option - uniform
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
'''
def normalize(list_of_shortmers, num_of_copies, distribution_type='normal'):
    mean = 0.3
    std_dev = 0.1

    if distribution_type == 'normal':
        # Generate "num_of_copies" normally distributed values
        values = np.random.normal(mean, std_dev, num_of_copies)
    elif distribution_type == 'uniform':
        # Generate "num_of_copies" uniformly distributed values
        values = np.random.uniform(0, len(list_of_shortmers)  , num_of_copies).astype(int)
        copies = [list_of_shortmers[i] for i in values]
        return copies
    else:
        raise ValueError("Unsupported distribution type. Use 'normal' or 'uniform'.")

    # Normalize the values to map to the 3 items
    normalized_indices = (values - values.min()) / (values.max() - values.min())
    mapped_indices = (normalized_indices * (len(list_of_shortmers) - 1)).astype(int)

    # Create the "num_of_copies" copies
    copies = [list_of_shortmers[i] for i in mapped_indices]
    return copies


def clear_list(list , num_copies):
    tmp = []
    for _ in list:
        tmp = [[] for _ in range(num_copies)]
    return tmp


def update_stats(stats_dict, key, shortmer , alphabet_dict):
    if key in stats_dict:
        stats_dict[key][shortmer] += 1
    else:
        stats_dict.update({key:{value:0 for value in alphabet_dict[key]}})
        stats_dict[key][shortmer] += 1

