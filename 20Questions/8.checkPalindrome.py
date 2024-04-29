def CheckPalindrome(number):
    strnumber = str(number)
    if (number < 0 or (number and number % 10 == 0)):
        return print("no")
    for i in range(len(strnumber)):     
        if(int(strnumber[i]) != int(strnumber[len(strnumber) - 1 - i])):
             return print("no")
        else:
            return print("yes")

(CheckPalindrome(121))
(CheckPalindrome(-121))
(CheckPalindrome(10))