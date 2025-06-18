import os

with open('pp2_spring/lab6/examplefile.txt', 'r') as r:
    with open('pp2_spring/lab6/examplefile_copy.txt', 'w') as w:
        for line in r:
            w.write(line)