def EditDistanceDynamic(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],     # Insert
                                dp[i-1][j],     # Remove
                                dp[i-1][j-1]) # Replace

    return dp[m][n]


def EditDistanceRecursive(str1, str2, m, n):

    if m == 0:
        return n

    if n == 0:
        return m

    if str1[m-1] == str2[n-1]:
        return EditDistanceRecursive(str1, str2, m-1, n-1)

    return   min(20 + EditDistanceRecursive(str1, str2, m, n-1), #Insert a character
                 20 + EditDistanceRecursive(str1, str2, m-1, n), # Remove a character
                 5 + EditDistanceRecursive(str1, str2, m-1, n-1) # Replace a character
                )

#Main Runline
str1 = "algorithm"
str2 = "alligator"
print (EditDistanceRecursive(str1, str2, len(str1), len(str2)))
print(EditDistanceDynamic(str1, str2, len(str1), len(str2)))