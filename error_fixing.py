from collections import defaultdict
import numpy as np

"""    
Error Fixing - Final Version
"""


'''
Shortmers is a dictionary
Cluster is a list of strings
'''

'''
iterate over each cluster and call fix_main for each one
'''
def fix_clusters(error_dict, strand_length_dict, shortmers, num_of_copies, seqma_length,alphabets_dict):
    result = {}
    result_strand = {}
    for key, cluster in error_dict.items():
        result[key],result_strand[key] = fix_main(cluster, shortmers, num_of_copies, strand_length_dict[key], seqma_length , alphabets_dict)

    return result,result_strand


'''
main fixing errors function , it detects what type strand we are scanning ( shortmer or sequence) 
and calls the relevant fixing function
'''
def fix_main(cluster, shortmers , num_of_copies, strand_length, seqma_length , alphabets_dict):
    result_strand = str()
    distance_arr = compare_strand_lengths(cluster, strand_length, num_of_copies)
    shortmer_length = len(shortmers['X1'])
    string_rate = 0.6
    #if we dont use .copy() - shallow copy. they will have the same reference in memory
    fixed_cluster = cluster

    #This will automatically handle the case where the key does not yet exist in the dictionary
    # by initializing it to 0 and then incrementing it.
    dict_1 = defaultdict(int)
    dict_2 = defaultdict(int)

    #TODO : we can improve prformance by saving the [j+1] we compute it twice in a row
    i = 0
    while i < strand_length:
        dict_1.clear()
        dict_2.clear()
        for j in range(num_of_copies):
            if len(cluster[j]) > i :
                dict_1[cluster[j][i]] +=1
            if len(cluster[j]) > i+1:
                dict_2[cluster[j][i+1]] +=1

        #find the key that has the maximum value associated with it.
        max_key1 = max(dict_1, key=dict_1.get)
        if (dict_2):
            max_key2 = max(dict_2, key=dict_2.get)
        else:
            max_key2 = 'x'

        if (i > (strand_length-shortmer_length)):
            (fixed_cluster, distance_arr) = fix_string(fixed_cluster, i, num_of_copies, max_key1, 'x', distance_arr)
            result_strand += max_key1
            i+=1


        elif  ((dict_1[max_key1] > num_of_copies * string_rate) and (dict_2[max_key2] > num_of_copies * string_rate) ):
            (fixed_cluster, distance_arr) = fix_string(fixed_cluster, i, num_of_copies, max_key1, max_key2, distance_arr)
            result_strand += max_key1

            i+=1


        elif (dict_1[max_key1] > num_of_copies * string_rate):
            (segma1, numOfRep1) = find_dominant_segma(cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)
            (segma2, numOfRep2) = find_dominant_segma(cluster, shortmers, i+1, shortmer_length, num_of_copies, seqma_length)
            sum1 = 0
            sum2 = 0
            for j in range(seqma_length):
                if(j < len(numOfRep1)):
                    sum1 += numOfRep1[j]
                if (j < len(numOfRep2)):
                    sum2 += numOfRep2[j]
            if (sum2 > sum1):
                #we assume that the first column is a string according to statistics
                (fixed_cluster, distance_arr) = fix_string(fixed_cluster, i, num_of_copies, max_key1, 'x',distance_arr)
                result_strand += max_key1
                result_strand += ','
                fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i+1, shortmer_length, num_of_copies, seqma_length)
                result_strand += calculate_segma(segma2, shortmers , alphabets_dict)
                result_strand += ','


                i += shortmer_length
                i+= 1
            else:
                if result_strand and (not result_strand.endswith(',')):
                    result_strand += ','

                fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)
                (segma1, numOfRep1) = find_dominant_segma(cluster, shortmers, i, shortmer_length, num_of_copies,
                                                          seqma_length)
                result_strand += calculate_segma(segma1, shortmers , alphabets_dict)
                result_strand += ','

                i += shortmer_length
            #TODO : add a boolean from fix_shortmer that is true when there is nothing to fix , then we increment (i) the window manually

        else:
            if  result_strand and (not result_strand.endswith(',')):
                result_strand += ','

            fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)
            (segma1, numOfRep1) = find_dominant_segma(cluster, shortmers, i, shortmer_length, num_of_copies,
                                                      seqma_length)

            result_strand += calculate_segma(segma1, shortmers, alphabets_dict)
            result_strand += ','

            i += shortmer_length

            #TODO : check if dic(max key) == numOfCopies , because then there is nothing to fix
            # we know that the first column- dict_1(from the two) is part of a string

    return fixed_cluster, result_strand


