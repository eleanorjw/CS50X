from cs50 import get_float

# Define num of coin
n = 0

# Get +ve change from user and convert to cents
while True:
    change = int(get_float("Change owed: ") * 100)
    if change > 0:
        break


# Change of $0.25
while change >= 25:
    change -= 25
    n += 1

# Change of $0.10
while change >= 10:
    change -= 10
    n += 1

# Change of $0.05    
while change >= 5:
    change -= 5
    n += 1

# Change of $0.01   
while change >= 1:
    change -= 1
    n += 1

# Print total coins
print(f"{n}")