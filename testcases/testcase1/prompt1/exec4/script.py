import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Excel-Datei einlesen
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Daten nach 'Straftaten_insgesamt' in absteigender Reihenfolge sortieren
df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Optional: Den sortierten DataFrame anzeigen
print(df_sortiert)

# Optional: Den sortierten DataFrame in eine neue Excel-Datei speichern
df_sortiert.to_excel('Fallzahlen_sortiert.xlsx', index=False)