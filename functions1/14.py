import math

def volume(r):
    v = math.pi * r * r * r * (4/3)

    print (f"The volume of the sphere is {v}")
#r  =int (input("Enter the radius of the sphere "))
volume(9)
#Output: The volume of the sphere is 3053.6280592892786



def palindrome(st):

    c = st.replace(" ", "").lower()
    lst = list (c)

    lst.reverse()

    lst1 = list(c)

    if lst == lst1:
        print ("It is palindrome!")
    else: print("It is not palindrome!")
#st = (input("Enter word or phrase: "))
st = "madam"
palindrome(st)
#Output: It is palindrome!



def histogram(lst):
    for i in lst:
        print("*" * i)
#lst = list (map (int, input("Enter an array: ").split()))
lst = 4, 9, 3
histogram(lst)
#Output: ****
#*********
#***


def has_33(nums):
    for i in range (len(nums)- 1):
        if nums [i] == 3 and nums[i+ 1] == 3:
            return True
    return False

#nums = list(map(int, input("Enter an array: ").split()))
nums = 3, 5, 9, 3, 3, 3
print (has_33(nums))
#Output: True