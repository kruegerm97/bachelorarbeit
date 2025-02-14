import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Liste der Oberbezirke
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow', 'Charlottenburg-Wilmersdorf',
    'Spandau', 'Steglitz-Zehlendorf', 'Tempelhof-Schöneberg', 'Neukölln',
    'Treptow-Köpenick', 'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# Liste der relevanten Sheet-Namen
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in range(2014, 2024)]

# Alle relevanten Sheets einlesen und in eine Liste von DataFrames speichern
daten_list = []
for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        daten_list.append(df)
    except Exception as e:
        print(f"Fehler beim Lesen des Sheets {sheet}: {e}")

# Alle DataFrames zu einem einzigen DataFrame zusammenführen
gesamt_df = pd.concat(daten_list, ignore_index=True)

# Anzeige der Spaltennamen zur Überprüfung (optional)
# print(gesamt_df.columns)

# Filtern der Unterbezirke:
# - Ausschließen der Oberbezirke
# - Ausschließen von nicht zugeordneten Zeilen
filtered_df = gesamt_df[
    (~gesamt_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)) &
    (~gesamt_df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', case=False, na=False))
]

# Sicherstellen, dass die 'Straftaten -insgesamt-' Spalte numerisch ist
filtered_df['Straftaten -insgesamt-'] = pd.to_numeric(filtered_df['Straftaten -insgesamt-'], errors='coerce')

# Entfernen von Zeilen mit NaN in 'Straftaten -insgesamt-'
filtered_df = filtered_df.dropna(subset=['Straftaten -insgesamt-'])

# Aggregieren der Straftaten pro Unterbezirk
aggregiert_df = filtered_df.groupby('Bezeichnung (Bezirksregion)')['Straftaten -insgesamt-'].sum().reset_index()

# Top 10 Unterbezirke mit den meisten Straftaten
top_10_df = aggregiert_df.sort_values(by='Straftaten -insgesamt-', ascending=False).head(10)

# Optional: Zur besseren Darstellung sortieren
top_10_df = top_10_df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Finale Ausgabe
print("Top 10 Unterbezirke mit den meisten Straftaten:")
print(top_10_df)

# Optional: Speichern des Ergebnisses in eine neue Excel-Datei
# top_10_df.to_excel('Top_10_Unterbezirke_Straftaten.xlsx', index=False)