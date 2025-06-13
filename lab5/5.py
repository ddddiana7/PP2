import re

txt = input("Enter your string: ")

x = re.search("^a.*b$", txt)

if x:
    print("Match found")

else: 
    print ("No Match")