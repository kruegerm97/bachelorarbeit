import pandas as pd

# Read excel file
file = 'Fallzahlen.xlsx'
sheets = pd.read_excel(file, sheet_name=None)

# Join all sheets
joined_df = pd.concat(sheets.values(), ignore_index=True)
grouped_df = joined_df.groupby(['LOR-Schlüssel', 'Bezirke'], as_index=False).sum()

# Exclude not to sort rows
exclude_keys = [999900, 999999]
to_sort_df = grouped_df[~grouped_df['LOR-Schlüssel'].isin(exclude_keys)]
excluded_df = grouped_df[grouped_df['LOR-Schlüssel'].isin(exclude_keys)]

# Sort DF
sorted_df = to_sort_df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Concat excluded rows
final_df = pd.concat([sorted_df, excluded_df], ignore_index=True)

print(final_df)