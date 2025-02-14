import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

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

try:
    # Excel-Datei einlesen
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)

    # Entfernen der letzten zwei Zeilen (Gesamtwerte)
    df = df.iloc[:-2]

    # Sicherstellen, dass die relevanten Spalten vorhanden sind
    erforderliche_spalten = ['Bezeichnung (Bezirksregion)', 'Raub']
    for spalte in erforderliche_spalten:
        if spalte not in df.columns:
            raise ValueError(f"Die erforderliche Spalte '{spalte}' wurde nicht gefunden.")

    # Erstellen einer neuen Spalte 'Oberbezirk', die den aktuellen Oberbezirk enthält
    df['Oberbezirk'] = df['Bezeichnung (Bezirksregion)'].where(df['Bezeichnung (Bezirksregion)'].isin(oberbezirke))
    df['Oberbezirk'] = df['Oberbezirk'].ffill()

    # Filtern der Unterbezirke (Ausschluss der Oberbezirke)
    unterbezirke = df[~df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)].copy()

    # Um sicherzustellen, dass die 'Raub' Spalte numerisch ist
    unterbezirke['Raub'] = pd.to_numeric(unterbezirke['Raub'], errors='coerce').fillna(0).astype(int)

    # Gruppieren nach 'Oberbezirk' und Finden des Unterbezirks mit den meisten Raubdelikten
    idx_max_raub = unterbezirke.groupby('Oberbezirk')['Raub'].idxmax()
    max_raub_unterbezirke = unterbezirke.loc[idx_max_raub]

    # Ausgabe der Ergebnisse
    print("Unterbezirk mit den meisten Raubdelikten pro Oberbezirk (2023):\n")
    for _, row in max_raub_unterbezirke.iterrows():
        print(f"Oberbezirk: {row['Oberbezirk']}")
        print(f"  Unterbezirk: {row['Bezeichnung (Bezirksregion)']}")
        print(f"  Anzahl Raubdelikte: {row['Raub']}\n")

except FileNotFoundError:
    print(f"Die Datei '{excel_datei}' wurde nicht gefunden. Bitte überprüfe den Pfad.")
except ValueError as ve:
    print(f"Fehler: {ve}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")