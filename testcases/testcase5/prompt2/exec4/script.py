import pandas as pd

def find_top_raub_unterbezirke(excel_file, sheet_name):
    """
    Liest die Daten aus dem angegebenen Excel-Sheet und ermittelt für jeden Oberbezirk
    den Unterbezirk mit den meisten Raubdelikten.
    
    :param excel_file: Pfad zur Excel-Datei
    :param sheet_name: Name des Sheets, das ausgelesen werden soll
    :return: Dictionary mit Oberbezirken als Schlüsseln und den entsprechenden
             Unterbezirken mit den meisten Raubdelikten als Werten
    """
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
        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{excel_file}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return

    # Die letzten zwei Zeilen entfernen (Gesamtwerte)
    df = df.iloc[:-2].reset_index(drop=True)
    
    # Initialisiere ein Dictionary, um die Unterbezirke für jeden Oberbezirk zu speichern
    oberbezirk_dict = {ober: [] for ober in oberbezirke}
    
    current_oberbezirk = None
    
    # Durchlaufe jede Zeile des DataFrames
    for idx, row in df.iterrows():
        bezirk_name = row['Bezeichnung (Bezirksregion)']
        
        if bezirk_name in oberbezirke:
            # Aktuellen Oberbezirk setzen
            current_oberbezirk = bezirk_name
            continue  # Weiter zur nächsten Zeile
        
        # Wenn kein aktueller Oberbezirk gesetzt ist, überspringe die Zeile
        if current_oberbezirk is None:
            continue
        
        # Extrahiere den Raub-Wert
        raub_count = row.get('Raub')
        
        # Überprüfen, ob der Raub-Wert gültig ist
        if pd.isna(raub_count):
            raub_count = 0  # Oder eine andere Standardbehandlung
        
        # Füge den Unterbezirk und den Raub-Wert dem aktuellen Oberbezirk hinzu
        unterbezirk = {
            'Name': bezirk_name,
            'Raub': raub_count
        }
        oberbezirk_dict[current_oberbezirk].append(unterbezirk)
    
    # Ergebnis-Dictionary, das die Top-Unterbezirke speichert
    top_unterbezirke = {}
    
    for ober, unterbezirke in oberbezirk_dict.items():
        if not unterbezirke:
            top_unterbezirke[ober] = None
            continue
        
        # Finde den Unterbezirk mit den meisten Raubdelikten
        top_unter = max(unterbezirke, key=lambda x: x['Raub'])
        top_unterbezirke[ober] = top_unter
    
    return top_unterbezirke

def main():
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'
    
    # Name des Sheets
    sheet_name = 'Fallzahlen_2023'
    
    # Finde die Top-Unterbezirke
    top_unterbezirke = find_top_raub_unterbezirke(excel_file, sheet_name)
    
    if not top_unterbezirke:
        print("Keine Daten gefunden oder ein Fehler ist aufgetreten.")
        return
    
    # Ausgabe der Ergebnisse
    print("Unterbezirke mit den meisten Raubdelikten pro Oberbezirk:\n")
    for ober, unter in top_unterbezirke.items():
        if unter:
            print(f"Oberbezirk: {ober}")
            print(f"  Unterbezirk: {unter['Name']}")
            print(f"  Raubdelikte: {unter['Raub']}\n")
        else:
            print(f"Oberbezirk: {ober} hat keine Unterbezirke oder keine Raubdelikte.\n")

if __name__ == "__main__":
    main()