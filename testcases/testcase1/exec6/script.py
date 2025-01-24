import pandas as pd

# Datei einlesen
# Da die Zahlen mit Kommas als Tausendertrennzeichen formatiert sind, müssen wir das beim Einlesen berücksichtigen.
# Außerdem gibt es mehrzeilige Header, die wir überspringen müssen.

# Definiere die Anzahl der zu überspringenden Header-Zeilen
skiprows = 4  # Anpassen, falls mehr oder weniger Zeilen übersprungen werden müssen

# Lese die CSV-Datei ein
df = pd.read_csv(
    'FZ_2023.csv',
    sep=',',
    skiprows=skiprows,
    encoding='utf-8',
    dtype=str  # Zunächst alle Daten als String einlesen
)

# Anzeigen der ersten Zeilen zur Überprüfung
#print(df.head())

# Benenne die Spalten um, um leichter darauf zugreifen zu können
df.columns = [
    'LOR-Schlüssel (Bezirksregion)',
    'Bezeichnung (Bezirksregion)',
    'Straftaten - insgesamt-',
    'Raub',
    'Straßenraub, Handtaschen-raub',
    'Körper-verletzungen - insgesamt-',
    'Gefährl. und schwere Körper-verletzung',
    'Freiheits-beraubung, Nötigung, Bedrohung, Nachstellung',
    'Diebstahl - insgesamt-',
    'Diebstahl von Kraftwagen',
    'Diebstahl an/aus Kfz',
    'Fahrrad-diebstahl',
    'Wohnraum-einbruch',
    'Branddelikte - insgesamt-',
    'Brand-stiftung',
    'Sach-beschädigung - insgesamt-',
    'Sach-beschädigung durch Graffiti',
    'Rauschgift-delikte',
    'Kieztaten'
]

# Entferne eventuell zusätzliche Leerzeilen oder nicht relevante Zeilen
df = df.dropna(subset=['Bezeichnung (Bezirksregion)'])

# Entferne Anführungszeichen und Punkte, falls vorhanden, und ersetze Kommas in Zahlen
numeric_columns = ['Straftaten - insgesamt-']

for col in numeric_columns:
    df[col] = df[col].str.replace('"', '').str.replace('.', '').str.replace(',', '').astype(int)

# Sortiere die Bezirke nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
df_sorted = df.sort_values(by='Straftaten - insgesamt-', ascending=False)

# Wähle relevante Spalten für die Ausgabe
output_df = df_sorted[['Bezeichnung (Bezirksregion)', 'Straftaten - insgesamt-']]

# Zeige die sortierte Liste an
print(output_df.to_string(index=False))