def fix_string(fixed_cluster, index_to_fix, num_of_copies, max_key1, max_key2 , distance_arr):
    for i in range(num_of_copies):
        if (len (fixed_cluster[i]) > index_to_fix) and  fixed_cluster[i][index_to_fix] == max_key1:
            continue
        else:
            if (len (fixed_cluster[i]) <= index_to_fix):
                fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
            elif ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key1)
                    and (index_to_fix + 2 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+2] == max_key2)):
                #detected insertion

                fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + fixed_cluster[i][index_to_fix + 1:])
                distance_arr[i] -= 1

            elif ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key2)):
                #detected subsitution

                #convert the string at fixed_cluster[i] to a list of characters
                sequence_list = list(fixed_cluster[i])
                #modify the list at the specific index
                sequence_list[index_to_fix] = max_key1
                #join the list back into a string
                fixed_cluster[i] = ''.join(sequence_list)

            elif fixed_cluster[i][index_to_fix] == max_key2:
                #detected deletion
                fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
                distance_arr[i] += 1
            else:
                if distance_arr[i] > 0 and ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key1 )):
                    #insertion
                    fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + fixed_cluster[i][index_to_fix + 1:])
                    distance_arr[i] -= 1


                elif(distance_arr[i] == 0):
                    #subsitution
                    sequence_list = list(fixed_cluster[i])
                    # Modify the list at the specific index
                    sequence_list[index_to_fix] = max_key1
                    # Join the list back into a string
                    fixed_cluster[i] = ''.join(sequence_list)
                else:
                    #deletion
                    fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
                    distance_arr[i] += 1

    return fixed_cluster, distance_arr


def find_dominant_segma(cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length):
    dict_of_shortmers_in_segma = defaultdict(int)
    # Reversed dictionary
    strings_to_shortmers = {v: k for k, v in shortmers.items()}  # reversed dict   CCG : X5

    for i in range(num_of_copies):
        tmp = cluster[i][start_index: (start_index + shortmer_length)]
        if (tmp in strings_to_shortmers):
            dict_of_shortmers_in_segma[tmp] += 1

    segma,NumOfRepeat = top_num_values(dict_of_shortmers_in_segma, seqma_length)
    return segma,NumOfRepeat


def compare_lists(list1, list2):
    if( (set(list1) == set(list2)) or ( (len(list1) < len(list2)) and (list1 in list2) ) ):
        return True
    return False

def calculate_segma(string_segma_list, shortmers_dict , alphabets_dict):
    shortmersX_list =[]
    strings_to_shortmers = {v: k for k, v in shortmers_dict.items()}  # reversed dict   CCG : X5
    #convert the segma string list to segma list with X's
    for string in string_segma_list:
        shortmersX_list.append(strings_to_shortmers[string])
    for segma,segma_list in alphabets_dict.items():
        if (compare_lists(shortmersX_list, segma_list)):
            return segma
    return 'ZINVALID'

def fix_shortmer(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length):
    segma,numofRepeat = find_dominant_segma(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length)
    for i in range(num_of_copies):

        if ((start_index + shortmer_length) >= len (fixed_cluster[i])):
            tmp = fixed_cluster[i][start_index: (start_index + shortmer_length)]
        else:
            tmp = fixed_cluster[i][start_index: (start_index + shortmer_length+1)]

        if tmp[0:shortmer_length] in segma:
            continue
        else:
            for s2 in segma:
                x = transform_string(tmp,s2)
                if (x != tmp):
                    w = fixed_cluster[i][:start_index]
                    if ((start_index + shortmer_length) >= len(fixed_cluster[i])):
                        fixed_cluster[i] = (w + x)
                    else:
                        y = fixed_cluster[i][start_index + shortmer_length + 1:]
                        fixed_cluster[i] = (w + x + y)
                    break


    return fixed_cluster


