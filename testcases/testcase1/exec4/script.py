import pandas as pd

# Pfad zur CSV-Datei
csv_datei = 'FZ_2023.csv'

# Lesen der CSV-Datei, Überspringen der ersten vier Zeilen, die keine relevanten Daten enthalten
df = pd.read_csv(csv_datei, skiprows=4, sep=',', encoding='utf-8')

# Anzeigen der ersten paar Zeilen, um sicherzustellen, dass die Daten korrekt gelesen wurden
# print(df.head())

# Bereinigen der Spalte 'Straftaten -insgesamt-'
# Entfernen der Anführungszeichen und Kommata, Umwandeln in Ganzzahlen
df['Straftaten -insgesamt-'] = (
    df['Straftaten -insgesamt-']
    .astype(str)  # Sicherstellen, dass die Werte als Strings behandelt werden
    .str.replace('"', '')  # Entfernen von Anführungszeichen
    .str.replace(',', '')  # Entfernen von Tausendertrennzeichen
    .astype(int)  # Umwandeln in Integer
)

# Optional: Entfernen von nicht zuordenbaren Bezirken, falls gewünscht
# df = df[~df['LOR-Schlüssel (Bezirksregion)'].str.contains('99')]

# Sortieren der Bezirke nach der Gesamtanzahl der Straftaten absteigend
sortierte_df = df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Zur besseren Lesbarkeit können Sie die Spaltennamen umbenennen
sortierte_df = sortierte_df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Bezirk',
    'Straftaten -insgesamt-': 'Straftaten_Gesamt'
})

# Anzeigen der sortierten Liste
print(sortierte_df[['Bezirk', 'Straftaten_Gesamt']].to_string(index=False))