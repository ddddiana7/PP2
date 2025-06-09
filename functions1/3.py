def solve(numheads, numlegs):
    for c in range (numheads + 1):
        r = numheads - c
        if 2 * c + 4 * r == numlegs:
            return c, r
    return "No Solution."

heads = int(input("Enter the number of heads:"))
legs = int (input ("Enter the number of legs:"))
c, r = solve(heads, legs)
print(f"Chickens: {c}, Rabbits: {r}")