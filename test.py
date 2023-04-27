def recursive_fiboonaci(n):
    if n <= 1:
        return n
    else:
        return recursive_fiboonaci(n - 1) + recursive_fiboonaci(n - 2)


for i in range(1, 7 + 1):
    print(recursive_fiboonaci(i))
