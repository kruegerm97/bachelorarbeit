import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Laden des Sheets in einen DataFrame
try:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"Die Datei '{excel_file}' wurde nicht gefunden.")
    exit(1)
except ValueError:
    print(f"Das Sheet '{sheet_name}' existiert nicht in der Datei.")
    exit(1)

# Überprüfen der relevanten Spalten
required_columns = [
    'LOR-Schlüssel (Bezirksregion)',
    'Bezeichnung (Bezirksregion)',
    'Raub'
]

for col in required_columns:
    if col not in df.columns:
        print(f"Die erforderliche Spalte '{col}' ist im Sheet nicht vorhanden.")
        exit(1)

# Entfernen von Zeilen, die nicht zugeordnet sind (optional)
# Angenommen, LOR-Schlüssel '129900', '999900', '999999' sind nicht zuzuordnen
invalid_keys = ['129900', '999900', '999999']
df = df[~df['LOR-Schlüssel (Bezirksregion)'].astype(str).str.startswith(tuple(invalid_keys))]

# Extrahieren des Oberbezirkscodes (angenommen, die ersten 2 Stellen)
df['Oberbezirk_Code'] = df['LOR-Schlüssel (Bezirksregion)'].astype(str).str[:2]

# Optional: Mapping der Oberbezirk-Codes zu Namen
# Dies muss entsprechend deiner Daten angepasst werden
oberbezirk_mapping = {
    '10': 'Mitte',
    '11': 'Pankow',
    '12': 'Charlottenburg-Wilmersdorf',
    '13': 'Friedrichshain-Kreuzberg',
    '14': 'Lichtenberg',
    '15': 'Marzahn-Hellersdorf',
    '16': 'Treptow-Köpenick',
    '17': 'Tempelhof-Schöneberg',
    '18': 'Neukölln',
    '19': 'Steglitz-Zehlendorf',
    # Füge weitere Codes und Namen hinzu, falls vorhanden
}

df['Oberbezirk'] = df['Oberbezirk_Code'].map(oberbezirk_mapping)

# Überprüfen auf fehlende Zuordnungen
missing_mapping = df[df['Oberbezirk'].isna()]['Oberbezirk_Code'].unique()
if len(missing_mapping) > 0:
    print("Warnung: Einige Oberbezirk-Codes konnten nicht zugeordnet werden:", missing_mapping)
    # Optional: Weiterverarbeiten oder Abbruch
    # exit(1)

# Gruppieren nach Oberbezirk und Finden des Unterbezirks mit den meisten Raubdelikten
result = df.loc[df.groupby('Oberbezirk')['Raub'].idxmax()][['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']]

# Sortieren nach Oberbezirk
result = result.sort_values('Oberbezirk')

# Ergebnis anzeigen
print("Unterbezirk mit den meisten Raubdelikten pro Oberbezirk:")
print(result.to_string(index=False))

# Optional: Ergebnis in eine neue Excel-Datei speichern
output_file = 'Meiste_Raubdelikte_pro_Oberbezirk.xlsx'
result.to_excel(output_file, index=False)
print(f"\nDas Ergebnis wurde in '{output_file}' gespeichert.")