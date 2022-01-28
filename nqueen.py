#!/usr/bin/env python
# coding: utf-8

# Gerates a random board with 1 queen per row and column
def generate_board():
    pos_init = [1,2,3,4,5,6,7,8]
    random.shuffle(pos_init)
    print("New board generated: ", pos_init)
    return pos_init

# Counts the pairs of queens attacking each other on diagonals
def check_diagonals(arr):
    count = 0
    
    for i in range(len(arr)):
        for j in range(1, len(arr) - i):
            if(arr[i+j] == arr[i] + j):
                count += 1
            if(arr[i+j] == arr[i] - j):
                count += 1
    return count

# Counts the pairs of queens attacking each other on rows
def check_rows(arr):
    count = 0
    
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if(arr[i] == arr[j]):
                count += 1
    return count

# Returns total pairs of attacking queens (h-value)
def check_attacking(arr):
    return (check_diagonals(arr) + check_rows(arr))

# Handles placing recursive calls on the stack
def hill_climb(arr):
    # if check_attacking(arr) is 0, arr is the answer
    # call function list_boards to return list of all boards with lowest h_val, as well as that h-val
    # recursive call on hill_climb for each element in list. Recursive call fails if lower h-val is not found (this prunes the tree)
    
    prev_h_val = check_attacking(arr)
    
    if(prev_h_val == 0):
        out = []
        for i in arr:
            if i not in out:
                out.append(i)
        print(out)
        return
        
    best_boards, h_val = list_boards(arr, prev_h_val)
    
    if(h_val < prev_h_val):
        for i in best_boards:
            hill_climb(i)
    else:
        return

# Calculates all 1-moves, the h-value for that move, then returns list of lowest h_vals boards, as well as h-val
def list_boards(arr, best_h_value):
    best_h_board_list = []
    for i in range(len(arr)): # iterating through rows
        hill_climb_arr = arr.copy()
        for j in range(len(arr)): # moving the element to the jth pos
            hill_climb_arr[i] = j+1
            curr_h_value = check_attacking(hill_climb_arr)

            if(hill_climb_arr[i] != arr[i]):
                temp_copy = hill_climb_arr.copy()
                if(curr_h_value == best_h_value):
                    best_h_board_list.append(temp_copy)
                if(curr_h_value < best_h_value):
                    best_h_board_list = [temp_copy]
                    best_h_value = curr_h_value
    
    return best_h_board_list, best_h_value

import random
import sys

sys.setrecursionlimit(2500)
test_arr = [1,2,3,4,5,6,7,8]
test_arr2 = [4,3,2,5,4,3,2,3]
test_arr3 = [1,6,2,5,7,4,8,3]
test_arr4 = [7,4,2,5,8,1,2,5]
test_arr5 = generate_board()

print("Test array: ", test_arr5)
print("Answer: ")
hill_climb(test_arr5)




