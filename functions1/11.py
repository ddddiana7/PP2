
def palindrome(st):

    c = st.replace(" ", "").lower()
    lst = list (c)

    lst.reverse()

    lst1 = list(c)

    if lst == lst1:
        print ("It is palindrome!")
    else: print("It is not palindrome!")

st = (input("Enter word or phrase: "))
palindrome(st)