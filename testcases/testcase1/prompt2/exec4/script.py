import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Namen des Sheets
sheet_name = 'Fallzahlen_2023'

# LOR-Schlüssel der Zeilen, die ausgeschlossen werden sollen
ausschluss_lor_schluessel = [999900, 999999]

# Excel-Datei einlesen
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Anzeigen der ursprünglichen Daten (optional)
print("Ursprüngliche Daten:")
print(df)

# Filtern der Bezirke, indem die ausgeschlossenen LOR-Schlüssel entfernt werden
df_gefiltert = df[~df['LOR-Schlüssel'].isin(ausschluss_lor_schluessel)]

# Anzeigen der gefilterten Daten (optional)
print("\nGefilterte Daten (ohne nicht zuzuordnende Bezirke):")
print(df_gefiltert)

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
df_sortiert = df_gefiltert.sort_values(by='Straftaten_insgesamt', ascending=False)

# Zurücksetzen des Index (optional, für sauberere Anzeige)
df_sortiert.reset_index(drop=True, inplace=True)

# Anzeigen der sortierten Daten (optional)
print("\nSortierte Daten nach 'Straftaten_insgesamt':")
print(df_sortiert)

# Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
# df_sortiert.to_excel('Sortierte_Fallzahlen.xlsx', index=False)