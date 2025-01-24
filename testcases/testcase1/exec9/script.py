import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Lesen der Excel-Datei, Überspringen der ersten 4 Zeilen, da diese Metadaten enthalten
df = pd.read_excel(
    excel_datei,
    sheet_name=sheet_name,
    skiprows=4,
    dtype=str  # Zunächst alle Daten als Strings einlesen
)

# Entfernen von möglichen Nan-Werten in der Spalte 'LOR-Schlüssel (Bezirksregion)'
df = df.dropna(subset=['LOR-Schlüssel (Bezirksregion)'])

# Entfernen von Tausendertrennzeichen und Konvertieren der 'Straftaten insgesamt' in Integer
# Annahme: Die Spalte heißt genau 'Straftaten -insgesamt-'
# Überprüfe die tatsächlichen Spaltennamen ggf. mit df.columns
df['Straftaten -insgesamt-'] = df['Straftaten -insgesamt-'].str.replace('.', '').str.replace(',', '').astype(int)

# Sortieren nach 'Straftaten insgesamt' in absteigender Reihenfolge
df_sortiert = df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Optional: Nur relevante Spalten auswählen
relevante_spalten = ['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']
df_sortiert = df_sortiert[relevante_spalten]

# Anzeigen der sortierten Daten
print(df_sortiert)

# Optional: Speichern der sortierten Daten in eine neue Excel-Datei
df_sortiert.to_excel('Sortierte_Fallzahlen_2023.xlsx', index=False)