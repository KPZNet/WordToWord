from typing import List
import numpy as np
from pkprint import ndtotext
from colorama import init, Fore, Back

INSERT_COST = 1
DELETE_COST = 1
REPLACE_COST = 2

INSERT_SYM = "I"
DELETE_SYM = "D"
REPLACE_SYM = "S"
NOCHANGE_SYM = "N"

TRACE_SYM = "*"

class Transfer:
    def __init__(self, _cost, _funct):
        self.cost = _cost
        self.funct = _funct


def transform_word_dynamic_programming(wordFrom, wordTo, m, n) :

    word_transfer_score_matrix = initialize_score_matrix ( m, n )
    word_transfer_trace_matrix = initialize_trace_matrix ( m, n )

    for k in range(len(wordTo)+1):
        word_transfer_score_matrix[0][k] = k * INSERT_COST
        word_transfer_trace_matrix[0][k] = INSERT_SYM
    for k in range(len(wordFrom)+1):
        word_transfer_score_matrix[k][0] = k * DELETE_COST
        word_transfer_trace_matrix[k][0] = DELETE_SYM

    word_transfer_trace_matrix[0][0] = NOCHANGE_SYM

    for i in range (1, m + 1) :
        for j in range (1, n + 1 ) :

            if wordFrom[i - 1] == wordTo[j - 1] :
                word_transfer_trace_matrix[i][j] = NOCHANGE_SYM
                word_transfer_score_matrix[i][j] = word_transfer_score_matrix[i - 1][j - 1]

            else:
                update_score_matrix ( i, j, word_transfer_score_matrix, word_transfer_trace_matrix )

    return word_transfer_score_matrix[m][n], word_transfer_score_matrix, word_transfer_trace_matrix

def update_score_matrix(i, j, word_transform_score_matrix, word_transform_trace_matrix) :
    insert_cost = Transfer(INSERT_COST + word_transform_score_matrix[i][j - 1], INSERT_SYM)
    remove_cost = Transfer(DELETE_COST + word_transform_score_matrix[i - 1][j], DELETE_SYM)
    replacement_cost = Transfer(REPLACE_COST + word_transform_score_matrix[i - 1][j - 1], REPLACE_SYM)
    li = [replacement_cost, insert_cost, remove_cost  ]
    min_cost = min ( li, key=lambda x : x.cost )
    word_transform_score_matrix[i][j] = min_cost.cost
    word_transform_trace_matrix[i][j] = min_cost.funct

def initialize_score_matrix(m: int, n: int) -> List[List[int]] :
    word_transfer_score_matrix: List[List[int]] = [[0 for x in range ( n + 1 )] for x in range ( m + 1 )]
    return word_transfer_score_matrix

def initialize_trace_matrix(m: int, n: int) -> List[List[str]] :
    word_transfer_trace_matrix: List[List[str]] = [[NOCHANGE_SYM for x in range ( n + 1 )] for x in range ( m + 1 )]
    return word_transfer_trace_matrix

def combined_score_trace_matrices(score, trace, m, n):
    combined_matrix = initialize_trace_matrix(m, n)
    for i in range(m+1):
        for j in range(n+1):
            sc_tr = trace[i][j] + ":" + str ( score[i][j] )
            combined_matrix[i][j] = sc_tr
    return combined_matrix


def min_cost_path(cost, operations, m, n) :

    row = m - 0
    col = n - 0

    while row > 0 and col > 0 :
        if cost[row - 1][col - 1] <= cost[row - 1][col] and cost[row - 1][col - 1] <= cost[row][col - 1] :
            operations[row - 1][col - 1] = operations[row - 1][col - 1] + TRACE_SYM
            row -= 1
            col -= 1
        elif cost[row - 1][col] <= cost[row - 1][col - 1] and cost[row - 1][col] <= cost[row][col - 1]:
            operations[row - 1][col] = operations[row - 1][col] + TRACE_SYM
            row -= 1
        else :
            operations[row][col - 1] = operations[row][col - 1] + TRACE_SYM
            col -= 1

    return operations


def transform_word_recursive(str1, str2, m, n) -> int :
    if m == 0 :
        return n * INSERT_COST

    if n == 0 :
        return m * INSERT_COST

    if str1[m - 1] == str2[n - 1] :
        return transform_word_recursive ( str1, str2, m - 1, n - 1 )

    return min ( 1 + transform_word_recursive ( str1, str2, m, n - 1 ),  # INSERT
                 1 + transform_word_recursive ( str1, str2, m - 1, n ),  # REMOVE
                 2 + transform_word_recursive ( str1, str2, m - 1, n - 1 )  # REPLACE
                 )


# Main Runline
init(autoreset = True)

wordOne = "hoccccccand"
wordTwo = "holand"
total_score_recursive = transform_word_recursive(wordOne, wordTwo, len(wordOne), len(wordTwo))
total_score, score_matrix, trace_matrix = transform_word_dynamic_programming ( wordOne, wordTwo, len ( wordOne ), len ( wordTwo ) )
combined = combined_score_trace_matrices(score_matrix, trace_matrix,len(wordOne), len(wordTwo))

combined = min_cost_path(score_matrix, combined,len(wordOne), len(wordTwo))

print (Fore.RED + Back.BLACK + 'some red text')

print ( ndtotext ( np.array ( score_matrix ) ) )
print ( ndtotext ( np.array ( trace_matrix ) ) )

print(wordOne)
print(wordTwo)
print ( ndtotext ( np.array ( combined ) ) )
