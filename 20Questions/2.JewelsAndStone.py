def JewsAndStone(Jewels,Stones):
    matching = 0
    for i in range (0,len(Jewels)):
        for j in range (0,len(Stones)):
            for x,y in zip (Jewels[i],Stones[j]):
                if x == y:
                    matching = matching + 1
    return matching
print(JewsAndStone("faoBDAbB","aABbaBfdDo"))