def MoveZeros(nums):
    i = 0
    for j in range(len(nums)):
        num = nums[j]
        if num == 0:
            continue
        nums[i], nums[j] = nums[j], nums[i]
        i += 1
    return nums

print(MoveZeros([0,1,0,3,12]))