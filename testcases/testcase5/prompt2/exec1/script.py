import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Oberbezirke-Liste
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

# Daten aus dem Excel-Sheet auslesen
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Letzte zwei Zeilen (Gesamtwerte) entfernen
df = df.iloc[:-2].reset_index(drop=True)

# Spaltennamen anpassen, falls nötig (Beispiel: Leerzeichen entfernen)
df.columns = [col.strip() for col in df.columns]

# Liste zur Speicherung der Ergebnisse
ergebnisse = []

# Variable zur Speicherung des aktuellen Oberbezirks
aktueller_oberbezirk = None

# Dictionary zur Speicherung der maximalen Raubdelikte pro Oberbezirk
max_raub_dict = {}

for index, row in df.iterrows():
    bezirk = row['Bezeichnung (Bezirksregion)']
    
    if bezirk in oberbezirke:
        # Neuer Oberbezirk gefunden
        aktueller_oberbezirk = bezirk
    else:
        if aktueller_oberbezirk is not None:
            # Unterbezirk des aktuellen Oberbezirks
            unterbezirk = bezirk
            raub = row['Raub']
            
            # Überprüfen, ob dieser Unterbezirk mehr Raubdelikte hat als vorherige
            if aktueller_oberbezirk not in max_raub_dict:
                max_raub_dict[aktueller_oberbezirk] = {'Unterbezirk': unterbezirk, 'Raub': raub}
            else:
                if raub > max_raub_dict[aktueller_oberbezirk]['Raub']:
                    max_raub_dict[aktueller_oberbezirk] = {'Unterbezirk': unterbezirk, 'Raub': raub}

# Ergebnisse ausgeben
print("Unterbezirk mit den meisten Raubdelikten pro Oberbezirk:")
for oberbezirk in oberbezirke:
    if oberbezirk in max_raub_dict:
        unterbezirk = max_raub_dict[oberbezirk]['Unterbezirk']
        raub = max_raub_dict[oberbezirk]['Raub']
        print(f"{oberbezirk}: {unterbezirk} ({raub} Raubdelikte)")
    else:
        print(f"{oberbezirk}: Keine Unterbezirke gefunden oder keine Daten vorhanden.")