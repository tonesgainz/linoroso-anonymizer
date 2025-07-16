import pandas as pd  # For data tables
import numpy as np   # For random scrambling

# Step 1: Load the raw CSV
file_path = 'business_report_raw.csv'  # Your file name
df = pd.read_csv(file_path)  # df = DataFrame (table)

# Extract and print labels (columns) for verification
columns = df.columns.tolist()
print("Extracted Columns:", columns)

# Step 2: Anonymize identifiers
# Mask ASINs, Titles, SKUs with generics (e.g., based on row index)
if 'Parent ASIN' in df.columns:
    df['Parent ASIN'] = 'Parent_ASIN_' + df.index.astype(str)
if 'Child ASIN' in df.columns:
    df['Child ASIN'] = 'Child_ASIN_' + df.index.astype(str)
if 'Title' in df.columns:
    df['Title'] = 'Product_Title_' + (df.index + 1).astype(str)  # e.g., Product_Title_1
if 'SKU' in df.columns:
    df['SKU'] = 'SKU_' + df.index.astype(str)

# Set seed for reproducibility (same results each run)
np.random.seed(42)
scramble_factor = np.random.uniform(0.8, 1.2, size=len(df))  # Random factors 0.8-1.2

# Step 3: Scramble numeric columns (sessions, views, units, items)
numeric_cols = ['Sessions - Total', 'Sessions - Total - B2B', 'Page Views - Total', 'Page Views - Total - B2B',
                'Units Ordered', 'Units Ordered - B2B', 'Total Order Items', 'Total Order Items - B2B']
for col in numeric_cols:
    if col in df.columns:
        # Clean commas, convert to float, scramble, round to int
        df[col] = (df[col].astype(str).str.replace(',', '').astype(float) * scramble_factor).round(0).astype(int)

# Step 4: Scramble percentage columns
percent_cols = ['Conversion Rate - Total', 'Session Percentage - Total - B2B', 'Page View Percentage - Total',
                'Page View Percentage - Total - B2B', 'Buy Box Percentage', 'Buy Box Percentage - B2B',
                'Unit Session Percentage', 'Unit Session Percentage - B2B']
for col in percent_cols:
    if col in df.columns:
        # Strip %, convert, scramble, round, re-add %
        df[col] = (df[col].astype(str).str.rstrip('%').astype(float) * scramble_factor).round(2).astype(str) + '%'

# Step 5: Scramble sales columns
sales_cols = ['Ordered Product Sales', 'Ordered Product Sales - B2B']
for col in sales_cols:
    if col in df.columns:
        # Strip US$/commas, convert, scramble, round, re-add US$
        cleaned = df[col].astype(str).str.replace('US$', '', regex=False).str.replace(',', '').astype(float)
        df[col] = 'US$' + (cleaned * scramble_factor).round(2).astype(str)

# Step 6: Clean data (e.g., drop any missing rows if needed)
df = df.dropna()

# Step 7: Sample a subset (e.g., 50% for smaller file)
df_anonymized = df.sample(frac=0.5, random_state=42)  # Adjust frac as needed

# Preview anonymized data
print("\nAnonymized Data Preview:")
print(df_anonymized.head())

# Step 8: Save the anonymized CSV
output_path = 'anonymized_business_report.csv'
df_anonymized.to_csv(output_path, index=False)
print(f"Anonymized file saved as '{output_path}'")