import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

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

# Generiere die Liste der Sheet-Namen Fallzahlen_2014 bis Fallzahlen_2023
jahre = range(2014, 2024)
sheet_names = [f'Fallzahlen_{jahr}' for jahr in jahre]

# Liste zur Speicherung der einzelnen DataFrames
df_list = []

# Iteriere über alle Sheet-Namen und lese die Daten
for sheet in sheet_names:
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df_list.append(df)
        print(f'Sheet {sheet} erfolgreich gelesen.')
    except Exception as e:
        print(f'Fehler beim Lesen des Sheets {sheet}: {e}')

# Zusammenführen aller DataFrames in einen einzigen DataFrame
combined_df = pd.concat(df_list, ignore_index=True)
print('Alle Sheets wurden erfolgreich zusammengeführt.')

# Anzeige der Spalten zur Überprüfung (optional)
# print(combined_df.columns)

# Filtern der Unterbezirke:
# - Entfernen der Oberbezirke
# - Entfernen von Zeilen, die "nicht zuzuordnen" enthalten

# Bedingung für Unterbezirke:
# - 'Bezeichnung (Bezirksregion)' ist nicht in der Liste der Oberbezirke
# - 'Bezeichnung (Bezirksregion)' enthält nicht 'nicht zuzuordnen' (case insensitive)

filtered_df = combined_df[
    (~combined_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)) &
    (~combined_df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', case=False, na=False))
]

print(f'Anzahl der Zeilen nach Filtern: {filtered_df.shape[0]}')

# Sicherstellen, dass die Spalte 'Straftaten -insgesamt-' numerisch ist
# Entfernen von Tausenderpunkten und Umwandeln in Integer
filtered_df['Straftaten -insgesamt-'] = filtered_df['Straftaten -insgesamt-'].astype(str).str.replace('.', '').astype(int)

# Aggregieren der Straftaten pro Unterbezirk über alle Jahre hinweg
aggregated_df = filtered_df.groupby('Bezeichnung (Bezirksregion)', as_index=False)['Straftaten -insgesamt-'].sum()

# Sortieren nach der aggregierten Anzahl der Straftaten in absteigender Reihenfolge
sorted_df = aggregated_df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Auswahl der Top 10 Unterbezirke mit den meisten Straftaten
top_10_df = sorted_df.head(10)

# Auswahl der gewünschten Spalten
final_df = top_10_df[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']]

# Optional: Umbenennen der Spalten für bessere Verständlichkeit
final_df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Unterbezirk',
    'Straftaten -insgesamt-': 'Gesamtstraftaten'
}, inplace=True)

# Anzeige des finalen DataFrames
print('Top 10 Unterbezirke mit den meisten Straftaten:')
print(final_df)

# Optional: Speichern des finalen DataFrames in eine neue Excel-Datei
# final_df.to_excel('Top_10_Unterbezirke_Straftaten.xlsx', index=False)