class Bank:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.amount = amount
        self.balance += amount
        print (f"Deposited {amount}. Balance is {self.balance}.")

    def withdraw(self, amount):
        self.amount = amount
        if amount > self.balance:
            print (f"Balance is {self.balance}. Withdrawl is denied.")
        else: 
            self.balance -= amount
            print (f"Widrawn {amount}. Balance is {self.balance}.")
        
User = Bank ("Diana", 100)

User.deposit(50)
User.withdraw(300)
User.withdraw (50)
            



        
