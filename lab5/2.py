import re

txt = input("Enter your string: ")

x = re.compile("^[a]{1}[b]{2,3}$")

if x.search(txt):
    print("Match found")

else: 
    print ("No Match")