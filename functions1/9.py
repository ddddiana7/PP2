import math

def volume(r):
    v = math.pi * r * r * r * (4/3)

    print (f"The volume of the sphere is {v}")

r  =int (input("Enter the radius of the sphere "))

volume(r)