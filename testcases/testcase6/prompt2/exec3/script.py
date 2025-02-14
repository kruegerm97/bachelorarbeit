import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Liste der Oberbezirke, die ausgeschlossen werden sollen
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow',
    'Charlottenburg-Wilmersdorf', 'Spandau', 'Steglitz-Zehlendorf',
    'Tempelhof-Schöneberg', 'Neukölln', 'Treptow-Köpenick',
    'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# Erstellen einer Liste der Sheet-Namen von 2014 bis 2023
jahreszahlen = range(2014, 2024)  # 2014 bis 2023 inklusive
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in jahreszahlen]

# Lesen aller relevanten Sheets und Speichern in einer Liste von DataFrames
dataframes = []
for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet, engine='openpyxl')
        dataframes.append(df)
        print(f"Sheet '{sheet}' erfolgreich gelesen.")
    except Exception as e:
        print(f"Fehler beim Lesen von Sheet '{sheet}': {e}")

# Zusammenführen aller DataFrames zu einem einzigen DataFrame
if dataframes:
    kombiniertes_df = pd.concat(dataframes, ignore_index=True)
    print("Alle Sheets erfolgreich zusammengeführt.")
else:
    raise ValueError("Keine Daten zum Verarbeiten gefunden.")

# Überprüfen der Spaltennamen
print("Spaltennamen im kombinierten DataFrame:")
print(kombiniertes_df.columns.tolist())

# Bereinigung der Spaltennamen (Entfernen von Zeilenumbrüchen und Leerzeichen)
kombiniertes_df.columns = kombiniertes_df.columns.str.replace('\n', ' ', regex=True).str.strip()

# Überprüfen der bereinigten Spaltennamen
print("Bereinigte Spaltennamen:")
print(kombiniertes_df.columns.tolist())

# Filtern der Unterbezirke (Ausschließen der Oberbezirke und nicht zugeordneten Einträge)
unterbezirke_df = kombiniertes_df[~kombiniertes_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)]
print(f"Anzahl der Unterbezirke nach Filter: {unterbezirke_df.shape[0]}")

# Weitere Filterung: Entfernen von nicht zugeordneten Zeilen
# Angenommen, nicht zugeordnete Zeilen enthalten bestimmte Schlüsselwörter
nicht_zugeordnet_keywords = ['nicht zuzuordnen', 'Berlin (PKS gesamt)']
unterbezirke_df = unterbezirke_df[~unterbezirke_df['Bezeichnung (Bezirksregion)'].str.contains('|'.join(nicht_zugeordnet_keywords), case=False, na=False)]
print(f"Anzahl der Unterbezirke nach Entfernen nicht zugeordneter Zeilen: {unterbezirke_df.shape[0]}")

# Sicherstellen, dass die Spalte 'Straftaten -insgesamt-' vorhanden ist
straftaten_spalte = 'Straftaten -insgesamt-'
if straftaten_spalte not in unterbezirke_df.columns:
    raise ValueError(f"Die Spalte '{straftaten_spalte}' wurde nicht gefunden. Bitte überprüfen Sie die Spaltennamen.")

# Gruppieren nach Unterbezirk und Summieren der Straftaten
aggregiertes_df = unterbezirke_df.groupby('Bezeichnung (Bezirksregion)')[straftaten_spalte].sum().reset_index()

# Sortieren nach der Anzahl der Straftaten in absteigender Reihenfolge
aggregiertes_df = aggregiertes_df.sort_values(by=straftaten_spalte, ascending=False)

# Auswahl der Top 10 Unterbezirke mit den meisten Straftaten
top10_df = aggregiertes_df.head(10)

# Finale Darstellung mit nur den gewünschten Spalten
final_df = top10_df[['Bezeichnung (Bezirksregion)', strafftaten_spalte]]

# Ausgabe des finalen DataFrames
print("Top 10 Unterbezirke mit den meisten Straftaten:")
print(final_df)

# Optional: Speichern des finalen DataFrames in eine neue Excel-Datei
final_df.to_excel('Top10_Unterbezirke_Straftaten.xlsx', index=False)
print("Das finale DataFrame wurde in 'Top10_Unterbezirke_Straftaten.xlsx' gespeichert.")