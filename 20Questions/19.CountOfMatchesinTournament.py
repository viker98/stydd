def CountMatches(num):
    counter = 0
    while num != 1:
        if num % 2 == 0:
            counter += num/2
            num = num/2
        else:
            counter += (num - 1) / 2
            num = (num- 1) / 2 + 1
    return int(counter)


print(CountMatches(14))