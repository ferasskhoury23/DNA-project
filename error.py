import random
import math
import numpy as np
"""
This Function returns a random DNA component that can be used to in the insertion or the substitution error
"""
def random_char():
    return random.choice('ACGT')

"""
This Function take a domain and a the number of random numbers that we want to generate and returns a list 
with the number of random numbers that we want to generate, where the size of the list is the number of random numbers
"""
def generate_random_numbers(count, start, end):
    return [random.randint(start, end) for _ in range(count)]

"""
This Function calculates how many error should we add to the original output(list of strings) based on the length of the list which is
affected by the strand's length and the size of the cluster, and also based on a random error type.
then we implement the errors on the certain cluster and return it
this function is for planting errors in scale of letters
"""
def sample_plant_errors(original_output, NumOfCopies, error_rate):
    outputWithErrors = original_output
    lengthOfStrand = len(original_output[0])
    length_sample = lengthOfStrand * NumOfCopies
    num_errors = math.floor(int(length_sample * error_rate))
    std_dev = num_errors * 0.2
    # Generate the number of errors with a normal distribution
    num_errors = int(np.random.normal(num_errors, std_dev))
    # Ensure the number of errors is not negative
    num_errors = max(0, num_errors)
    '''
    another way is to iterate the sequences letter by letter , and for each letter we  chose to plant error by 'throwing a coin'
    BUT we did it this - adding std-dev way to optimize the runtime
    '''
    randomErrorsIndexes = generate_random_numbers(num_errors, 0, length_sample - 1)
    for i in range(num_errors):
        strand_index = randomErrorsIndexes[i] // lengthOfStrand
        char_index = randomErrorsIndexes[i] % lengthOfStrand
        error_type = random.choice(['delete', 'insert', 'substitute'])

        if error_type == 'delete': #deletes a specific index and merges before and after it
            outputWithErrors[strand_index] = (outputWithErrors[strand_index][:char_index] +
                                              outputWithErrors[strand_index][char_index + 1:])
        elif error_type == 'insert': #insert in a random index
            outputWithErrors[strand_index] = (outputWithErrors[strand_index][:char_index] +
                                              random_char() +
                                              outputWithErrors[strand_index][char_index:])
        elif error_type == 'substitute':
            outputWithErrors[strand_index] = (outputWithErrors[strand_index][:char_index] +
                                              random_char() +
                                              outputWithErrors[strand_index][char_index + 1:])

    return outputWithErrors




"""
This Function is used to generate the whole error list. We will implement the errors per cluster.
result dict is a dict that each key is the barcode and each value is the simulation result string
"""
def plant_error(result_dict , num_of_copies , error_rate, shortmers_output ,input_shortmers, isShortmer = False):
    tmp_errors = {}
    if not isShortmer:
        for key in result_dict:
            tmp_errors[key] = sample_plant_errors(result_dict[key], num_of_copies, error_rate)
        return tmp_errors
    else:
        for key in shortmers_output:
            tmp_errors[key] = sample_plant_errors_shortmers(shortmers_output[key], num_of_copies , error_rate , input_shortmers)
        return tmp_errors






"""
This Function calculates how many error should we add to the original output based on the length of the list which is
affected by the strand's length and the size of the cluster, and also based on a random error type.
then we implement the errors on the certain cluster and return it
this function is for planting errors in scale of shortmers(X)

the input to this function - shortmers-output is a dict that each key is the barcode and each value is list of lists. see output_symbols.json for reference

"""
def sample_plant_errors_shortmers(shortmers_output, NumOfCopies, error_rate , input_shortmers):
    outputWithErrors = shortmers_output
    index_list = []

    for i, _str in enumerate(shortmers_output[0]):
        if _str.startswith("X"):
            index_list.append(i)

    num_of_X = len(index_list)

    num_of_X_in_cluster = num_of_X * NumOfCopies
    num_errors = math.floor(int(num_of_X_in_cluster * error_rate))
    std_dev = num_errors * 0.2
    # Generate the number of errors with a normal distribution
    num_errors = int(np.random.normal(num_errors, std_dev))
    # Ensure the number of errors is not negative
    num_errors = max(0, num_errors)

    '''
    another way is to iterate the sequences letter by letter , and for each letter we  chose to plant error by 'throwing a coin'
    BUT we did it this - adding std-dev way to optimize the runtime
    '''
    randomErrorsIndexes = generate_random_numbers(num_errors, 0, num_of_X_in_cluster - 1)

    for i in range(num_errors):
        strand_index = randomErrorsIndexes[i] // num_of_X  # in which copy we implement the error
        shortmer_index = index_list[randomErrorsIndexes[i] % num_of_X]
        error_type = random.choice(['delete', 'insert', 'substitute'])

        if error_type == 'delete': #deletes a specific index and merges before and after it
            outputWithErrors[strand_index].pop(shortmer_index)
        elif error_type == 'insert': #insert in a random index
            outputWithErrors[strand_index].insert(shortmer_index,random.choice(list(input_shortmers.keys()))) ## gets a random key from the shortmers input and inserts it to the list

        elif error_type == 'substitute':
            outputWithErrors[strand_index][shortmer_index] = random.choice(list(input_shortmers.keys()))
    return outputWithErrors







