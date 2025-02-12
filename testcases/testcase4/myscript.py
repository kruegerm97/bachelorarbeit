import pandas as pd

# Read Excel
df = pd.read_excel('Fallzahlen.xlsx', sheet_name=None, usecols=['Bezirke', 'Straftaten_insgesamt'])

gesamtwerte = []
# Loop all sheets
for sheet_name, data in df.items():
    # Get year from sheet name
    year = sheet_name.split('_')[-1]
    # Get total
    total = data["Straftaten_insgesamt"].iloc[-1]
    # Append to list
    gesamtwerte.append((year, total))

# Create DataFrame and add % change
df_total = pd.DataFrame(gesamtwerte, columns=['Jahr', 'Straftaten_insgesamt'])
df_total["% Entwicklung"] = df_total['Straftaten_insgesamt'].pct_change() * 100
df_total["% Entwicklung"] = df_total["% Entwicklung"].round(2)

print(df_total)