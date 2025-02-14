import pandas as pd

# 1. Definiere den Dateinamen
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

# 2. Liste der Oberbezirke
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow', 'Charlottenburg-Wilmersdorf',
    'Spandau', 'Steglitz-Zehlendorf', 'Tempelhof-Schöneberg', 'Neukölln',
    'Treptow-Köpenick', 'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# 3. Lese alle Sheets ein und speichere sie in einer Liste von DataFrames
# Annahme: Die Sheets heißen 'Fallzahlen_2014' bis 'Fallzahlen_2023'
jahre = range(2014, 2024)
dataframes = []

for jahr in jahre:
    sheet_name = f'Fallzahlen_{jahr}'
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df['Jahr'] = jahr  # Füge eine Spalte für das Jahr hinzu
        dataframes.append(df)
    except Exception as e:
        print(f"Fehler beim Lesen des Sheets '{sheet_name}': {e}")

# 4. Füge alle DataFrames zu einem einzigen DataFrame zusammen
gesamt_df = pd.concat(dataframes, ignore_index=True)

# 5. Entferne Zeilen, die Oberbezirke, 'Berlin (PKS gesamt)' oder nicht zuzuordnende Einträge enthalten
# Definiere die Namen der nicht zuzuordnenden Einträge
nicht_zugeordnet = [
    'Bezirk (Rd), nicht zuzuordnen',
    'Stadtgebiet Berlin, nicht zuzuordnen',
    'Berlin (PKS gesamt)'
]

# Filtere die DataFrame, um nur Unterbezirke zu behalten
unterbezirk_df = gesamt_df[~gesamt_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke + nicht_zugeordnet)]

# 6. Summiere die Straftaten über alle Jahre hinweg für jeden Unterbezirk
# Achte auf den genauen Spaltennamen, möglicherweise enthält er einen Zeilenumbruch
# Daher benutze hier eine Rohzeichenkette oder ersetze Zeilenumbrüche
straftaten_spalte = 'Straftaten \n-insgesamt-'  # Anpassung basierend auf dem Beispiel

# Überprüfe, ob die Spalte existiert
if straftaten_spalte not in unterbezirk_df.columns:
    # Alternativ Zeilenumbrüche entfernen und erneut versuchen
    unterbezirk_df.columns = unterbezirk_df.columns.str.replace('\n', ' ', regex=True)
    strafftaten_spalte = 'Straftaten  -insgesamt-'
    if strafftaten_spalte not in unterbezirk_df.columns:
        raise ValueError(f"Die Spalte '{straftaten_spalte}' wurde nicht gefunden.")

# Gruppiere nach Unterbezirk und summiere die Straftaten
aggregierte_straftaten = unterbezirk_df.groupby('Bezeichnung (Bezirksregion)')[straftaten_spalte].sum()

# 7. Sortiere die Unterbezirke absteigend nach den Straftaten
sortierte_straftaten = aggregierte_straftaten.sort_values(ascending=False)

# 8. Wähle die Top 10 Unterbezirke mit den höchsten Straftaten
top_10_unterbezirke = sortierte_straftaten.head(10)

# 9. Erstelle einen neuen DataFrame mit den Top 10 Unterbezirken und ihren Straftaten
final_df = top_10_unterbezirke.reset_index()
final_df.columns = ['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']

# 10. Gib den finalen DataFrame aus
print(final_df)