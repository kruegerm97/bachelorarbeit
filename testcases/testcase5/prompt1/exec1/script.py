import pandas as pd

# Liste der Oberbezirke in Berlin
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

def get_oberbezirk(bezeichnung):
    """
    Bestimmt den Oberbezirk basierend auf der Bezeichnung des Bezirks.
    """
    for oberbezirk in oberbezirke:
        if bezeichnung.startswith(oberbezirk):
            return oberbezirk
    return None  # Rückgabe von None, wenn kein Oberbezirk gefunden wird

def main():
    # Pfad zur Excel-Datei
    datei_pfad = 'Fallzahlen&HZ 2014-2023.xlsx'
    
    try:
        # Einlesen des spezifischen Sheets
        df = pd.read_excel(datei_pfad, sheet_name='Fallzahlen_2023')
    except FileNotFoundError:
        print(f"Die Datei '{datei_pfad}' wurde nicht gefunden.")
        return
    except ValueError:
        print("Das Sheet 'Fallzahlen_2023' existiert nicht in der Excel-Datei.")
        return

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    notwendige_spalten = ['Bezeichnung (Bezirksregion)', 'Raub']
    for spalte in notwendige_spalten:
        if spalte not in df.columns:
            print(f"Die Spalte '{spalte}' ist in den Daten nicht vorhanden.")
            return

    # Hinzufügen einer neuen Spalte für den Oberbezirk
    df['Oberbezirk'] = df['Bezeichnung (Bezirksregion)'].apply(get_oberbezirk)

    # Entfernen von Einträgen, die keinem Oberbezirk zugeordnet werden können
    df = df.dropna(subset=['Oberbezirk'])

    # Gruppieren nach Oberbezirk und Finden des Unterbezirks mit den meisten Raubdelikten
    top_unterbezirke = df.loc[df.groupby('Oberbezirk')['Raub'].idxmax()][['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']]

    # Ausgabe der Ergebnisse
    print("Unterbezirk mit den meisten Raubdelikten pro Oberbezirk (2023):\n")
    for index, row in top_unterbezirke.iterrows():
        oberbezirk = row['Oberbezirk']
        unterbezirk = row['Bezeichnung (Bezirksregion)']
        raub = row['Raub']
        print(f"Oberbezirk: {oberbezirk}")
        print(f"  Unterbezirk: {unterbezirk}")
        print(f"  Anzahl Raubdelikte: {raub}\n")

if __name__ == "__main__":
    main()