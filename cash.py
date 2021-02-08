from cs50 import get_float

# Define num of coin
n = 0

# Get +ve change from user
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

# Change of $0.25
while change >= 0.25:
    change -= 0.25
    n += 1

# Change of $0.10
while change >= 0.1:
    change -= 0.1
    n += 1

# Change of $0.05    
while change >= 0.05:
    change -= 0.05
    n += 1

# Change of $0.01   
while change >= 0.01:
    change -= 0.01
    n += 1

# Print total coins
print(f"{n}")