import pandas as pd

# 1. Alle Sheets einlesen und in separaten DataFrames speichern
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in range(2014, 2024)]  # 2014 bis 2023

# Dictionary zur Speicherung der DataFrames
dataframes = {}

for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        dataframes[sheet] = df
    except Exception as e:
        print(f"Fehler beim Lesen des Sheets {sheet}: {e}")

# 2. Alle DataFrames zu einem einzigen zusammenführen
gesamtdf = pd.concat(dataframes.values(), ignore_index=True)

# 3. Oberbezirke definieren
oberbezirke = [
    'Mitte', 'Friedrichshain-Kreuzberg', 'Pankow', 'Charlottenburg-Wilmersdorf',
    'Spandau', 'Steglitz-Zehlendorf', 'Tempelhof-Schöneberg', 'Neukölln',
    'Treptow-Köpenick', 'Marzahn-Hellersdorf', 'Lichtenberg', 'Reinickendorf'
]

# 4. Zeilen entfernen, die Oberbezirke, 'Berlin (PKS gesamt)', 'Stadt Berlin, nicht zuzuordnen' oder ähnliche enthalten
begrenzende_werte = oberbezirke + ['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen', 'Bezirk (Rd), nicht zuzuordnen']

# Annahme: Spaltenname genau 'Bezeichnung (Bezirksregion)'
unterbezirk_df = gesamtdf[~gesamtdf['Bezeichnung (Bezirksregion)'].isin(begrenzende_werte)].copy()

# 5. Straftaten insgesamt über alle Jahre summieren
# Beachten Sie den genauen Spaltennamen, eventuell mit Zeilenumbruch und Bindestrich
# Um den Spaltennamen sicher zu erfassen, können wir nach einer Teilübereinstimmung suchen
# Alternativ den exakten Spaltennamen verwenden, wie im Beispiel 'Straftaten \n-insgesamt-'

# Finden des exakten Spaltennamens
spaltennamen = unterbezirk_df.columns
straftaten_spalte = [spalte for spalte in spaltennamen if 'Straftaten' in spalte and 'insgesamt' in spalte]
if not straftaten_spalte:
    raise ValueError("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")
straftaten_spalte = straftaten_spalte[0]

# Gruppieren nach Unterbezirk und Summieren der Straftaten
aggregiert = unterbezirk_df.groupby('Bezeichnung (Bezirksregion)')[straftaten_spalte].sum().reset_index()

# 6. Sortieren der Unterbezirke absteigend nach Straftaten
aggregiert_sortiert = aggregiert.sort_values(by=straftaten_spalte, ascending=False)

# 7. Top 10 Unterbezirke auswählen
top_10 = aggregiert_sortiert.head(10)

# 8. Neuer DataFrame mit den gewünschten Spalten
final_df = top_10[['Bezeichnung (Bezirksregion)', straftaten_spalte]].copy()

# Optional: Spalten umbenennen für Klarheit
final_df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Unterbezirk',
    straftaten_spalte: 'Gesamte Straftaten'
}, inplace=True)

# 9. Finalen DataFrame ausgeben
print(final_df)