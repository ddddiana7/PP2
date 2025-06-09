class MyClass:

    def getString(self):
        self.s1 = input()

    def printString(self):
        print (self.s1.upper())

obj = MyClass()

obj.getString()

obj.printString()