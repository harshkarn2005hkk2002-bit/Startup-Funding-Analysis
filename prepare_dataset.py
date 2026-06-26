import pandas as pd

# Path to your downloaded CSV
input_csv = r"C:\Users\harsh\Downloads\startup_funding_dataset (1).csv"

# Path to save cleaned dataset
output_csv = "data/real_companies.csv"

# Load CSV
df = pd.read_csv(input_csv)

# Strip spaces in column names
df.columns = df.columns.str.strip()

# Ensure essential columns exist
expected_columns = ['Startup Name', 'Industry', 'Country', 'Funding Stage', 'Amount Raised (USD)', 'Funding Date', 'Number of Employees']
for col in expected_columns:
    if col not in df.columns:
        df[col] = None  # Add empty column if missing

# Strip spaces in string columns
for col in ['Startup Name', 'Industry', 'Country', 'Funding Stage']:
    df[col] = df[col].astype(str).str.strip()

# Convert funding amount to numeric, keep all rows (NaN if invalid)
df['Amount Raised (USD)'] = pd.to_numeric(df['Amount Raised (USD)'].replace('[\$,]', '', regex=True), errors='coerce')

# Save cleaned CSV
df.to_csv(output_csv, index=False)

print(f"Cleaned dataset saved to {output_csv}")
print(f"Total companies: {len(df)}")
print(f"Countries included: {df['Country'].nunique()}")