import pandas as pd

file = 'Fallzahlen&HZ 2014-2023.xlsx'

# Sheets from 2014 to 2023
sheets = [f'Fallzahlen_{year}' for year in range(2014, 2024)]
dfs = []

# Lines to ignore
ignore_lines = [
    "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf", 
    "Spandau", "Steglitz-Zehlendorf", "Tempelhof-Schöneberg", "Neukölln", 
    "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf",
    "Berlin (PKS gesamt)", "Stadtgebiet Berlin, nicht zuzuordnen"
]

# Read the needed sheets in loop, use only the required columns and add to df list
with pd.ExcelFile(file) as xls:
    for sheet in sheets:
        if sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet, usecols=["Bezeichnung (Bezirksregion)","Straftaten \n-insgesamt-"])
            dfs.append(df)

# Combine all dataframes
combined_df = pd.concat(dfs, ignore_index=True)
# Check if the column is numeric
combined_df["Straftaten \n-insgesamt-"] = pd.to_numeric(combined_df["Straftaten \n-insgesamt-"], errors='coerce')

# Filter out the ignore lines
filtered_df = combined_df[~combined_df['Bezeichnung (Bezirksregion)'].isin(ignore_lines)]

# Group df
grouped_df = filtered_df.groupby('Bezeichnung (Bezirksregion)', as_index=False)['Straftaten \n-insgesamt-'].sum()

# Sort df
sorted_df = grouped_df.sort_values(by="Straftaten \n-insgesamt-", ascending=False)

# Get top 10
top_10 = sorted_df.head(10)

print(top_10)