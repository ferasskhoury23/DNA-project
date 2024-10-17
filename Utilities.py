import random

"""    
Utilities - Final Version
"""

'''
Helps finding the original strand length.
'''
def helper(dict):
    result = {}
    for key, value in dict.items():
        result[key] = len(dict[key][0])
    return result


"""
For a function that provides a number based on a maximum, minimum, mean, and deviation, 
you could be referring to a random number generator that follows a specific distribution,
such as a normal (Gaussian) distribution
"""
def pick_number(min, max):
    mean = (min + max) / 2
    std_dev = (max - mean) / 2
    while True:
        number = random.gauss(mean, std_dev)
        if min <= number <= max:
            return round(number)

'''
This function takes initial parameters to start the stimulation generator
'''
def parameters_from_input():
    print("Please enter minimum and maximum values for picking The number of copies :")
    print("Min value : ")
    min_input_value = int(input())
    print("Max value : ")
    max_input_value = int(input())
    if ((min_input_value < 0) or (max_input_value < 0) or (max_input_value < min_input_value)):
        raise ValueError("Invalid Inputs")

    num_of_copies = pick_number(min_input_value, max_input_value)
    print("number of copies is :", num_of_copies)
    print("-----------------------------------------------------------------------------------------------------------")
    print("Please enter error_rate between 0 and 0.05")
    error_rate = float(input())
    if ((error_rate > 0.05) or (error_rate < 0)):
        raise ValueError("Error Rate Invalid")

    return num_of_copies, error_rate

def is_sublist(small, big):
    """Helper function to check if `small` list is a sublist of `big`."""
    for i in range(len(big) - len(small) + 1):
        if big[i:i+len(small)] == small:
            return True
    return False

def find_longest_key_with_sublist(target_list, dict_of_lists):
    longest_match = []
    longest_key = None

    for key, lst in dict_of_lists.items():
        # Check if the current list contains the entire target list
        if is_sublist(target_list, lst):
            return key  # Return the key immediately if we find a perfect match

        # Find the longest matching sublist
        for i in range(len(lst)):
            for j in range(i + 1, len(lst) + 1):
                sublist = lst[i:j]
                if len(sublist) > len(longest_match) and is_sublist(sublist, target_list):
                    longest_match = sublist
                    longest_key = key

    return longest_key if longest_key else None
