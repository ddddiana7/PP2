import os

with open('1.txt', 'r') as r:
    with open('2.txt', 'w') as w:
        for line in r:
            w.write(line)