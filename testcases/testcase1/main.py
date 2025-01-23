import pandas as pd

# Pfad zur CSV-Datei
csv_file = 'HZ_2023.csv'

# Laden der CSV-Datei
# Überspringt die ersten 4 Zeilen, die keine Daten enthalten
df = pd.read_csv(
    csv_file,
    delimiter=',',
    skiprows=4,
    quotechar='"',
    encoding='utf-8'
)

# Anzeigen der ersten paar Zeilen, um die Struktur zu überprüfen
print("Ursprüngliche Daten:")
print(df.head())

# Entfernen von Zeilen, die keine gültigen Bezirke sind (z.B. "nicht zuzuordnen")
# Annahme: "Straftaten -insgesamt-" enthält '-' für solche Zeilen
df = df[df['Straftaten \n-insgesamt-'] != '-']

# Entfernen von eventuell vorhandenen Leerzeichen in den Spaltennamen
df.columns = df.columns.str.strip()

# Umbenennen der Spalte für einfacheren Zugriff
df.rename(columns={'Straftaten \n-insgesamt-': 'Straftaten_insgesamt'}, inplace=True)

# Entfernen von Anführungszeichen und Kommas sowie Konvertierung in Ganzzahlen
df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].str.replace('"', '') \
                                                   .str.replace(',', '') \
                                                   .astype(int)

# Sortieren der Bezirke nach der Gesamtanzahl der Straftaten in absteigender Reihenfolge
df_sorted = df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Zurücksetzen des Indexes
df_sorted.reset_index(drop=True, inplace=True)

# Anzeigen der sortierten Daten
print("\nBezirke sortiert nach der Gesamtanzahl der Straftaten (absteigend):")
print(df_sorted[['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', 'Straftaten_insgesamt']])

# Optional: Speichern der sortierten Daten in eine neue CSV-Datei
output_file = 'sorted_crime_data.csv'
df_sorted.to_csv(output_file, index=False)
print(f"\nDie sortierten Daten wurden in '{output_file}' gespeichert.")