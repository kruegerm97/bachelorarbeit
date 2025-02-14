import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

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

# Liste der Sheet-Namen von Fallzahlen_2014 bis Fallzahlen_2023
jahre = list(range(2014, 2024))
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in jahre]

# Leere Liste zur Speicherung der DataFrames
df_list = []

# Iteriere über jedes Sheet und lese die Daten
for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        df_list.append(df)
    except Exception as e:
        print(f"Fehler beim Lesen des Sheets {sheet}: {e}")

# Zusammenführen aller DataFrames
gesamt_df = pd.concat(df_list, ignore_index=True)

# Entfernen der Oberbezirke und nicht zugeordneten Zeilen
# Bedingungen:
# 1. 'Bezeichnung (Bezirksregion)' nicht in oberbezirke
# 2. 'Bezeichnung (Bezirksregion)' enthält nicht 'nicht zuzuordnen'

# Erste Bedingung
bedingung_1 = ~gesamt_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)

# Zweite Bedingung: Ausschließen von Zeilen, die 'nicht zuzuordnen' enthalten
bedingung_2 = ~gesamt_df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', case=False, na=False)

# Anwenden der Bedingungen
unterbezirke_df = gesamt_df[bedingung_1 & bedingung_2]

# Sicherstellen, dass die Spalte 'Straftaten -insgesamt-' numerisch ist
# Eventuell müssen Nicht-Nummerische Werte (z.B. NaN) behandelt werden
unterbezirke_df['Straftaten -insgesamt-'] = pd.to_numeric(unterbezirke_df['Straftaten -insgesamt-'], errors='coerce').fillna(0)

# Aggregieren der Straftaten über alle Jahre hinweg
aggregiert_df = unterbezirke_df.groupby('Bezeichnung (Bezirksregion)')['Straftaten -insgesamt-'].sum().reset_index()

# Sortieren nach absteigender Anzahl der Straftaten und Auswahl der Top 10
top10_df = aggregiert_df.sort_values(by='Straftaten -insgesamt-', ascending=False).head(10)

# Optional: Zurücksetzen des Indexes
top10_df = top10_df.reset_index(drop=True)

# Ausgabe des finalen DataFrames
print(top10_df)

# Optional: Speichern des Ergebnisses in eine neue Excel-Datei
# top10_df.to_excel('Top10_Unterbezirke_Straftaten.xlsx', index=False)