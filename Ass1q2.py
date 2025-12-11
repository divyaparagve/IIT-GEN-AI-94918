nums = input("Enter numbers (comma-separated): ").split(",")

even = 0
odd = 0

for n in nums:
    if int(n) % 2 == 0:
        even += 1
    else:
        odd += 1

print("Even:", even)
print("Odd:", odd)
5