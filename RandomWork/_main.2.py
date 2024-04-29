class HealthComp():
    def __init__(self,health):
        self.heath = health

    def TakeDamage(self,amount):
        self.heath -= amount

class Character():
    '''
    ### Class represents the Character
    * name : str - name of Character
    * health: float - the health of Character
    * level: int - level of the Character
    '''
    def __init__(self,**kwargs):
        self.name = kwargs["name"]
        self.health = kwargs["health"]
        self.level = kwargs["level"]
    
    def TakeDamage(self, damageAmount):
        self.health -= damageAmount
        if self.health <= 0:
            print("I am dead!!")
            self.health = 0

class Player(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Enemy(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def TakeDamage(self,damageAmt):
        super().TakeDamage(damageAmt)
        print("Player got one more score")
        

player1 = Player(name = "player1", health = 10, level = 1)
enemy1 = Enemy(name = "enemy1", health = 10, level = 1)
player1.TakeDamage(39)
enemy1.TakeDamage(30)