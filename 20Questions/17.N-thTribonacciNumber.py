
def NthTribonacciNum(num):
    if num == 0:
        return 0
    Tlist = [0,1,1]
    for i in range(num-2):
        Tlist.append(sum(Tlist[-3:]))
    return Tlist[-1]

print(NthTribonacciNum(25))