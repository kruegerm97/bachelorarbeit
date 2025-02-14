import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Liste der Oberbezirke
oberbezirke = [
    'Mitte',
    'Friedrichshain-Kreuzberg',
    'Pankow',
    'Charlottenburg-Wilmersdorf',
    'Spandau',
    'Steglitz-Zehlendorf',
    'Tempelhof-Schöneberg',
    'Neukölln',
    'Treptow-Köpenick',
    'Marzahn-Hellersdorf',
    'Lichtenberg',
    'Reinickendorf'
]

# Lesen des Excel-Sheets
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Entfernen der letzten zwei Zeilen (Gesamtwerte)
df = df.iloc[:-2].reset_index(drop=True)

# Initialisierung
current_oberbezirk = None
unterbezirke_dict = {ober: [] for ober in oberbezirke}

# Iteration über die Zeilen des DataFrames
for index, row in df.iterrows():
    bezirk_name = row['Bezeichnung (Bezirksregion)']
    
    if bezirk_name in oberbezirke:
        # Aktueller Oberbezirk festlegen
        current_oberbezirk = bezirk_name
    else:
        if current_oberbezirk:
            # Unterbezirk zuweisen
            unterbezirke_dict[current_oberbezirk].append({
                'Bezeichnung': bezirk_name,
                'Raub': row['Raub']
            })
        else:
            # Falls kein Oberbezirk festgelegt ist, überspringen
            continue

# Ermittlung des Unterbezirks mit den meisten Raubdelikten für jeden Oberbezirk
top_unterbezirke = {}

for oberbezirk, unterbezirke in unterbezirke_dict.items():
    if unterbezirke:
        # Finden des Unterbezirks mit dem maximalen 'Raub' Wert
        top_unterbezirk = max(unterbezirke, key=lambda x: x['Raub'])
        top_unterbezirke[oberbezirk] = {
            'Unterbezirk': top_unterbezirk['Bezeichnung'],
            'Raubdelikte': top_unterbezirk['Raub']
        }
    else:
        top_unterbezirke[oberbezirk] = {
            'Unterbezirk': None,
            'Raubdelikte': 0
        }

# Ausgabe der Ergebnisse
print("Unterbezirk mit den meisten Raubdelikten pro Oberbezirk (2023):\n")
for oberbezirk, daten in top_unterbezirke.items():
    unterbezirk = daten['Unterbezirk']
    raub = daten['Raubdelikte']
    if unterbezirk:
        print(f"{oberbezirk}: {unterbezirk} ({raub} Raubdelikte)")
    else:
        print(f"{oberbezirk}: Kein Unterbezirk gefunden.")