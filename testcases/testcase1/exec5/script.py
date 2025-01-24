import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Einlesen des Excel-Sheets
df = pd.read_excel(excel_datei, sheet_name=sheet_name, skiprows=4)

# Anzeige der ersten Zeilen zur Überprüfung
#print(df.head())

# Benennung der Spalten basierend auf den gegebenen Daten
spalten = [
    'LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)',
    'Straftaten insgesamt', 'Raub', 'Straßenraub, Handtaschenraub',
    'Körperverletzungen insgesamt', 'Gefährliche und schwere Körperverletzung',
    'Freiheitsberaubung, Nötigung, Bedrohung, Nachstellung',
    'Diebstahl insgesamt', 'Diebstahl von Kraftwagen', 'Diebstahl an/aus Kfz',
    'Fahrraddiebstahl', 'Wohnraumeinbruch', 'Branddelikte insgesamt',
    'Brandstiftung', 'Sachbeschädigung insgesamt', 'Sachbeschädigung durch Graffiti',
    'Rauschgiftdelikte', 'Kieztaten'
]

# Setzen der Spaltennamen
df.columns = spalten

# Entfernen von Zeilen, die keine gültigen Bezirke sind (z.B. leere Zeilen oder Zusammenfassungen)
# Hier nehmen wir an, dass gültige Bezirke eine numerische LOR-Schlüssel haben
df = df[df['LOR-Schlüssel (Bezirksregion)'].astype(str).str.match(r'^\d+')].copy()

# Bereinigung der 'Straftaten insgesamt' Spalte
# Entfernen von Punkt als Tausendertrennzeichen und Ersetzen von Komma durch nichts
# Falls Ihre Daten Dezimalstellen hätten, müssten Sie entsprechend anpassen
df['Straftaten insgesamt'] = df['Straftaten insgesamt'].astype(str).str.replace('.', '', regex=False).str.replace(',', '').astype(int)

# Sortieren des DataFrames nach 'Straftaten insgesamt' in absteigender Reihenfolge
df_sortiert = df.sort_values(by='Straftaten insgesamt', ascending=False)

# Zurücksetzen des Indexes nach dem Sortieren
df_sortiert.reset_index(drop=True, inplace=True)

# Anzeige des sortierten DataFrames
print(df_sortiert[['Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']])

# Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
df_sortiert.to_excel('Fallzahlen_2023_sortiert.xlsx', sheet_name='Sortiert', index=False)