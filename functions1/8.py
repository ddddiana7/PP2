def spy_game(nums):
    a = [0, 0, 7]
    for i in nums:
        if i == a[0]:
            a.pop(0)
        if not a:
            return True
        
    return False

nums = list(map(int, input("Enter an array: ").split()))


print (spy_game(nums))