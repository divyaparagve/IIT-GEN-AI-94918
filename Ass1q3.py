import csv

# Read CSV
with open("Products.csv", "r") as f:
    data = list(csv.reader(f))

header = data[0]
rows = data[1:]

# b) Print each row
for row in rows:
    print(row)

# c) Total rows
print("Total rows:", len(rows))

# d) Products priced above 500
count_above_500 = 0
for r in rows:
    if float(r[3]) > 500:   # Price column
        count_above_500 += 1
print("Products above 500:", count_above_500)

# e) Average price
total_price = 0
for r in rows:
    total_price += float(r[3])
avg_price = total_price / len(rows)
print("Average price:", avg_price)

# f) Products of a category
cat = input("Enter category: ")
for r in rows:
    if r[2].lower() == cat.lower():
        print("Product:", r[1])

# g) Total quantity in stock
total_qty = 0
for r in rows:
    total_qty += int(r[4])
print("Total quantity:", total_qty)
