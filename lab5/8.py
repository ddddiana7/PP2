import re

txt = input("Enter your string: ")

x = re.findall(r'[A-Z][a-z]*', txt) #строка которая нач с заглавной буквы потом lowercase

print(x)
