from typing import List
import numpy as np
from pkprint import ndtotext
from colorama import init, Fore, Back

#constants for cost formula
INSERT_COST = 20
DELETE_COST = 20
REPLACE_COST = 5

#symbols used to keep track of operations
INSERT_SYM = "I"
DELETE_SYM = "D"
REPLACE_SYM = "S"
NOCHANGE_SYM = "N"

#convenient print characters
TRACE_SYM_END = ")"
TRACE_SYM_START = "("

#class used to keep track of minimal operation for each sub string
class Transfer:
    def __init__(self, _cost, _funct):
        self.cost = _cost
        self.funct = _funct

#Main function to convert "Word A" to "Word B"
def transform_word_dynamic_programming(wordFrom, wordTo) :
    #get word lengths
    m = len(wordOne)
    n = len(wordTwo)
    #initialize score matrix and operation matrix
    word_transfer_score_matrix = initialize_score_matrix ( m, n )
    word_transfer_trace_matrix = initialize_trace_matrix ( m, n )
    #Intialize the first column and row vectors for "null" case costs
    #since these are static and already known
    for k in range(len(wordTo)+1):
        word_transfer_score_matrix[0][k] = k * INSERT_COST
        word_transfer_trace_matrix[0][k] = INSERT_SYM
    for k in range(len(wordFrom)+1):
        word_transfer_score_matrix[k][0] = k * DELETE_COST
        word_transfer_trace_matrix[k][0] = DELETE_SYM
    #initialize our operation matrix that we use to keep track
    #of which operations were used in each iteration
    word_transfer_trace_matrix[0][0] = NOCHANGE_SYM
    #iterate through word A to word B and find optimal sub problems at each step
    for i in range (1, m + 1) :
        for j in range (1, n + 1 ) :
            #if the letters are the same, then the cost is the previous iteration for both words
            if wordFrom[i - 1] == wordTo[j - 1] :
                word_transfer_trace_matrix[i][j] = NOCHANGE_SYM
                word_transfer_score_matrix[i][j] = word_transfer_score_matrix[i - 1][j - 1]
            #the letters are not the same, so find the best solution...
            else:
                update_score_matrix ( i, j, word_transfer_score_matrix, word_transfer_trace_matrix )

    return word_transfer_score_matrix[m][n], word_transfer_score_matrix, word_transfer_trace_matrix

#Routine to find the best solution when letters are not equal for an interation
def update_score_matrix(i, j, word_transform_score_matrix, word_transform_trace_matrix) :
    #figure out costs for each possible operation (delete, insert, replace)
    insert_cost = Transfer(INSERT_COST + word_transform_score_matrix[i][j - 1], INSERT_SYM)
    remove_cost = Transfer(DELETE_COST + word_transform_score_matrix[i - 1][j], DELETE_SYM)
    replacement_cost = Transfer(REPLACE_COST + word_transform_score_matrix[i - 1][j - 1], REPLACE_SYM)
    #find minimal cost or "best" operation at this iteration
    li = [replacement_cost, insert_cost, remove_cost  ]
    min_cost = min ( li, key=lambda x : x.cost )
    #place best or minimal costs in our cost matrix and add operation used to our operation matrix
    word_transform_score_matrix[i][j] = min_cost.cost
    word_transform_trace_matrix[i][j] = min_cost.funct

#helper routine to initialize score matrix to all 0's
def initialize_score_matrix(m: int, n: int) -> List[List[int]] :
    word_transfer_score_matrix: List[List[int]] = [[0 for x in range ( n + 1 )] for x in range ( m + 1 )]
    return word_transfer_score_matrix

#helper routine to intialize our operations matrix to defaults
def initialize_trace_matrix(m: int, n: int) -> List[List[str]] :
    word_transfer_trace_matrix: List[List[str]] = [[NOCHANGE_SYM for x in range ( n + 1 )] for x in range ( m + 1 )]
    return word_transfer_trace_matrix

#special helper routine to combine costs and operations so we can print out the operations used to convert
#this makes for a nice printout and very helpful for debugging process
def combined_score_trace_matrices(score, trace, m, n):
    combined_matrix = initialize_trace_matrix(m, n)
    for i in range(m+1):
        for j in range(n+1):
            sc_tr = " " + trace[i][j] + ":" + str ( score[i][j] )
            combined_matrix[i][j] = sc_tr
    return combined_matrix

#helper routine to add the words to the trace operation matrix
#to make easy to read
def add_words_to_combined(combined_matrix, wordOne, wordTwo):
    #convert strings to lists and add NULLs to front
    l1 = list("0" + "0" + wordOne)
    l2 = list("0" + wordTwo)
    #add TO word to first row
    combined_matrix.insert(0, l2)
    #add FROM word to first column
    for l in range(len(l1)):
        c = combined_matrix[l]
        c.insert(0, "   " + l1[l] + "  ")
    return combined_matrix

# Main run
init(autoreset = True)
# set words to convert "from" and "to"
wordOne = "cit"
wordTwo = "catamaran"
print("-----------------------")
print("Word From: " + wordOne)
print("Word To: " + wordTwo)
# do main transformation from word A to word B
total_score, score_matrix, trace_matrix = transform_word_dynamic_programming ( wordOne, wordTwo )
# create special matrix that has operations and costs for each step combined for easy viewing
combined_matrix = combined_score_trace_matrices(score_matrix, trace_matrix, len(wordOne), len(wordTwo))
#add words to trace matrix for easy readability
add_words_to_combined(combined_matrix, wordOne, wordTwo)

#print out results!
print("Score Matrix:")
print ( ndtotext ( np.array ( score_matrix ) ) )
print(Fore.MAGENTA + "Conversion Cost: {0}".format(total_score))
print("Trace Path")
print(ndtotext (np.array (combined_matrix)))
