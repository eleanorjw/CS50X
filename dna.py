import sys
import csv

names = []


# Proper cmdlinearg
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

# Open csv file and read
with open(sys.argv[1], "r") as f:
    reader = csv.DictReader(f)
    h = reader.fieldnames
    col = len(h)
    for name in reader:
        for i in range(1, col):
            name[h[i]] = int(name[h[i]])
        names.append(name)

# Open, read and close txt
txtf = open(sys.argv[2], "r")
txt = txtf.read()
txtf.close()

# Find max STR repeat
max = []
# Get each STR arrangement
for i in range(1, col):
    L = len(h[i])
    tmp = 0
    m = 0
    j = 0
    # Loop through txt to search for max of each arrangement
    while j + L <= len(txt):
        if txt[j:j + L] == h[i]:
            tmp += 1
            j += L
            if tmp > m:
                m = tmp
        else:
            tmp = 0
            j += 1
    max.append(m)
    
# Find match
matched = False
# Loop through list of names
for i in range(len(names)):
    match = 0
    # Check if each person STR matches
    for j in range(1, col):
        if names[i][h[j]] == max[j - 1]:
            match += 1
    if match == col - 1:
        print(f"{names[i]['name']}")
        matched = True
if matched == False:
    print("No match")