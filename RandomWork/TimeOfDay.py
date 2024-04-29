class TimeOfDay():
    def __init__(self, **kwargs):
        hour = kwargs["hours"]
        if not self.IsValidHour(hour):
            raise ValueError(f"{hour} is not a valid hour")
        minuets = kwargs["minutes"]
        if not self.IsValidMinuteorSec(minuets):
            raise ValueError(f"{minuets} is not a valid minute")
        seconds = kwargs["seconds"]
        if not self.IsValidMinuteorSec(seconds):
            raise ValueError(f"{seconds} is not a valid second")

        self.__hour__ = kwargs["hours"]
        self.__minute__ = kwargs["minutes"]
        self.__second__ = kwargs["seconds"]

    def IsValidMinuteorSec(self,val):
        if val < 0 or val > 59:
            return False
        else:
            return True

    def IsValidHour(self,hour):
        if (hour < 0 or hour > 23):
            return False
        else:
            return True
    def AddHour(self, hoursToAdd):
        remainingHours = hoursToAdd % 24
        self.__hour__ += remainingHours

        if self.__hour__ > 23:
            self.__hour__ -= 24

        '''
        self.hour += hoursToAdd
        while self.hour > 24:
            self.hour -= 24
        '''

    def AddMinute(self,minutesToAdd):
        
        remainingMinuets = minutesToAdd % 60
        self.__minute__ += remainingMinuets

        if self.__minute__ > 59:
            self.__minute__ -= 60
            self.AddHour(1)

        self.AddHour(minutesToAdd//60)
        
        '''
        self.__minute__ += minutesToAdd

        while self.__minute__ > 59:
            self.AddHour(1)
            self.__minute__ -= 60
        '''

    def AddSecond(self,secondsToAdd):
        remainingSeconds = secondsToAdd % 60
        self.__second__ += remainingSeconds
        if self.__second__ > 59:
            self.__second__ -= 60
            self.AddMinute(1)

        self.AddMinute(secondsToAdd//60)



    def __str__(self):
        return f"{self.__hour__}:{self.__minute__}:{self.__second__}"
    
    def __add__(self,other):
        newVal = TimeOfDay(hours = 0,minutes = 0,seconds = 0)
        newVal.AddHour(self.__hour__ + other.__hour__)
        newVal.AddMinute(self.__minute__ + other.__minute__)
        newVal.AddSecond(self.__second__ + other.__second__)
        return newVal

    def __subtract__(self,other):
        newVal = TimeOfDay(hours = 0,minutes = 0,seconds = 0)
        newVal.AddHour(self.__hour__ - other.__hour__)
        newVal.AddMinute(self.__minute__ - other.__minute__)
        newVal.AddSecond(self.__second__ - other.__second__)
        return newVal        
        
        



time = TimeOfDay(hours = 23, minutes = 1, seconds = 1)
time2 = TimeOfDay(hours = 1, minutes = 1, seconds = 1)

time = time - time2

print(time)


class Date():
    def __init__(self):
        pass
