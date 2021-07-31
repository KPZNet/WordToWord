
INSERT_COST = 20
DELETE_COST = 20
REPLACE_COST = 5

def WordTransformCost_DP(str1, str2, m, n):

    wordTransferScoreMatrix = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                wordTransferScoreMatrix[i][j] = j # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                wordTransferScoreMatrix[i][j] = i # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                wordTransferScoreMatrix[i][j] = wordTransferScoreMatrix[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                minCost = min( INSERT_COST + wordTransferScoreMatrix[i][j-1],     # Insert
                               DELETE_COST + wordTransferScoreMatrix[i-1][j],     # Remove
                               REPLACE_COST + wordTransferScoreMatrix[i-1][j-1])  # Replace
                wordTransferScoreMatrix[i][j] = minCost

    return wordTransferScoreMatrix[m][n]


def WordTransformCost_Recursive(str1, str2, m, n):

    if m == 0:
        return n*20

    if n == 0:
        return m*20

    if str1[m-1] == str2[n-1]:
        return WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )

    return   min( 20 + WordTransformCost_Recursive( str1, str2, m, n - 1 ),  #Insert a character
                  20 + WordTransformCost_Recursive( str1, str2, m - 1, n ),  # Remove a character
                  5 + WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )  # Replace a character
                  )

#Main Runline
str1 = "hon"
str2 = "hobn"
print ( WordTransformCost_Recursive( str1, str2, len( str1 ), len( str2 ) ) )
print( WordTransformCost_DP( str1, str2, len( str1 ), len( str2 ) ) )