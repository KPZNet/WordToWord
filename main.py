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

TRACE_SYM_END = ")"
TRACE_SYM_START = "("

class Transfer:
    def __init__(self, _cost, _funct):
        self.cost = _cost
        self.funct = _funct

def transform_word_dynamic_programming(wordFrom, wordTo) :
    m = len(wordOne)
    n = len(wordTwo)
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
            sc_tr = " " + trace[i][j] + ":" + str ( score[i][j] )
            combined_matrix[i][j] = sc_tr
    return combined_matrix


def min_cost_path(cost, operations, m, n) :

    row = m - 0
    col = n - 0

    while row > 0 and col > 0 :
        if cost[row - 1][col - 1] <= cost[row - 1][col] and cost[row - 1][col - 1] <= cost[row][col - 1] :
            operations[row - 1][col - 1] = TRACE_SYM_START+ operations[row - 1][col - 1].strip() +TRACE_SYM_END
            row -= 1
            col -= 1
        elif cost[row - 1][col] <= cost[row - 1][col - 1] and cost[row - 1][col] <= cost[row][col - 1]:
            operations[row - 1][col] = TRACE_SYM_START+ operations[row - 1][col].strip() + TRACE_SYM_END
            row -= 1
        else :
            operations[row][col - 1] = TRACE_SYM_START+ operations[row][col - 1].strip() + TRACE_SYM_END
            col -= 1

    return operations


# Main Runline
init(autoreset = True)

wordOne = "hoccccccand"
wordTwo = "holand"
print("-----------------------")
print("Word From: " + wordOne)
print("Word To: " + wordTwo)
total_score, score_matrix, trace_matrix = transform_word_dynamic_programming ( wordOne, wordTwo )
combined_matrix = combined_score_trace_matrices(score_matrix, trace_matrix, len(wordOne), len(wordTwo))

combined_matrix = min_cost_path(score_matrix, combined_matrix, len(wordOne), len(wordTwo))

print("Score Matrix:")
print ( ndtotext ( np.array ( score_matrix ) ) )
print("Operations Matrix:")
print ( ndtotext ( np.array ( trace_matrix ) ) )

print(Fore.MAGENTA + "Conversion Cost: {0}".format(total_score))
print("Trace Path")
print(ndtotext (np.array (combined_matrix)))
