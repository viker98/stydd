def TwoSum(nums,target):
    for i in range (len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target and i != j:
                return [i,j]
                
def TwoSumInClass(nums,target):
    compliments = {}
    for i in range(len(nums)):
        num = nums[i]
        compliment = target - num
        if num in compliments:
            return[compliments[num], i]       
        
        compliments[compliment] = i


print(TwoSumInClass([2,7,11,15],9))
print(TwoSumInClass([3,2,4],6))
print(TwoSumInClass([3,3],6))
print("")

print(TwoSum([2,7,11,15],9))
print(TwoSum([3,2,4],6))
print(TwoSum([3,3],6))