'''gets src and dest strings , changes the src string according to the errors- subsitution , deletion , insertion . 
until we get that the start of src string is equal to dest.
We assume that there is maximum one error in the src string.
if we cant get the dest from src with only one error , we return the original src'''
def transform_string(src, des):
    if not des:
        return src
    if not src:
        return des

    if src.startswith(des):
        return src

    #insertion
    if len(des) > len(src):
        #insert the first character of des at the start of src
        if (des[0] + src == des):
            return des
        else:
            return src
    for i in range(min(len(src), len(des))):
        if src[i] != des[i]:  # Characters differ
            modified_src = src[:i] + des[i] + src[i:]  # Substitute character
            if modified_src.startswith(des):
                return modified_src  # Return modified src if it matches des

    #Deletion
    #try deleting the first character
    if src[1:].startswith(des):
        return src[1:]

    #try deleting any character in src
    for i in range(len(src)):
        if (src[:i] + src[i + 1:]).startswith(des):
            return src[:i] + src[i + 1:]

    #Substitution
    #check substitution at the first differing character
    for i in range(min(len(src), len(des))):
        if src[i] != des[i]:
            modified_src = src[:i] + des[i] + src[i + 1:]
            if modified_src.startswith(des):
                return modified_src

    #if the last character of src can be substituted
    if len(src) > len(des):
        modified_src = src[:-1] + des[-1]
        if modified_src.startswith(des):
            return modified_src

    #if no valid transformation can be made, return original src
    return src


'''
top repetitive shortmers in a segma
returns two sorted lists , keys and values .
'''
def top_num_values(my_dict, num):
    #sort the dictionary items by value in descending order and take the top <num>
    top = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:num]
    #separate the keys and values into two lists
    keys = [item[0] for item in top]
    values = [item[1] for item in top]

    return keys, values


"""
Calculate the Hamming distance between two sequences.
"""
def _hamming_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of the same length")
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


'''
for each cluster returns for each strand the distance from the original strand_length
the goal is to identify if there is a deletion(and by how much) and if there is addition 
'''
def compare_strand_lengths(cluster, strand_length, num_of_copies):
    """Calculate the distance of each sequence from the expected strand length."""
    distance_arr = []
    for i in range(num_of_copies):
        distance = len(cluster[i]) - strand_length
        distance_arr.append(distance)
    return distance_arr



'''
 Computes the Levenshtein distance by using dynamic programming to fill out a matrix.
'''
def levenshtein_distance(seq1, seq2):
    # Create a distance matrix
    len_seq1, len_seq2 = len(seq1), len(seq2)
    matrix = np.zeros((len_seq1 + 1, len_seq2 + 1))

    # Initialize the matrix
    for i in range(len_seq1 + 1):
        matrix[i][0] = i
    for j in range(len_seq2 + 1):
        matrix[0][j] = j

    # Fill the matrix
    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,  # deletion
                               matrix[i][j - 1] + 1,  # insertion
                               matrix[i - 1][j - 1] + cost)  # substitution

    return matrix[len_seq1][len_seq2]


'''
Calculates the similarity percentage based on the Levenshtein distance and the length of the sequences.
'''
def levenshtein_similarity(seq1, seq2):
    distance = levenshtein_distance(seq1, seq2)
    max_len = max(len(seq1), len(seq2))
    similarity_percentage = (1 - distance / max_len) * 100
    return similarity_percentage


'''
calculate and return the success rate according to Levenshtein distance
'''
def calculate_sucess_rate(final_result, original):
    sum = 0
    total_length = 0
    for key , value in final_result.items():
        for i in range(len(value)):
            sum += levenshtein_similarity(final_result[key][i], original[key][i])
        total_length += len(value)

    return (sum/total_length)
