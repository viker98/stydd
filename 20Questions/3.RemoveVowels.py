def RemoveVowels(word):
    keyToRemove = ['a','e','i','o','u']
    newstr = ""
    for i in range (0,len(word)):
        if word[i] not in keyToRemove:
            newstr+=word[i]
    return newstr 
print(RemoveVowels("artstationisacommunityforartists"))
