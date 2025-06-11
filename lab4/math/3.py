import math

def area_of_polygon(sides, length):
    area = (sides * length**2)/(4 * math.tan(math.pi/sides))
    print (f"The area of the polygon is: {round(area, 0)}")

sides = int(input("Input number of sides: "))
length = int (input("Input the length of a side: "))

area_of_polygon(sides, length)