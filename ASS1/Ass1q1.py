# Take input from the user
sentence = input("Enter a sentence: ")

# Number of characters (including spaces)
num_chars = len(sentence)

# Number of words
words = sentence.split()
num_words = len(words)

# Number of vowels
vowels = "aeiouAEIOU"
num_vowels = 0
for ch in sentence:
    if ch in vowels:
        num_vowels += 1

# Print results
print("Number of characters:", num_chars)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)
