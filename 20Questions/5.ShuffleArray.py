def ShuffleArray(nums,n):
    x = 0
    y = n
    retVal= []

    while y < len(nums):
        retVal.append(nums[x])
        retVal.append(nums[y])
        x += 1
        y += 1
 
    return retVal


Nums = [2,5,1,3,4,7]
Nth = 3
print(ShuffleArray(Nums,Nth))