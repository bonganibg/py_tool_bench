import polars as pl 

df = pl.read_parquet("./data/parquet/A.csv.parquet")
print(df)