import os
lst = list(input().split())
with open('1.txt', 'w') as file:
    for i in lst:
        file.write(str(i) + ' ')