# This file contains some functions that allow the calculation of Levenshtein distance using the dynamic programming algorithm presented in Jurafsky and Martin 3rd ed.

import numpy as np

insert_cost = 1
delete_cost = 1
substitute_cost = 1

def edit_distance_matrix(src, tgt):
    source_length = len(src)
    target_length = len(tgt)
    # Fill matrix with -1's to indicate unvisited entries.
    matrix = np.full((source_length + 1, target_length + 1, 2), -1)
    # Visit first row and first column.
    for i in range(source_length + 1):
        matrix[i,0,0] = i
        matrix[i,0,1] = 1 # Indicates pointing only up (i.e. deletion)
    for j in range(target_length + 1):
        matrix[0,j,0] = j
        matrix[0,j,1] = 2 # Indicates pointing only right (i.e. insertion)
    # Visit the rest of the table
    for i in range(1, source_length + 1):
        for j in range(1, target_length + 1):
            pointers = 0
            cost_with_insertion = matrix[i,j-1,0] + insert_cost
            cost_with_deletion = matrix[i-1,j,0] + delete_cost
            if src[i-1] != tgt[j-1]: # Subtracting 1 since we have an extra row and column in our matrix for the empty string
                cost_with_substitution = matrix[i-1,j-1,0] + substitute_cost
            else:
                cost_with_substitution = matrix[i-1,j-1,0] + 0
            # Set pointers value and total cost value.
            if cost_with_deletion <= cost_with_substitution and cost_with_deletion <= cost_with_insertion:
                pointers += 1
                total_cost = cost_with_deletion
            if cost_with_insertion <= cost_with_deletion and cost_with_insertion <= cost_with_substitution:
                pointers += 2
                total_cost = cost_with_insertion
            if cost_with_substitution <= cost_with_insertion and cost_with_substitution <= cost_with_deletion:
                pointers += 4
                total_cost = cost_with_substitution
            matrix[i,j,0] = total_cost
            matrix[i,j,1] = pointers
    return matrix

def edit_distance(src,tgt):
    matrix = edit_distance_matrix(src,tgt)
    return(matrix[matrix.shape[0]-1,matrix.shape[1]-1,0])

def align(src, tgt):
    matrix = edit_distance_matrix(src,tgt)
    i = matrix.shape[0] - 1
    j = matrix.shape[1] - 1
    l = [(i,j,-1)] # set the third dimension to -1 to signal that this is the last step in the trace below
    while i > 0 or j > 0:
        if matrix[i,j,1] >= 4:
            i -= 1
            j -= 1
            l.append((i,j,4))
        elif matrix[i,j,1] >= 2:
            j -= 1
            l.append((i,j,2))
        else:
            i -= 1
            l.append((i,j,1))
    l.reverse()
    result = []
    i = 0
    pointer = 0
    current = list(src)
    for entry in l:
        result.append(''.join(current))
        if entry[2] == 4: # if substitution
            current[pointer] = tgt[pointer]
            pointer += 1
        elif entry[2] == 2: # insertion
            current.insert(pointer, tgt[pointer])
            pointer += 1
        elif entry[2] == -1: # done
            return result
        else: # deletion
            current.pop(pointer)

import sys
    
source = sys.argv[1]
target = sys.argv[2]
print("Distance: " + str(edit_distance(source, target)))
print(align(source, target))
