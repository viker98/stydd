def numWaterBottles(NumberOfBottles, Exchange):
        return int(NumberOfBottles + (NumberOfBottles - 1) / (Exchange - 1))


print(numWaterBottles(15,4))