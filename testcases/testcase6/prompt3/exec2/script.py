import pandas as pd

# Schritt 1: Definieren Sie den Dateipfad und die relevanten Sheetnamen
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'
jahre = range(2014, 2024)  # 2014 bis 2023 inclusive
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in jahre]

# Schritt 2: Lesen Sie alle Sheets ein und speichern Sie sie in separaten DataFrames
dataframes = {}
for sheet in sheet_namen:
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        dataframes[sheet] = df
        print(f"Sheet '{sheet}' erfolgreich gelesen.")
    except Exception as e:
        print(f"Fehler beim Lesen des Sheets '{sheet}': {e}")

# Prüfen, ob alle Sheets erfolgreich gelesen wurden
if len(dataframes) != len(sheet_namen):
    print("Nicht alle Sheets wurden erfolgreich gelesen. Bitte überprüfen Sie die Sheetnamen und die Excel-Datei.")
    exit()

# Schritt 3: Fügen Sie alle DataFrames zu einem einzigen DataFrame zusammen
gesamt_df = pd.concat(dataframes.values(), ignore_index=True)
print("Alle Sheets wurden erfolgreich zu einem einzigen DataFrame zusammengeführt.")

# Schritt 4: Definieren Sie die Oberbezirke
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

# Schritt 5: Definieren Sie die Ausschlusskriterien
ausschlusskriterien = oberbezirke + [
    'Berlin (PKS gesamt)',
    'Stadt Berlin, nicht zuzuordnen',
    'Bezirk (Rd), nicht zuzuordnen',
    'Stadtgebiet Berlin, nicht zuzuordnen'
]

# Schritt 6: Filtern Sie die DataFrame, um nur Unterbezirke zu behalten
unterbezirke_df = gesamt_df[~gesamt_df['Bezeichnung (Bezirksregion)'].isin(ausschlusskriterien)]
print(f"Anzahl der verbleibenden Unterbezirke: {unterbezirke_df['Bezeichnung (Bezirksregion)'].nunique()}")

# Schritt 7: Summieren Sie die Straftaten pro Unterbezirk über alle Jahre hinweg
# Stellen Sie sicher, dass die Spalte 'Straftaten \n-insgesamt-' numerisch ist
unterbezirke_df['Straftaten \n-insgesamt-'] = pd.to_numeric(unterbezirke_df['Straftaten \n-insgesamt-'], errors='coerce')

# Gruppieren nach 'Bezeichnung (Bezirksregion)' und summieren
straftaten_summe = unterbezirke_df.groupby('Bezeichnung (Bezirksregion)')['Straftaten \n-insgesamt-'].sum().reset_index()

# Schritt 8: Sortieren Sie die Unterbezirke nach der aggregierten Anzahl an Straftaten absteigend
straftaten_sortiert = straftaten_summe.sort_values(by='Straftaten \n-insgesamt-', ascending=False)

# Schritt 9: Wählen Sie die Top 10 Unterbezirke mit den höchsten Gesamtstraftaten aus
top10_unterbezirke = straftaten_sortiert.head(10)

# Schritt 10: Erstellen Sie den finalen DataFrame mit den gewünschten Spalten
finaler_df = top10_unterbezirke[['Bezeichnung (Bezirksregion)', 'Straftaten \n-insgesamt-']]

# Schritt 11: Ausgabe des finalen DataFrames
print("\nTop 10 Unterbezirke mit den höchsten Gesamtstraftaten:")
print(finaler_df.to_string(index=False))