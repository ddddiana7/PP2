import math

def angle_radians(degrees):

    radians = degrees * (math.pi/180)
    return radians

degrees = int (input("Input degree: "))

radians = angle_radians(degrees)
print ("Output radians: ", round(radians, 6))
