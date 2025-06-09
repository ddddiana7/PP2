def histogram(lst):
    for i in lst:
        print("*" * i)

lst = list (map (int, input("Enter an array: ").split()))

histogram(lst)