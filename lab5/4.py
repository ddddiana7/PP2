import re 

txt = input("Enter your string: ")

x = re.search("[A-Z]{1}+[a-z]{1}", txt)

if x:
    print("Match found")

else: 
    print ("No Match")