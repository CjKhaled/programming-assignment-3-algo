"""
HVLCS Algorithm
"""

import sys


def read_input(text):
    lines = text.strip().splitlines()

    k = int(lines[0])
    values = {}
    for i in range(1, k + 1):
        ch, v = lines[i].split()
        values[ch] = int(v)

    a = lines[k + 1]
    b = lines[k + 2]
    return values, a, b


def hvlcs(values, a, b):
    m, n = len(a), len(b)

    dp = []
    for i in range(m + 1):
        dp.append([0] * (n + 1))

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                v = values[a[i-1]]
                dp[i][j] = max(dp[i-1][j-1] + v, dp[i-1][j], dp[i][j-1])
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # traceback
    result = []
    i = m
    j = n
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            v = values[a[i-1]]
            if dp[i][j] == dp[i-1][j-1] + v:
                result.append(a[i-1])
                i -= 1
                j -= 1
                continue
        if dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return dp[m][n], "".join(result)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    values, a, b = read_input(text)
    val, subseq = hvlcs(values, a, b)
    print(val)
    print(subseq)


if __name__ == "__main__":
    main()