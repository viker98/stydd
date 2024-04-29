def SingleNumber(nums):
    for i in range (len(nums)):
        hasDup = False
        for j in range(len(nums)):
            if i != j and nums[i] == nums[j]:
                hasDup = True        

        if not hasDup:
            return nums[i]        
                
    
def SingleNumberInClass(nums):
    twice = {}
    for i in range(len(nums)):
        num = nums[i]
        twice[i] = num
        if num in twice:
            print(twice)
            twice[i] = num 
        else:
            return num

def singlenum(nums):
    counts = {}
    for num in nums:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
            print(counts)

    print(counts)
    for num, count in counts.items():
        if count == 1:
            return num
    

def singlenumInConstant(nums):
    retVal = 0
    for num in nums:
        retVal ^= num
    return retVal


print(singlenum([4,1,2,1,2]))
'''
print(SingleNumber([2,2,1]))
print(SingleNumber([4,1,2,1,2]))
print(SingleNumber([1]))
'''