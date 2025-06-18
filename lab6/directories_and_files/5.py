import os
list = list(input().split())
with open('pp2_spring/lab6/examplefile.txt', 'w') as file:
    for i in list:
        file.write(str(i) + ' ')