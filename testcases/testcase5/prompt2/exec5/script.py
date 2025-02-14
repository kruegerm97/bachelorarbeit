import pandas as pd

# Definiere den Dateipfad und den Sheet-Namen
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'
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

# Lese das Excel-Sheet ein
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Entferne die letzten zwei Zeilen (Gesamtwerte)
df = df.iloc[:-2].reset_index(drop=True)

# Bereinige die Spaltennamen (entferne Zeilenumbrüche und Leerzeichen)
df.columns = df.columns.str.replace('\n', ' ').str.strip()

# Stelle sicher, dass die 'Raub' Spalte numerisch ist
df['Raub'] = pd.to_numeric(df['Raub'], errors='coerce')

# Initialisiere ein Dictionary, um die Ergebnisse zu speichern
ergebnisse = {}

# Variable, um den aktuellen Oberbezirk zu verfolgen
aktueller_oberbezirk = None

# Iteriere über die DataFrame-Zeilen
for index, row in df.iterrows():
    bezirk_bezeichnung = row['Bezeichnung (Bezirksregion)']
    
    if bezirk_bezeichnung in oberbezirke:
        # Aktuellen Oberbezirk setzen
        aktueller_oberbezirk = bezirk_bezeichnung
        # Initialisiere eine Liste für die Unterbezirke des aktuellen Oberbezirks
        ergebnisse[aktueller_oberbezirk] = []
    else:
        if aktueller_oberbezirk:
            # Füge den Unterbezirk zu der Liste des aktuellen Oberbezirks hinzu
            ergebnisse[aktueller_oberbezirk].append({
                'Unterbezirk': bezirk_bezeichnung,
                'Raub': row['Raub']
            })

# Jetzt finde für jeden Oberbezirk den Unterbezirk mit den meisten Raubdelikten
for oberbezirk, unterbezirk_list in ergebnisse.items():
    if not unterbezirk_list:
        print(f"Oberbezirk '{oberbezirk}' hat keine Unterbezirke.")
        continue
    
    # Finde den Unterbezirk mit dem maximalen Raub-Wert
    max_raub_unterbezirk = max(unterbezirk_list, key=lambda x: x['Raub'])
    
    print(f"Oberbezirk: {oberbezirk}")
    print(f"  Unterbezirk mit den meisten Raubdelikten: {max_raub_unterbezirk['Unterbezirk']} ({max_raub_unterbezirk['Raub']} Raubdelikte)")
    print()