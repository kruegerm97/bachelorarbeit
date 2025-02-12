import pandas as pd

file = 'Fallzahlen.xlsx'
sheet = 'Fallzahlen_2023'

# Read the excel file
try:
    df = pd.read_excel(file, sheet_name=sheet)
except FileNotFoundError:
    print(f"Datei '{file}' wurde nicht gefunden.")
    exit(1)

# Check for required column
required_columns = ['LOR-Schlüssel', 'Straftaten_insgesamt']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Fehlende Spalten in der Excel-Datei: {missing_columns}")

# Extract non sort rows and save them for later
extract_keys = [999900, 999999]
extract_rows = df[df['LOR-Schlüssel'].isin(extract_keys)]
df = df[~df['LOR-Schlüssel'].isin(extract_keys)]

# Sort dataframe and concat with extracted rows
sorted_df = df.sort_values(by='Straftaten_insgesamt', ascending=False)
sorted_df = pd.concat([sorted_df, extract_rows], ignore_index=True)

print(sorted_df)