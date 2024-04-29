def arrangeCoins(n):
        completeStairs = 0
        
        i = 1
        while n >= 0:
            n -= i
            if n >= 0:
              completeStairs += 1
            i += 1

        return completeStairs

print(arrangeCoins(8))


