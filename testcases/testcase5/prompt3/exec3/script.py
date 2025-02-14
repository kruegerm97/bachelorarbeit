import pandas as pd

# Schritt 1: Die Daten des Sheets 'Fallzahlen_2023' auslesen
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Schritt 2: Die Daten in einem Pandas DataFrame speichern
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Schritt 3: Das DataFrame auf die notwendigen Spalten reduzieren
necessary_columns = ['Bezeichnung (Bezirksregion)', 'Raub']
df = df[necessary_columns]

# Schritt 4: Unnötige Zeilen entfernen (letzte zwei Zeilen)
df = df.iloc[:-2].reset_index(drop=True)

# Schritt 5: Die Oberbezirke definieren
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow', 
    'Charlottenburg-Wilmersdorf', 'Spandau', 'Steglitz-Zehlendorf', 
    'Tempelhof-Schöneberg', 'Neukölln', 'Treptow-Köpenick', 
    'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# Hinzufügen einer neuen Spalte zur Identifizierung des aktuellen Oberbezirks
df['Oberbezirk'] = None
current_oberbezirk = None

for index, row in df.iterrows():
    bezirk = row['Bezeichnung (Bezirksregion)']
    if bezirk in oberbezirke:
        current_oberbezirk = bezirk
        df.at[index, 'Oberbezirk'] = current_oberbezirk
    else:
        df.at[index, 'Oberbezirk'] = current_oberbezirk

# Schritt 6: Unterbezirke identifizieren (Zeilen, die keine Oberbezirke sind)
unterbezirke_df = df[~df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)].copy()

# Sicherstellen, dass 'Raub' als numerischer Wert vorliegt
unterbezirke_df['Raub'] = pd.to_numeric(unterbezirke_df['Raub'], errors='coerce')

# Schritt 6: Für jeden Oberbezirk den Unterbezirk mit dem höchsten 'Raub' finden
max_raub_df = unterbezirke_df.loc[unterbezirke_df.groupby('Oberbezirk')['Raub'].idxmax()]

# Schritt 7: Die Ergebnisse in einem neuen DataFrame speichern
final_df = max_raub_df[['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']].rename(
    columns={
        'Bezeichnung (Bezirksregion)': 'Unterbezirk',
        'Raub': 'Raub'
    }
).reset_index(drop=True)

# Schritt 8: Das finale DataFrame ausgeben
print(final_df)