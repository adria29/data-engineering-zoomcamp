import sys
import pandas as pd

month = sys.argv[1] #[0] is always the script file name
print(f'hello pipeline, month = {month}')

df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "month": month})
print(df.head())

df.to_parquet(f"output_day_{month}.parquet")
