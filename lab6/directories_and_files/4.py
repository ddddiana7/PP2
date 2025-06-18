import os

with open('pp2_spring/lab6 (DONE)/builtinfunctions/builtinfunc1.py', 'r') as file:
    x = sum(1 for line in file)

print(x)