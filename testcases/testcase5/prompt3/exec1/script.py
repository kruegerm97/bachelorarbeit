import pandas as pd

# Schritt 1: Excel-Datei und Sheet definieren
file_path = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Schritt 2: Daten aus dem Excel-Sheet in ein Pandas DataFrame laden
try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"Die Datei {file_path} wurde nicht gefunden.")
    exit(1)
except ValueError:
    print(f"Das Sheet '{sheet_name}' existiert nicht in der Datei {file_path}.")
    exit(1)

# Schritt 3: Notwendige Spalten auswählen
try:
    df = df[['Bezeichnung (Bezirksregion)', 'Raub']]
except KeyError as e:
    print(f"Die erforderliche Spalte wurde nicht gefunden: {e}")
    exit(1)

# Schritt 4: Die letzten zwei Zeilen entfernen (Gesamtwerte)
df = df.iloc[:-2]

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

# Schritt 6: Oberbezirke identifizieren und Unterbezirke zuweisen
# Eine neue Spalte 'Oberbezirk' erstellen, die nur dann gesetzt ist, wenn die Zeile ein Oberbezirk ist
df['Oberbezirk'] = df['Bezeichnung (Bezirksregion)'].where(df['Bezeichnung (Bezirksregion)'].isin(oberbezirke))

# Die 'Oberbezirk'-Spalte nach unten füllen, sodass jeder Unterbezirk seinen zugehörigen Oberbezirk hat
df['Oberbezirk'] = df['Oberbezirk'].ffill()

# Schritt 7: Unterbezirke aus den Daten filtern (Zeilen, die keine Oberbezirke sind)
df_unterbezirke = df[~df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)].copy()

# Schritt 8: Für jeden Oberbezirk den Unterbezirk mit dem höchsten 'Raub' ermitteln
# Gruppieren nach 'Oberbezirk' und Finden des Index mit maximalem 'Raub' in jeder Gruppe
idx = df_unterbezirke.groupby('Oberbezirk')['Raub'].idxmax()

# Das finale DataFrame erstellen mit den gewünschten Spalten
result_df = df_unterbezirke.loc[idx, ['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']].copy()

# Spalten umbenennen für bessere Lesbarkeit
result_df.rename(columns={'Bezeichnung (Bezirksregion)': 'Unterbezirk'}, inplace=True)

# Schritt 9: Das finale DataFrame ausgeben
print(result_df.reset_index(drop=True))