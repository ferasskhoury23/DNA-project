
'''
shortmers is a dictionary
cluster is a list of strings
'''
from collections import defaultdict


def fix_main(cluster , shortmers , num_of_copies , strand_length , code_distance,seqma_length):
    distance_arr = compare_strand_lengths(cluster , strand_length , num_of_copies)
    shortmer_length = len(shortmers['X1'])

    #if we dont use .copy() - shallow copy. they will have the same reference in memory
    fixed_cluster = cluster

    #This will automatically handle the case where the key does not yet exist in the dictionary
    # by initializing it to 0 and then incrementing it.
    dict_1 = defaultdict(int)
    dict_2 = defaultdict(int)

    #TODO : we can improve prformance by saving the [j+1] we compute it twice in a row
    for i in range(strand_length-1):
        dict_1.clear()
        dict_2.clear()
        for j in range(num_of_copies):
            if len(cluster[j]) > i+1 :
                dict_1[cluster[j][i]] +=1
                dict_2[cluster[j][i+1]] +=1

        #find the key that has the maximum value associated with it.
        max_key1 = max(dict_1, key=dict_1.get)

        if (dict_1[max_key1] < num_of_copies*0.7):
            fixed_cluster = fix_shortmer(fixed_cluster,shortmers,i,shortmer_length,num_of_copies,seqma_length)
            #TODO : add a boolean from fix_shortmer that is true when there is nothing to fix , then we increment (i) the window manually
        else:
            max_key2 = max(dict_2, key=dict_2.get)
            if (dict_2[max_key2] < num_of_copies / 2):
                #fixed_cluster = fix_shortmer_plus_string(fixed_cluster, i, shortmer_length, num_of_copies)
                fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)


            else:
                #TODO : check if dic(max key) == numOfCopies , because then there is nothing to fix
                # we know that the first column- dict_1(from the two) is part of a string
                (fixed_cluster,distance_arr) = fix_string(fixed_cluster, i, num_of_copies,max_key1,max_key2,distance_arr)
                i += 1
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
                # Convert the string at fixed_cluster[i] to a list of characters
                sequence_list = list(fixed_cluster[i])
                # Modify the list at the specific index
                sequence_list[index_to_fix] = max_key1
                # Join the list back into a string
                fixed_cluster[i] = ''.join(sequence_list)

            elif fixed_cluster[i][index_to_fix] == max_key2:
                #detected deletion
                fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
                distance_arr[i] += 1
            else:

                if distance_arr[i] > 0 and ((index_to_fix + 1 < len(fixed_cluster[i])) and (fixed_cluster[i][index_to_fix+1] == max_key1 )):

                    fixed_cluster[i] = (fixed_cluster[i][:index_to_fix] + fixed_cluster[i][index_to_fix + 1:])
                    distance_arr[i] -= 1


                else:
                    if (distance_arr[i] == 0):
                        sequence_list = list(fixed_cluster[i])
                        # Modify the list at the specific index
                        sequence_list[index_to_fix] = max_key1
                        # Join the list back into a string
                        fixed_cluster[i] = ''.join(sequence_list)
                    else:
                        fixed_cluster[i] = (
                                    fixed_cluster[i][:index_to_fix] + max_key1 + fixed_cluster[i][index_to_fix + 1:])
                        distance_arr[i] += 1




    return fixed_cluster,distance_arr


def fix_shortmer(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length):
    dict_of_shortmers_in_segma = defaultdict(int)
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
            res = ''
            minChanges = len(tmp)
            for s2 in segma:
                x = min_edit_distance_sw(tmp,s2)
                if (minChanges>x):
                    res = s2
                minChanges = min(x,minChanges)

            fixed_cluster[i] = (fixed_cluster[i][:start_index] + res + fixed_cluster[i][start_index +shortmer_length + 1:])
    return fixed_cluster

def min_edit_distance_sw(s1, s2):
    len1, len2 = len(s1), len(s2)
    min_changes = float('inf')

    # If s2 is longer, we need to pad s1 or return the len2 if s1 is empty
    if len1 < len2:
        return len2

    # Slide a window of length len2 across s1
    for i in range(len1 - len2 + 1):
        current_changes = 0
        window = s1[i:i + len2]

        # Calculate changes for the current window
        for j in range(len2):
            if window[j] != s2[j]:
                current_changes += 1

        # Update the minimum number of changes
            min_changes = min(min_changes, current_changes)

        # If len1 > len2, account for the extra characters in s1
            min_changes += len1 - len2

            return min_changes

'''
top repetitive shortmers in a segma
'''
def top_num_values(my_dict,num):
    # Sort the dictionary items by value in descending order and take the top <num>
    top = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:num]

    keys = [item[0] for item in top]
    return keys



def fix_shortmer_plus_string(fixed_cluster, i, shortmer_length, num_of_copies):
    pass




def _hamming_distance(seq1, seq2):
    """Calculate the Hamming distance between two sequences."""
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of the same length")
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


'''
for each cluster returns for each strand the distance from the original strrand_length
the goal is to identify if there is a deletion(and by how much) and if there is addition 
'''
def compare_strand_lengths(cluster, strand_length, num_of_copies):
    """Calculate the distance of each sequence from the expected strand length."""
    distance_arr = []
    for i in range(num_of_copies):
        distance = abs(len(cluster[i]) - strand_length)
        distance_arr.append(distance)
    return distance_arr

if __name__ == '__main__':
    cluster = [
        "AATACTTCTCCGGAGTGATAACCTCTACGTCCTGGGAG",
        "TTCACTTCTCCGGAGTGATGAACAGCACGTCCTAATGG",
        "CCGACTTCTCCGGAGTGATGAACCTAACGTTCCGCCAT",
        "GGACTTCTCCGGAGTGATGAACTCTACGTCCTGGATG",
        "AATACTACTCCGGAGTGATGAACCCGACGTCCACACCG",
        "GGTACTTCTCCGGGATGATGAACCCCGACGTCCTGTGACA",
        "AATACTTCTCCGGAGTGATGAAGTCACGTCCCACTGG",
        "AATACCTTCTCCGGAGTGATGAACCCGACGTCCACAACA",
        "GGAACTTCTCCGGAGTGATGAACAGCACGTCCTAACCG",
        "AATACTTCTCCGGAGTGATGAACCCGACGTCCCACGAG",
        "GCGACTTCTCGGAGTGATGAACAGAGGTCCTAAATG",
        "CCGACTTCTCCGGAGTGATGAACGCCACGTCCACACCG",
        "CCGACTTCTCCGGGTGATTGAACTCTACTTCCGCCACA",
        "GAGACTTCTCCGGAGTGATGAACCTAACGTCCTGGCA"
    ]
