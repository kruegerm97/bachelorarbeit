import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ2014-2023.xlsx'

# Einlesen des Sheets 'Fallzahlen_2023'
# Annahme: Die relevanten Daten beginnen ab der 5. Zeile (Index 4)
df = pd.read_excel(excel_datei, sheet_name='Fallzahlen_2023', skiprows=4)

# Anpassen der Spaltennamen, falls sie Leerzeichen oder Sonderzeichen enthalten
df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace(' ', '_').str.replace('-', '_').str.replace(',', '').str.replace('.', '')

# Anzeigen der ersten Zeilen zur Überprüfung
print("Erste Zeilen des DataFrames:")
print(df.head())

# Entfernen von Zeilen, die keine Bezirke enthalten (z.B. Gesamtübersicht)
# Annahme: Bezirkscode sollte numerisch sein, daher filtern wir Zeilen mit numerischen LOR-Schlüsseln
df = df[pd.to_numeric(df['LOR-Schlüssel_(Bezirksregion)'], errors='coerce').notnull()]

# Bereinigen der 'Straftaten_insgesamt' Spalte:
# Entfernen von Tausendertrennzeichen und Umwandeln in Integer
df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].astype(str).str.replace(',', '').astype(int)

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Anzeigen der sortierten Daten
print("\nSortierte Daten (nach 'Straftaten_insgesamt'):")
print(df_sortiert[['Bezeichnung_(Bezirksregion)', 'Straftaten_insgesamt']].head(20))

# Optional: Speichern der sortierten Daten in eine neue Excel-Datei
sortierte_datei = 'Fallzahlen_2023_sortiert.xlsx'
df_sortiert.to_excel(sortierte_datei, index=False)
print(f"\nDie sortierten Daten wurden in der Datei '{sortierte_datei}' gespeichert.")