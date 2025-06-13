import re 

txt = input("Enter your string: ")

x = re.search("[a-z]+[_]{1}", txt)

if x:
    print("Match found")

else: 
    print ("No Match")