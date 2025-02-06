import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Einlesen der Excel-Datei
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Anzeigen der ersten paar Zeilen (optional)
print("Unsortierte Daten:")
print(df.head())

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Anzeigen der sortierten Daten (optional)
print("\nSortierte Daten nach 'Straftaten_insgesamt':")
print(df_sortiert.head())

# Optional: Speichern des sortierten DataFrames in einer neuen Excel-Datei
df_sortiert.to_excel('Fallzahlen_sortiert.xlsx', index=False)

print("\nDie sortierten Daten wurden in 'Fallzahlen_sortiert.xlsx' gespeichert.")