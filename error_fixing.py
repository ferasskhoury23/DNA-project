
'''
shortmers is a dictionary
cluster is a list of strings
'''
def function(cluster , shortmers , num_of_copies , strand_length , code_distance,seqma_length):
    distance_arr = compare_strand_lengths(cluster , strand_length , num_of_copies)
    shortmer_length = len(shortmers['X1'])

    dict_1 = {}
    dict_2 = {}
    fixed_cluster = cluster

    for i in range(strand_length-1):
            for j in range(num_of_copies):
                dict_1[cluster[i][j]]+=1
                dict_2[cluster[i][j+1]]+=1

            max_key1 = max(dict_1, key=dict_1.get)
            if (max_key1 < num_of_copies/2):
                fixed_cluster = fix_shortmer(fixed_cluster,shortmers,i,shortmer_length,num_of_copies,seqma_length)

            else:
                max_key2 = max(dict_2, key=dict_2.get)
                if (max_key2 < num_of_copies / 2):
                    fixed_cluster = fix_shortmer_plus_string(fixed_cluster, i, shortmer_length, num_of_copies)

                else:
                    # dict_1 is string
                    (fixed_cluster,distance_arr) = fix_string(fixed_cluster, i, num_of_copies,max_key1,max_key2,distance_arr)
                    i += 1,


    return fixed_cluster




def fix_string(fixed_cluster, index_to_fix, num_of_copies,max_key1,max_key2,distance_arr):
    for i in range(num_of_copies):
        if fixed_cluster[i][index_to_fix] == max_key1:
            continue
        else:
            if ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key1)):
                if ((index_to_fix + 2 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+2] == max_key2)):
                    #we detected insertion error , fix it
                    fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] +
                                                      fixed_cluster[i][index_to_fix + 1:])
                    distance_arr[i] -= 1
                else :
                    #TODO check what about this !!
                    pass
            elif ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key2)):
                #detected subsitution
                fixed_cluster[i][index_to_fix] = max_key1

            elif fixed_cluster[i][index_to_fix] == max_key2:
                #detected deletion
                fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
                distance_arr[i] += 1
            else:

                if distance_arr[i] > 0 and ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key1 )):

                    fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + fixed_cluster[i][index_to_fix + 1:])
                    distance_arr[i] -= 1


                else:
                     fixed_cluster[i][index_to_fix] = max_key1

    return fixed_cluster,distance_arr


def fix_shortmer(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length):
    dict_of_shortmers_in_segma = {}
    # Reversed dictionary
    strings_to_shortmers = {v: k for k, v in shortmers.items()} #reversed dict

    for i in range(num_of_copies):
        tmp = fixed_cluster[i][start_index : (start_index + shortmer_length)]
        if ( tmp in strings_to_shortmers):
            dict_of_shortmers_in_segma[strings_to_shortmers[tmp]]+=1

    segma = top_num_values(dict_of_shortmers_in_segma,seqma_length)
    for i in range(num_of_copies):
        tmp = fixed_cluster[i][start_index: (start_index + shortmer_length)]
        if tmp in segma:
            continue
        else:
            #TODO continue here

def top_num_values(my_dict,num):
    # Sort the dictionary items by value in descending order and take the top 3
    top_three = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:num]

    # Separate the keys and values into two lists
    keys = [item[0] for item in top_three]
    return keys

def _hamming_distance(seq1, seq2):
    """Calculate the Hamming distance between two sequences."""
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of the same length")
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


'''
for each cluster returns for each strand the distance from the original strrand_length
the goal is to identify if there is a deletion(and by how much) and if there is addition 
'''
def compare_strand_lengths(cluster , strand_length ,num_of_copies):
    result = []
    for i in range(num_of_copies):
        result[i]= strand_length - len(cluster[i])
    return result


