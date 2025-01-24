import pandas as pd

# Pfad zur Excel-Datei und Name des Sheets
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Lesen des Excel-Sheets
# Annahme: Die tatsächlichen Spaltenüberschriften beginnen ab der 5. Zeile (Index 4)
# Passen Sie 'skiprows' entsprechend an, falls die Struktur der Excel-Datei abweicht
df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=4, dtype=str)

# Entfernen von Leerzeilen oder Zeilen ohne Bezirksschlüssel
df = df.dropna(subset=['LOR-Schlüssel (Bezirksregion)'])

# Funktion zur Bereinigung und Konvertierung der Zahlen
def clean_number(x):
    if isinstance(x, str):
        # Entfernen von Punkten und Kommas als Tausendertrennzeichen
        return int(x.replace('.', '').replace(',', ''))
    else:
        return x

# Bereinigung der 'Straftaten insgesamt' Spalte
df['Straftaten insgesamt'] = df['Straftaten insgesamt'].apply(clean_number)

# Optional: Bereinigung weiterer relevanter Spalten (falls benötigt)
# Beispiel für 'Raub' Spalte
# df['Raub'] = df['Raub'].apply(clean_number)

# Sortieren des DataFrames nach 'Straftaten insgesamt' in absteigender Reihenfolge
df_sorted = df.sort_values(by='Straftaten insgesamt', ascending=False)

# Zurücksetzen des Indexes nach dem Sortieren
df_sorted = df_sorted.reset_index(drop=True)

# Auswahl relevanter Spalten zur Anzeige
# Sie können weitere Spalten hinzufügen oder entfernen, je nach Bedarf
result = df_sorted[['Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']]

# Anzeige der sortierten Ergebnisse
print(result)

# Optional: Speichern der sortierten Daten in eine neue Excel-Datei
output_file = 'Sortierte_Fallzahlen_2023.xlsx'
df_sorted.to_excel(output_file, sheet_name='Sortiert', index=False)
print(f"\nDie sortierten Daten wurden in '{output_file}' gespeichert.")