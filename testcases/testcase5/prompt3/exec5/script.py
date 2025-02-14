import pandas as pd

# Schritt 1: Excel-Datei und das spezifische Sheet laden
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Schritt 2: Daten in einem Pandas DataFrame speichern
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Schritt 3: DataFrame auf die notwendigen Spalten reduzieren
selected_columns = ['Bezeichnung (Bezirksregion)', 'Raub']
df = df[selected_columns]

# Schritt 4: Die letzten zwei Zeilen entfernen (Gesamtwerte)
df = df.iloc[:-2].reset_index(drop=True)

# Schritt 5: Liste der Oberbezirke definieren
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

# Initialisierung
results = []
current_oberbezirk = None

# Schritt 6: Durch das DataFrame iterieren und Unterbezirke zuordnen
for index, row in df.iterrows():
    bezirk = row['Bezeichnung (Bezirksregion)']
    raub = row['Raub']
    
    if bezirk in oberbezirke:
        # Aktuellen Oberbezirk setzen
        current_oberbezirk = bezirk
    else:
        if current_oberbezirk:
            # Unterbezirk und Raub-Wert hinzufügen
            results.append({
                'Oberbezirk': current_oberbezirk,
                'Unterbezirk': bezirk,
                'Raub': raub
            })

# In einen neuen DataFrame umwandeln
results_df = pd.DataFrame(results)

# Schritt 6 (Fortsetzung): Für jeden Oberbezirk den Unterbezirk mit dem höchsten 'Raub' finden
max_raub_df = results_df.loc[results_df.groupby('Oberbezirk')['Raub'].idxmax()].reset_index(drop=True)

# Schritt 7: Spalten umbenennen (falls nötig) und finalen DataFrame erstellen
final_df = max_raub_df[['Oberbezirk', 'Unterbezirk', 'Raub']]

# Schritt 8: Finalen DataFrame ausgeben
print(final_df)