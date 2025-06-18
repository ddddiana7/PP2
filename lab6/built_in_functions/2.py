string2 = input("Enter your string: ")
upper = sum(map(lambda x: x.isupper(), string2))
lower = sum(map(lambda x: x.islower(), string2))
print(f"Upper: {upper}, lower: {lower}")