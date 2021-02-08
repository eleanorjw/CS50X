from cs50 import get_string

# Get user text
text = get_string("Text: ")

# Calculate letters, words and sentences in text
lttr = 0
words = 1
stc = 0
for c in text:
    # Cal letters
    if c.isalpha():
        lttr += 1
    # Cal words    
    elif c == " ":
        words += 1
    # Cal sentences
    elif c == "." or c == "?" or c == "!":
        stc += 1

# Cal index
index = round(0.0588 * lttr / words * 100 - 0.296 * stc / words * 100 - 15.8)
    
# Print results
if index > 15:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")

