import re

txt = input("Enter your string: ")

x = re.compile('(?=[A-Z])')
print(x.sub(' ', txt)) #вставляет пробел перед каждой заглав буквой