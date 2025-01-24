import pandas as pd

# Pfad zur CSV-Datei
csv_file = 'FZ_2023.csv'

# CSV-Datei einlesen
# Annahme: Die tatsächlichen Daten beginnen ab der 5. Zeile (Index 4)
df = pd.read_csv(
    csv_file,
    skiprows=4,               # Überspringt die ersten 4 Zeilen (Metadaten)
    delimiter=',',            # Trennzeichen ist ein Komma
    thousands=',',            # Tausendertrennzeichen ist ein Komma
    encoding='utf-8'          # Stellen Sie sicher, dass die Codierung stimmt
)

# Anzeigen der ersten Zeilen zur Überprüfung
print("Erste Zeilen des DataFrames:")
print(df.head())

# Spaltennamen überprüfen
print("\nSpaltennamen:")
print(df.columns.tolist())

# Definieren der relevanten Spalten
district_col = 'Bezeichnung (Bezirksregion)'
total_crimes_col = 'Straftaten -insgesamt-'

# Überprüfen, ob die Spalten existieren
if district_col not in df.columns or total_crimes_col not in df.columns:
    raise ValueError(f"Überprüfen Sie die Spaltennamen. Erwartet '{district_col}' und '{total_crimes_col}'.")

# Bereinigen der Daten: Entfernen von Anführungszeichen und Umwandeln in numerische Werte
df[total_crimes_col] = df[total_crimes_col].replace({',': ''}, regex=True).astype(int)

# Sortieren nach der Gesamtzahl der Straftaten in absteigender Reihenfolge
sorted_df = df.sort_values(by=total_crimes_col, ascending=False)

# Auswahl der relevanten Spalten
result_df = sorted_df[[district_col, total_crimes_col]].reset_index(drop=True)

# Anzeigen der sortierten Daten
print("\nBezirke sortiert nach der Gesamtzahl der Straftaten (2023):")
print(result_df)

# Optional: Speichern der sortierten Daten in eine neue CSV-Datei
output_file = 'Sortierte_Fallzahlen_2023.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nDie sortierten Daten wurden in '{output_file}' gespeichert.")