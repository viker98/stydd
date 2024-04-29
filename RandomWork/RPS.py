import random as rnd

RPSGuess = 0
keepPlaying = 1

WinCombos = {1:3,
             2:1,
             3:2}
ComputerOptions = list(WinCombos.keys())
def GetPlayerInput():
    #print("AI Guess is: ", AIGuess )
    print("Welcome to Rock Paper Scissors\nPlease Pick a Number")
    RPSGuess = input("'1' for Rock, '2' for Paper, '3' for Scissors: ")
    if (RPSGuess.isnumeric() and (RPSGuess == "1" or RPSGuess == "2" or RPSGuess == "3")):
        RPSGuess = int(RPSGuess)
        print(RPSGuess)
        return RPSGuess
    else:
        print("That is not a valid Answer")
        GetPlayerInput()
        

def RockPaperScissors():
    RPSGuess = GetPlayerInput()
    AIGuess = rnd.choice(ComputerOptions)
    if(WinCombos[RPSGuess] == AIGuess):
        print("Computer Chose", AIGuess)
        print("You Win")
        keepPlaying = input("Do you wanna keep going '1' for Yes and '0' for No: ")
        keepPlaying = int(keepPlaying)
    elif(RPSGuess == AIGuess):
        print("Computer Chose", AIGuess)
        print("Its a tie\nThanks for playing!")
        keepPlaying = input("Do you wanna keep going '1' for Yes and '0' for No: ")
        keepPlaying = int(keepPlaying)
    else:
        print("Computer Chose", AIGuess)
        print("You Lose\nThanks for Playing")
        keepPlaying = input("Do you wanna keep going '1' for Yes and '0' for No: ")
        keepPlaying = int(keepPlaying)

while keepPlaying == 1:
    RockPaperScissors()
else:
    print("Thanks for playing!!")
