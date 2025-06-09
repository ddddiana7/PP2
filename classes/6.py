import math

prime = lambda n:(
    n > 1 and all (n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
)


nums = [1, 3, 5, 7, 2, 11, 30, 22, 39]

primeNums = list (filter(prime, nums))

print ("Prime numbers are: ", primeNums)