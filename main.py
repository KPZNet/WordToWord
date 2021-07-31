
import numpy as np
from pkprint import ndtotext

INSERT_COST = 2
DELETE_COST = 2
REPLACE_COST = 1


def WordTransformCost_DP(wordFrom, wordTo, m, n) ->int:

    wordTransferScoreMatrix = InitializeScoreMatrix(m, n)

    for i in range(m + 1):
        for j in range(n + 1):

            if i == 0:
                wordTransferScoreMatrix[i][j] = j * INSERT_COST

            elif j == 0:
                wordTransferScoreMatrix[i][j] = i * INSERT_COST

            elif wordFrom[i - 1] == wordTo[j - 1]:
                wordTransferScoreMatrix[i][j] = wordTransferScoreMatrix[i-1][j-1]

            else:
                UpdateScoreMatrix(i, j, wordTransferScoreMatrix)

    print(ndtotext(np.array ( wordTransferScoreMatrix )))
    return wordTransferScoreMatrix[m][n]

def InitializeScoreMatrix(m, n):
    wordTransferScoreMatrix = [[0 for x in range(n + 1)] for x in range(m + 1)]
    return wordTransferScoreMatrix

def UpdateScoreMatrix(i, j, wordTransferScoreMatrix):
    insert_cost = INSERT_COST + wordTransferScoreMatrix[i][j - 1]
    remove_cost = DELETE_COST + wordTransferScoreMatrix[i - 1][j]
    replacement_cost = REPLACE_COST + wordTransferScoreMatrix[i - 1][j - 1]
    min_cost = min(insert_cost, remove_cost, replacement_cost)
    wordTransferScoreMatrix[i][j] = min_cost


def WordTransformCost_Recursive(str1, str2, m, n) -> int:

    if m == 0:
        return n* INSERT_COST

    if n == 0:
        return m* INSERT_COST

    if str1[m-1] == str2[n-1]:
        return WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )

    return   min( 1 + WordTransformCost_Recursive( str1, str2, m, n - 1 ),  #INSERT
                  1 + WordTransformCost_Recursive( str1, str2, m - 1, n ),  #REMOVE
                  2 + WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )  #REPLACE
                  )

#Main Runline
wordOne = "AB"
wordTwo = "CDF"
print ( WordTransformCost_Recursive( wordOne, wordTwo, len( wordOne ), len( wordTwo ) ) )
print( WordTransformCost_DP( wordOne, wordTwo, len( wordOne ), len( wordTwo ) ) )