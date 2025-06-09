import math

def is_prime(n):
    if n < 2:
        return False
    for i in range (2, int(math.sqrt(n)) + 1):
        if n % 2 == 0 :
            return False
        else: return True
    return True

def filter_prime (numbers):
    return list(filter(is_prime, numbers))


userinput = list(map(int, input("Enter numbers: ").split()))

prime_numbers = filter_prime(userinput)
print("Prime numbers:", prime_numbers)                