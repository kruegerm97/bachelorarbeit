import pandas as pd

# Dateipfad zur Excel-Datei
file_path = 'Fallzahlen&HZ 2014-2023.xlsx'

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

# Generiere die Liste der Sheet-Namen von 2014 bis 2023
sheet_names = [f'Fallzahlen_{year}' for year in range(2014, 2024)]

# Lese alle relevanten Sheets ein und speichere sie in einer Liste
dfs = []
for sheet in sheet_names:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet)
        dfs.append(df)
    except ValueError:
        print(f"Sheet {sheet} nicht gefunden in der Datei.")

# Kombiniere alle DataFrames zu einem einzigen DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Bereinige die Spaltennamen: Entferne Zeilenumbrüche und führende/trailende Leerzeichen
combined_df.columns = combined_df.columns.str.replace('\n', ' ').str.strip()

# Identifiziere die Spalte für "Straftaten -insgesamt-"
# Diese Annahme basiert auf den bereitgestellten Beispieldaten
straftaten_spalte = 'Straftaten -insgesamt-'

if straftaten_spalte not in combined_df.columns:
    # Falls die Spalte nicht exakt gefunden wird, suche ähnlich benannte Spalten
    mögliche_spalten = [col for col in combined_df.columns if 'Straftaten' in col and 'insgesamt' in col.lower()]
    if mögliche_spalten:
        straftaten_spalte = mögliche_spalten[0]
    else:
        raise ValueError('Die Spalte für "Straftaten -insgesamt-" wurde nicht gefunden.')

# Filtere nur die Unterbezirke:
# - Schließe die Oberbezirke aus
# - Schließe Zeilen aus, die "nicht zuzuordnen" enthalten
unterbezirke_df = combined_df[
    (~combined_df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)) &
    (~combined_df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', case=False, na=False))
]

# Stelle sicher, dass die Straftaten-Spalte numerisch ist
unterbezirke_df[straftaten_spalte] = pd.to_numeric(unterbezirke_df[straftaten_spalte], errors='coerce').fillna(0)

# Aggregiere die Straftaten über alle Jahre hinweg pro Unterbezirk
aggregated_df = unterbezirke_df.groupby('Bezeichnung (Bezirksregion)')[straftaten_spalte].sum().reset_index()

# Ermittele die Top 10 Unterbezirke mit den meisten Straftaten
top10_df = aggregated_df.sort_values(by=straftaten_spalte, ascending=False).head(10)

# Benenne die Spalten für den finalen DataFrame um (optional)
final_df = top10_df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Unterbezirk',
    straftaten_spalte: 'Straftaten_Gesamt'
})

# Optional: Setze die Spalten in eine bestimmte Reihenfolge
final_df = final_df[['Unterbezirk', 'Straftaten_Gesamt']]

# Ausgabe des finalen DataFrames
print(final_df)

# Optional: Speichere das Ergebnis in eine neue Excel-Datei
# final_df.to_excel('Top10_Unterbezirke_Straftaten.xlsx', index=False)