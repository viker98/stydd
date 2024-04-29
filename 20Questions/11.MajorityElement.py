def MajorityElement(nums):
    counts = {}
    for num in nums:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
    print(counts)
    for num, count in counts.items():
        if count > len(nums)/2:
            return num
    
