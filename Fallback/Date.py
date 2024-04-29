class Date():
    def __init__(self, **kwargs):
        Year = kwargs["Year"]
        if not self.IsValidYear(Year):
            raise ValueError(f"{Year} is not a valid year")
        Months = kwargs["Months"]
        if not self.IsValidMonth(Months):
            raise ValueError(f"{Months} is not a valid Month")
        Days = kwargs["Days"]
        if not self.IsValidDay(Days,Months):
            raise ValueError(f"{Days} is not a valid days")

        self.__Year__ = kwargs["Year"]
        self.__Months__ = kwargs["Months"]
        self.__Days__ = kwargs["Days"]

    def IsValidYear(self,val):
        if val < 0:
            return False
        else:
            return True
    def IsValidMonth(self,val):
        if val < 0 or val > 12:
            return False
        else:
            return True
        
    def IsValidDay(self,day,month):
        if month in {1,3,5,7,8,10,12} and (day < 0 or day > 31):
            return False
        elif month in {4,6,9,11} and (day < 0 or day > 30):
            return False
        elif month == 2 and ( day < 0 or day > 28):
            return False
        else:
            return True

    def AddYear(self,yearsToAdd):
        self.__Year__ += yearsToAdd

    def AddMonth(self,monthsToAdd):
        remainingMonths = monthsToAdd %  12
        self.__Months__ += remainingMonths

        if self.__Months__ > 12:
            self.__Months__ -= 12
            self.AddYear(1)

        self.AddYear(monthsToAdd//12)

    def __str__(self):
        return f"{self.__Months__}/{self.__Days__}/{self.__Year__}"
    def AddDays(self,daysToAdd):
        while daysToAdd > 0:
            if self.__Months__ in {1,3,5,7,8,10,12}:
                self.__Days__ += 1
                daysToAdd -= 1
                if self.__Days__ > 31:
                    self.__Days__ = 1
                    self.AddMonth(1)
            elif self.__Months__ in {4,6,9,11}:
                self.__Days__ += 1
                daysToAdd -= 1
                if self.__Days__ > 30:
                    self.__Days__ = 1
                    self.AddMonth(1)
                    
            elif self.__Months__ == 2 :
                self.__Days__ += 1
                daysToAdd -= 1
                if self.__Days__ > 28:
                    self.__Days__ = 1
                    self.AddMonth(1)
    
    def __add__(self,other):
        newVal = Date(Year = 0,Months = 0,Days = 0)
        newVal.AddYear(self.__Year__ + other.__Year__)
        newVal.AddMonth(self.__Months__ + other.__Months__)
        newVal.AddDays(self.__Days__ + other.__Days__)
        return newVal 

day = Date(Year = 2024, Months = 1, Days = 25)

day2 = Date(Year = 50, Months = 1,Days = 4)

day = day + day2
print(day)
