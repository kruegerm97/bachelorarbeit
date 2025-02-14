import pandas as pd

# Pfad zur Excel-Datei
file_path = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Excel-Datei einlesen
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Anzeige der ersten Zeilen zur Überprüfung (optional)
# print(df.head())

# Annahme: Der LOR-Schlüssel hat mindestens 5 Stellen
# Extrahieren des Oberbezirkskennung (erste zwei Stellen)
df['Oberbezirk_Key'] = df['LOR-Schlüssel'].astype(str).str[:2]

# Extrahieren des Unterbezirkskennung (ganzer Schlüssel)
df['Unterbezirk_Key'] = df['LOR-Schlüssel'].astype(str)

# Gruppieren nach Oberbezirk_Key und Bezeichnung des Oberbezirks
# Hier nehmen wir an, dass die Bezeichnung des Oberbezirks dieselbe ist für alle Unterbezirke
oberbezirke = df.groupby('Oberbezirk_Key')['Bezeichnung'].first().reset_index()
oberbezirke = oberbezirke.rename(columns={'Bezeichnung': 'Oberbezirk_Name'})

# Merge der Oberbezirk Informationen zurück zum Haupt-DataFrame
df = df.merge(oberbezirke, on='Oberbezirk_Key', how='left')

# Gruppieren nach Oberbezirk und Finden des Unterbezirks mit den meisten Raubdelikten
# Annahme: Die Spalte für Raubdelikte heißt 'Raub'
result = df.groupby('Oberbezirk_Name').apply(
    lambda x: x.loc[x['Raub'].idxmax()][['Bezeichnung', 'Raub']]
).reset_index()

# Umbenennen der Spalten für Klarheit
result = result.rename(columns={
    'Bezeichnung': 'Unterbezirk_mit_meisten_Raub',
    'Raub': 'Anzahl_Raub'
})

# Anzeige des Ergebnisses
print(result)

# Optional: Speichern des Ergebnisses in eine CSV-Datei
result.to_csv('Unterbezirk_mit_meisten_Raub_pro_Oberbezirk_2023.csv', index=False)