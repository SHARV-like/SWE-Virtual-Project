import pandas as pd
import os

data_folder = "data"

all_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

df_list = []

for file in all_files:
    df = pd.read_csv(os.path.join(data_folder, file))
    df.columns = df.columns.str.strip().str.lower()   # 🔥 FIX
    df_list.append(df)

df = pd.concat(df_list, ignore_index=True)

# print("Unique products:")
# print(df["product"].unique())

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Convert price to float
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

# Filter pink morsel
df = df[df["product"].str.strip().str.lower() == "pink morsel"].copy()

# Calculate sales
df["sales"] = df["quantity"] * df["price"]

# Keep required columns
df = df[["sales", "date", "region"]]

df.columns = ["Sales", "Date", "Region"]

df.to_csv("formatted_output.csv", index=False)

print("Done ✅")