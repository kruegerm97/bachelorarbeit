import pandas as pd

# 1. Definiere den Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# 2. Erstelle eine Liste der Sheet-Namen von 'Fallzahlen_2014' bis 'Fallzahlen_2023'
jahre = range(2014, 2024)  # 2024 ist exklusiv, also bis 2023
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in jahre]

# 3. Lese alle Sheets ein und speichere jedes in einem separaten DataFrame
dataframes = []
for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        dataframes.append(df)
        print(f"Sheet '{sheet}' erfolgreich eingelesen.")
    except Exception as e:
        print(f"Fehler beim Einlesen von Sheet '{sheet}': {e}")

# 4. Füge alle DataFrames zu einem einzigen zusammen
kombinierter_df = pd.concat(dataframes, ignore_index=True)
print("Alle Sheets erfolgreich zu einem DataFrame kombiniert.")

# 5. Definiere die Liste der Oberbezirke
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

# 6. Definiere zusätzliche auszuschließende Einträge
ausschluss_liste = oberbezirke + [
    'Berlin (PKS gesamt)',
    'Stadtgebiet Berlin, nicht zuzuordnen',
    'Bezirk (Rd), nicht zuzuordnen'
]

# 7. Entferne alle Zeilen, die in der Ausschlussliste enthalten sind
unterbezirke_df = kombinierter_df[~kombinierter_df['Bezeichnung (Bezirksregion)'].isin(ausschluss_liste)]
print(f"Anzahl der verbleibenden Unterbezirke: {unterbezirke_df['Bezeichnung (Bezirksregion)'].nunique()}")

# 8. Stelle sicher, dass die Spalte 'Straftaten \n-insgesamt-' numerisch ist
unterbezirke_df['Straftaten \n-insgesamt-'] = pd.to_numeric(unterbezirke_df['Straftaten \n-insgesamt-'], errors='coerce')

# 9. Entferne mögliche NaN-Werte in der Straftaten-Spalte
unterbezirke_df = unterbezirke_df.dropna(subset=['Straftaten \n-insgesamt-'])

# 10. Summiere die Straftaten pro Unterbezirk über alle Jahre hinweg
aggregierte_straftaten = unterbezirke_df.groupby('Bezeichnung (Bezirksregion)')['Straftaten \n-insgesamt-'].sum()

# 11. Sortiere die Unterbezirke absteigend nach der aggregierten Anzahl an Straftaten
sortierte_straftaten = aggregierte_straftaten.sort_values(ascending=False)

# 12. Wähle die Top 10 Unterbezirke mit den höchsten Gesamtstraftaten aus
top_10_unterbezirke = sortierte_straftaten.head(10)

# 13. Erstelle einen neuen DataFrame mit den gewünschten Spalten
finaler_df = top_10_unterbezirke.reset_index()
finaler_df.columns = ['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']

# 14. Gib den finalen DataFrame aus
print("\nTop 10 Unterbezirke mit den höchsten Gesamtstraftaten:")
print(finaler_df)