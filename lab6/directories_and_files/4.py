import os

with open('3.py', 'r') as file:
    x = sum(1 for line in file)

print(x)