import pandas as pd
import pandasql as ps
# SQL on Pandas Dataframes
#   - pandasql
#   - duckdb

filepath = "books_hdr.csv"

df = pd.read_csv(filepath)
print("Dataframe Column Types:")
print(df.dtypes)
print("\nbook Data:")
print(df)
# query = "SELECT * FROM data WHERE price BETWEEN 100 AND 2000 ORDER BY subject"
query = "SELECT * FROM data WHERE price BETWEEN 100 AND 2000 ORDER BY subject"
result = ps.sqldf(query, {"data": df})
print("\nQuery Result:")
print(result)