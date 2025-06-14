class Shape:

    def area(self):
        return 0

class Square(Shape):

        def __init__(self, length):
            self.length = length
        
        def area(self):
           return self.length * self.length
        
class Rectangle (Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

obj1 = Shape()
print (obj1.area())

obj2 = Square(7)
print(obj2.area())

obj3 = Rectangle (4, 5)
print(obj3.area())