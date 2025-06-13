import re

txt  = input("Enter your string: ")

print(txt.replace(' ', ':').replace('.', ':').replace(',', ':'))