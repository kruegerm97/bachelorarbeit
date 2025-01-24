import pandas as pd

# Datei- und Sheetnamen festlegen
file_name = 'Fallzahlen&HZ2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Excel-Sheet lesen, die ersten 4 Zeilen überspringen
df = pd.read_excel(file_name, sheet_name=sheet_name, header=4, thousands=',')

# OPTIONAL: Überprüfe die Spaltenüberschriften
#print(df.columns)

# Überprüfen, ob die Spalten 'Bezeichnung (Bezirksregion)' und 'Straftaten -insgesamt-' existieren
required_columns = ['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Spalte '{col}' nicht gefunden. Überprüfe die Spaltennamen.")

# Sortieren nach der Gesamtzahl der Straftaten in absteigender Reihenfolge
df_sorted = df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Ergebnis anzeigen (Top 10 Bezirke)
print(df_sorted[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']].head(10))

# Ergebnis in eine neue Excel-Datei speichern
df_sorted.to_excel('sorted_fallzahlen_2023.xlsx', index=False)

# OPTIONAL: Ergebnis als CSV speichern
# df_sorted.to_csv('sorted_fallzahlen_2023.csv', index=False)