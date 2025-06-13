import re

txt = input("Enter your string: ")

x = re.compile('(?=[A-Z])') #найти позвоцию перед A-Z, но не включать

print (re.split(x, txt))