from typing import List

import numpy as np
from pkprint import ndtotext

INSERT_COST = 2
DELETE_COST = 2
REPLACE_COST = 1


def transform_word_dynamic_programming(wordFrom, wordTo, m, n) -> int:
    word_transfer_score_matrix = initialize_score_matrix(m, n)

    for i in range(m + 1):
        for j in range(n + 1):

            if i == 0:
                word_transfer_score_matrix[i][j] = j * INSERT_COST

            elif j == 0:
                word_transfer_score_matrix[i][j] = i * INSERT_COST

            elif wordFrom[i - 1] == wordTo[j - 1]:
                word_transfer_score_matrix[i][j] = word_transfer_score_matrix[i - 1][j - 1]

            else:
                update_score_matrix(i, j, word_transfer_score_matrix)

    return word_transfer_score_matrix[m][n], word_transfer_score_matrix


def initialize_score_matrix(m: int, n: int) -> List[List[int]]:
    word_transfer_score_matrix: List[List[int]] = [[0 for x in range(n + 1)] for x in range(m + 1)]
    return word_transfer_score_matrix


def update_score_matrix(i, j, word_transform_score_matrix):
    insert_cost = INSERT_COST + word_transform_score_matrix[i][j - 1]
    remove_cost = DELETE_COST + word_transform_score_matrix[i - 1][j]
    replacement_cost = REPLACE_COST + word_transform_score_matrix[i - 1][j - 1]
    min_cost = min(insert_cost, remove_cost, replacement_cost)
    word_transform_score_matrix[i][j] = min_cost


def transform_word_recursive(str1, str2, m, n) -> int:
    if m == 0:
        return n * INSERT_COST

    if n == 0:
        return m * INSERT_COST

    if str1[m - 1] == str2[n - 1]:
        return transform_word_recursive(str1, str2, m - 1, n - 1)

    return min(1 + transform_word_recursive(str1, str2, m, n - 1),  # INSERT
               1 + transform_word_recursive(str1, str2, m - 1, n),  # REMOVE
               2 + transform_word_recursive(str1, str2, m - 1, n - 1)  # REPLACE
               )


# Main Runline
wordOne = "AB"
wordTwo = "CDF"
# print (transformword_recursive(wordOne, wordTwo, len(wordOne), len(wordTwo)))
total_score, score_matrix = transform_word_dynamic_programming(wordOne, wordTwo, len(wordOne), len(wordTwo))
print(ndtotext(np.array(score_matrix)))
