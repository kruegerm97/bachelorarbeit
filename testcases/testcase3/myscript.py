import pandas as pd

# Read Excel file
df = pd.read_excel('Fallzahlen.xlsx', sheet_name='Fallzahlen_2023', usecols=['Bezirke','Straftaten_insgesamt'])

# Extract total and save for later
total = df['Straftaten_insgesamt'].iloc[-1]
df = df.iloc[:-1]

# Calculate percentage
df['% Anteil'] = (df['Straftaten_insgesamt'] / total) * 100
df['% Anteil'] = df['% Anteil'].round(2)

# Add total row
df_total = pd.DataFrame({
    'Bezirke': ['Berlin (PKS gesamt)'],
    'Straftaten_insgesamt': [total],
    '% Anteil': [100]
})
df = pd.concat([df, df_total], ignore_index=True)

print(df)