
import numpy as np
import pprint

INSERT_COST = 20
DELETE_COST = 20
REPLACE_COST = 5


def ndtotext(A, w=None, h=None):
    if A.ndim==1:
        if w == None :
            return str(A)
        else:
            s ='['+' '*(max(w[-1],len(str(A[0])))-len(str(A[0]))) +str(A[0])
            for i,AA in enumerate(A[1:]):
                s += ' '*(max(w[i],len(str(AA)))-len(str(AA))+1)+str(AA)
            s +='] '
    elif A.ndim==2:
        w1 = [max([len(str(s)) for s in A[:,i]])  for i in range(A.shape[1])]
        w0 = sum(w1)+len(w1)+1
        s= u'\u250c'+u'\u2500'*w0+u'\u2510' +'\n'
        for AA in A:
            s += ' ' + ndtotext(AA, w=w1) +'\n'
        s += u'\u2514'+u'\u2500'*w0+u'\u2518'
    elif A.ndim==3:
        h=A.shape[1]
        s1=u'\u250c' +'\n' + (u'\u2502'+'\n')*h + u'\u2514'+'\n'
        s2=u'\u2510' +'\n' + (u'\u2502'+'\n')*h + u'\u2518'+'\n'
        strings=[ndtotext(a)+'\n' for a in A]
        strings.append(s2)
        strings.insert(0,s1)
        s='\n'.join(''.join(pair) for pair in zip(*map(str.splitlines, strings)))
    return s


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

    a = np.array ( wordTransferScoreMatrix )
    print(ndtotext(a, 10, 20))


    return wordTransferScoreMatrix[m][n]


def WordTransformCost_Recursive(str1, str2, m, n):

    if m == 0:
        return n* INSERT_COST

    if n == 0:
        return m* INSERT_COST

    if str1[m-1] == str2[n-1]:
        return WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )

    return   min( 20 + WordTransformCost_Recursive( str1, str2, m, n - 1 ),  #Insert a character
                  20 + WordTransformCost_Recursive( str1, str2, m - 1, n ),  # Remove a character
                  5 + WordTransformCost_Recursive( str1, str2, m - 1, n - 1 )  # Replace a character
                  )

#Main Runline
wordOne = "hon"
wordTwo = "hobn"
print ( WordTransformCost_Recursive( wordOne, wordTwo, len( wordOne ), len( wordTwo ) ) )
print( WordTransformCost_DP( wordOne, wordTwo, len( wordOne ), len( wordTwo ) ) )