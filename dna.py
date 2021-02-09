import sys
import csv

names = []


# Proper cmdlinearg
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

# Open csv file
with open(sys.argv[1], "r") as f:
    reader = csv.DictReader(f)
    h = reader.fieldnames
    col = len(h)
    for name in reader:
        for i in range(1, col):
            name[h[i]] = int(name[h[i]])
        names.append(name)

# Open txt
txtf = open(sys.argv[2], "r")
txt = txtf.read()
txtf.close()

# Find max STR repeat
max = []
for i in range(1, col):
    l = len(h[i])
    tmp = 0
    m = 0
    def checkSTR(j):
        global tmp
        global m
        if txt[j:j + l] == h[i]:
            tmp += 1
            j += l
            if tmp > m:
                m = tmp
        else:
            tmp = 0
            j += 1
            
        if (j + l) <= len(txt):
                checkSTR(j)
    checkSTR(0)
    max.append(m)
    
# Find match
matched = False
for i in range(len(names)):
    match = 0
    for j in range(1, col):
        if names[i][h[j]] == max[j - 1]:
            match += 1
    if match == col - 1:
        print(f"{names[i]['name']}")
        matched = True
if matched == False:
    print("No match")




