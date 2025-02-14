import pandas as pd

# 1. Definiere den Dateinamen und die zu lesenden Sheets
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'
jahre = list(range(2014, 2024))  # 2014 bis 2023
sheet_names = [f'Fallzahlen_{jahr}' for jahr in jahre]

# 2. Lese alle Sheets ein und speichere sie in einer Liste von DataFrames
dataframes = []
for sheet in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)
    dataframes.append(df)

# 3. Füge alle DataFrames zu einem einheitlichen DataFrame zusammen
all_data = pd.concat(dataframes, ignore_index=True)

# 4. Definiere die Oberbezirke
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow', 'Charlottenburg-Wilmersdorf',
    'Spandau', 'Steglitz-Zehlendorf', 'Tempelhof-Schöneberg', 'Neukölln',
    'Treptow-Köpenick', 'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# Zusätzliche nicht zuzuordnende Einträge
nicht_zuordenbar = [
    'Berlin (PKS gesamt)',
    'Bezirk (Rd), nicht zuzuordnen',
    'Stadtgebiet Berlin, nicht zuzuordnen'
]

# 5. Entferne alle Zeilen, die Oberbezirke oder nicht zuordenbare Einträge enthalten
filtered_data = all_data[~all_data['Bezeichnung (Bezirksregion)'].isin(oberbezirke + nicht_zuordenbar)]

# 6. Entferne weitere allgemeine Einträge, falls vorhanden (optional)
# Falls es noch andere allgemeine Einträge gibt, können diese hier hinzugefügt werden
# Beispielsweise: 'Gesamt Berlin' oder ähnliche

# 7. Aggregiere die Straftaten pro Unterbezirk über alle Jahre hinweg
# Zuerst sicherstellen, dass die Spalte korrekt benannt ist
# Manchmal können Leerzeichen oder Zeilenumbrüche Probleme verursachen

# Liste der möglichen Spaltennamen für 'Straftaten -insgesamt-'
straftaten_spalten = [
    'Straftaten \n-insgesamt-',
    'Straftaten -insgesamt-',
    'Straftaten - insgesamt -'  # Falls es Varianten gibt
]

# Finde die existierende Spalte
straftaten_spalte = None
for col in straftaten_spalten:
    if col in filtered_data.columns:
        straftaten_spalte = col
        break

if not straftaten_spalte:
    raise ValueError("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")

# Gruppiere nach 'Bezeichnung (Bezirksregion)' und summiere die Straftaten
aggregated = filtered_data.groupby('Bezeichnung (Bezirksregion)')[straftaten_spalte].sum().reset_index()

# 8. Sortiere die Unterbezirke absteigend nach der aggregierten Anzahl an Straftaten
aggregated_sorted = aggregated.sort_values(by=straftaten_spalte, ascending=False)

# 9. Wähle die Top 10 Unterbezirke mit den höchsten Gesamtstraftaten aus
top_10 = aggregated_sorted.head(10)

# 10. Erstelle den finalen DataFrame mit den gewünschten Spalten
final_df = top_10[['Bezeichnung (Bezirksregion)', straftaten_spalte]].copy()
final_df = final_df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Unterbezirk',
    straftaten_spalte: 'Gesamtstraftaten'
})

# 11. Ausgabe des finalen DataFrames
print(final_df)