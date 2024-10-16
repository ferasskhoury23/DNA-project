from collections import defaultdict

'''
shortmers is a dictionary
cluster is a list of strings
'''

def fix_main(cluster, shortmers , num_of_copies, strand_length, code_distance, seqma_length):
    distance_arr = compare_strand_lengths(cluster, strand_length, num_of_copies)
    shortmer_length = len(shortmers['X1'])
    string_rate = 0.7
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
            i+=1


        elif  ((dict_1[max_key1] > num_of_copies * string_rate) and (dict_2[max_key2] > num_of_copies * string_rate) ):
            (fixed_cluster, distance_arr) = fix_string(fixed_cluster, i, num_of_copies, max_key1, max_key2, distance_arr)
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
                    sum2 += numOfRep2[j] #TODO check indexes
            if (sum2 > sum1):
                #we assume that the first column is a string according to statistics
                (fixed_cluster, distance_arr) = fix_string(fixed_cluster, i, num_of_copies, max_key1, 'x',distance_arr)

                fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i+1, shortmer_length, num_of_copies, seqma_length)


                i += shortmer_length
                i+= 1
            else:
                fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)
                i += shortmer_length
            #TODO : add a boolean from fix_shortmer that is true when there is nothing to fix , then we increment (i) the window manually

        else:
            fixed_cluster = fix_shortmer(fixed_cluster, shortmers, i, shortmer_length, num_of_copies, seqma_length)
            i += shortmer_length

            #TODO : check if dic(max key) == numOfCopies , because then there is nothing to fix
            # we know that the first column- dict_1(from the two) is part of a string

    return fixed_cluster



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
    strings_to_shortmers = {v: k for k, v in shortmers.items()}  # reversed dict

    for i in range(num_of_copies):
        tmp = cluster[i][start_index: (start_index + shortmer_length)]
        if (tmp in strings_to_shortmers):
            dict_of_shortmers_in_segma[tmp] += 1

    segma,NumOfRepeat = top_num_values(dict_of_shortmers_in_segma, seqma_length)
    return segma,NumOfRepeat



def fix_shortmer(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length):
    segma,numofRepeat = find_dominant_segma(fixed_cluster,shortmers,start_index,shortmer_length,num_of_copies,seqma_length)
    print("--------------------------------------------")
    print(segma)
    for i in range(num_of_copies):

        if ((start_index + shortmer_length) >= len (fixed_cluster[i])):
            tmp = fixed_cluster[i][start_index: (start_index + shortmer_length)]
        else:
            tmp = fixed_cluster[i][start_index: (start_index + shortmer_length+1)]

        if tmp[0:shortmer_length] in segma:
            continue
        else:
            res = ''
            minChanges = len(tmp)
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


def transform_string(src, des):
    # Check if either string is empty
    if not des:
        return src  # If des is empty, return src as it is
    if not src:
        return des  # If src is empty, return des


    # If src already starts with des, return it unchanged
    if src.startswith(des):
        return src

    # Case 1: Insertion
    if len(des) > len(src):
        # Insert the first character of des at the start of src
        if (des[0] + src == des):
            return des
        else:
            return src
    for i in range(min(len(src), len(des))):
        if src[i] != des[i]:  # Characters differ
            modified_src = src[:i] + des[i] + src[i:]  # Substitute character
            if modified_src.startswith(des):
                return modified_src  # Return modified src if it matches des

    # Case 2: Deletion
        # Try deleting the first character of src
    if src[1:].startswith(des):
        return src[1:]  # If it starts with des after deleting the first character

    # Try deleting any character in src
    for i in range(len(src)):
        if (src[:i] + src[i + 1:]).startswith(des):
            return src[:i] + src[i + 1:]  # Return modified src after deletion

    # Case 3: Substitution
    # Check for substitution at the first differing character
    for i in range(min(len(src), len(des))):
        if src[i] != des[i]:  # Characters differ
            modified_src = src[:i] + des[i] + src[i + 1:]  # Substitute character
            if modified_src.startswith(des):
                return modified_src  # Return modified src if it matches des

    # If the last character of src can be substituted
    if len(src) > len(des):
        modified_src = src[:-1] + des[-1]  # Substitute last character
        if modified_src.startswith(des):
            return modified_src

    return src  # If no valid transformation can be made, return original src


def min_edit_distance_sw(s1, s2):
    len1, len2 = len(s1), len(s2)
    min_changes = max(len1 , len2)

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
returns two sorted lists , keys and values .
'''
def top_num_values(my_dict, num):
    # Sort the dictionary items by value in descending order and take the top <num>
    top = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:num]

    # Separate the keys and values into two lists
    keys = [item[0] for item in top]
    values = [item[1] for item in top]

    return keys, values



def fix_shortmer_plus_string(fixed_cluster, i, shortmer_length, num_of_copies):
    pass



"""Calculate the Hamming distance between two sequences."""
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


if __name__ == '__main__':
    source = "wzwyxxy"
    destination = "wzwzxx"
    str = transform_string(source, destination)

    print (str)

