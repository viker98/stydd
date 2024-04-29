import time


def CountDigitDivide(number):
    t0 = time.time()
    strNumber = str(number)
    amount = 0
    for i in range(len(strNumber)):
        if (number % int(strNumber[i]) == 0):
            amount = amount + 1

    t1 = time.time()
    total = t1-t0
    print(total)
    return amount


def DigInClass(num):
    cpy = num
    count = 0
    while cpy > 0:
        digit = cpy % 10
        cpy = cpy // 10
        if num % digit == 0:
            count += 1
    return count

(DigInClass(1248))

(CountDigitDivide(1248))
