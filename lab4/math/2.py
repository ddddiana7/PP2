def area_of_trapezoid(height, base1, base2):
    area = ((base1 + base2)/2)*height
    print (f"Expected Output: {area}")

height = int (input("Height: "))
base1 = int (input("Base, first value: "))
base2  = int (input("Base, second value: "))

area_of_trapezoid(height, base1, base2)