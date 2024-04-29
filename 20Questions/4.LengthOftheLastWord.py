def LengthofLastWord(sentence):
    length = 0
    for i in range(len(sentence)-1,0,-1):
        if (sentence[i] != " "):
            length = length + 1
        else:
            return length
            
print(LengthofLastWord("luffy is still joyboy"))