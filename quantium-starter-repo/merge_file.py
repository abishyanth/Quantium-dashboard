import pandas as pd

files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

processed_dfs = []

for file in files:
    df = pd.read_csv(file)

    # Keep only Pink Morsels
    df = df[df["product"] == "pink morsel"]


    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
    df["Sales"] = df["quantity"] * df["price"]

    df = df[["Sales", "date", "region"]]

    df.rename(columns={'date': 'Date', 'region': 'Region'}, inplace = True)

    processed_dfs.append(df)


final_df = pd.concat(processed_dfs, ignore_index=True)

final_df.to_csv('pink_morsels_sales.csv', index=False)

print("Formated output file created!!!")