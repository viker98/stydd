def HappyNumber(n):
    visited = set()
    while n != 1:
        cpy = n
        sum = 0
        while cpy > 0:
            digit = cpy % 10
            cpy //= 10
            sum += digit ** 2
        n = sum

        if n not in visited:
            visited.add(n)
        else:
            return False
    return True

print(HappyNumber(19))
            