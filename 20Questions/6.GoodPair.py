def GoodPair(nums):
    pairs = 0
    for i in range (len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i] == nums[j]:
                pairs = pairs+1
                  
    return pairs

def GoodPairLinear(nums):
    repeatCount = {}

    for num in nums:
        if num not in repeatCount:
            repeatCount[num] = 1
        else:
            repeatCount[num] += 1

    count = 0
    for c in repeatCount.values():
        count += (c-1) * c / 2
    
    return int(count)
print(GoodPair([1,2,3,1,1,3]))
print(GoodPair([1,1,1,1]))
print(GoodPair([1,2,3]))