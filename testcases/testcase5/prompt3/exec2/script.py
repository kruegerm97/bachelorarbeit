import pandas as pd

# 1. Die Daten des Sheets 'Fallzahlen_2023' auslesen
file_path = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# 2. Die Daten in einem Pandas Dataframe speichern
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 3. Das Dataframe auf die notwendigen Spalten reduzieren: 'Bezeichnung (Bezirksregion)' und 'Raub'
df = df[['Bezeichnung (Bezirksregion)', 'Raub']]

# 4. Unnötige Zeilen entfernen: Die letzten zwei Zeilen der Tabelle sind Gesamtwerte und sollen entfernt werden.
df = df.iloc[:-2]

# 5. Die Oberbezirke in der Spalte 'Bezeichnung (Bezirksregion)' identifizieren
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

# Erstellen einer neuen Spalte 'Oberbezirk', die den aktuellen Oberbezirk enthält
df['Oberbezirk'] = df['Bezeichnung (Bezirksregion)'].where(df['Bezeichnung (Bezirksregion)'].isin(oberbezirke))
df['Oberbezirk'] = df['Oberbezirk'].ffill()

# 6. Die Unterbezirke identifizieren, indem Oberbezirke selbst ausgeschlossen werden
df_unter = df[~df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)].copy()

# Sicherstellen, dass die 'Raub'-Spalte numerisch ist
df_unter['Raub'] = pd.to_numeric(df_unter['Raub'], errors='coerce')

# Entfernen von Zeilen mit fehlenden 'Raub'-Werten
df_unter = df_unter.dropna(subset=['Raub'])

# Für jeden Oberbezirk den Unterbezirk mit dem höchsten Wert in der Spalte 'Raub' identifizieren
idx_max_raub = df_unter.groupby('Oberbezirk')['Raub'].idxmax()
df_max_raub = df_unter.loc[idx_max_raub]

# 7. Die Ergebnisse in einem neuen Dataframe speichern mit den Spalten: 'Oberbezirk', 'Unterbezirk', 'Raub'
final_df = df_max_raub[['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']].rename(columns={
    'Bezeichnung (Bezirksregion)': 'Unterbezirk'
}).reset_index(drop=True)

# 8. Das finale Dataframe ausgeben
print(final_df)