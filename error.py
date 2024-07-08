import json
import random
import math

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
This Function calculates how many error should we add to the original output based on the length of the list which is
affected by the strand's length and the size of the cluster, and also based on a random error type.
then we implement the errors on the certain cluster and return it
"""
def sample_plant_errors(original_output, NumOfCopies, error_rate):
    outputWithErrors = original_output
    lengthOfStrand = len(original_output[0])
    length_sample = lengthOfStrand*NumOfCopies
    num_errors = math.floor(int(length_sample * error_rate))
    randomErrorsIndexes = generate_random_numbers(num_errors, 0, length_sample - 1)
    for i in range(num_errors):
        strand_index = randomErrorsIndexes[i] // lengthOfStrand
        char_index = randomErrorsIndexes[i] % lengthOfStrand
        error_type = random.choice(['delete', 'insert', 'substitute'])

        if error_type == 'delete':
            outputWithErrors[strand_index] = (outputWithErrors[strand_index][:char_index] +
                                              outputWithErrors[strand_index][char_index + 1:])
        elif error_type == 'insert':
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
"""
def plant_error(result_dict , num_of_copies , error_rate):
    tmp_errors = {}
    for key in result_dict:
        tmp_errors[key] = sample_plant_errors(result_dict[key], num_of_copies, error_rate)
    return tmp_errors


















