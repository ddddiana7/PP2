import re

txt = input("Enter your string: ")

#обычные слова с загл
step1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', txt) #любой симв перед загл+загл буква + строчные буквы в любом колве +шаблон для замены + где происходит замена

#любое место
snake_case = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', step1).lower()

print("snake_case string:", snake_case)
