import pandas as pd
import re

def find_district_with_most_crimes(excel_file):
    """
    Liest relevante Sheets aus einer Excel-Datei, summiert die Straftaten pro Bezirk über alle Jahre und gibt den Bezirk mit den meisten Straftaten zurück.
    
    :param excel_file: Pfad zur Excel-Datei
    :return: Tuple mit Bezirk und Gesamtzahl der Straftaten
    """
    # Definieren Sie die Jahre, die Sie analysieren möchten
    years = list(range(2014, 2024))  # 2014 bis 2023

    # Initialisieren Sie ein Dictionary zur Speicherung der Gesamtstraftaten pro Bezirk
    total_crimes = {}

    # Laden Sie die Excel-Datei
    try:
        xl = pd.ExcelFile(excel_file)
    except Exception as e:
        print(f"Fehler beim Laden der Excel-Datei: {e}")
        return

    # Iterieren Sie über alle Sheet-Namen
    for sheet in xl.sheet_names:
        # Prüfen Sie, ob der Sheet-Name dem Muster "PKS Jahr" entspricht
        match = re.search(r'PKS (\d{4})', sheet)
        if match:
            year = int(match.group(1))
            if year not in years:
                continue  # Überspringen Sie Jahre außerhalb des gewünschten Bereichs
            
            try:
                # Lesen Sie den relevanten Sheet, überspringen Sie die ersten 4 Zeilen, die Metadaten enthalten
                df = xl.parse(sheet, skiprows=4)
            except Exception as e:
                print(f"Fehler beim Lesen des Sheets {sheet}: {e}")
                continue

            # Bereinigen Sie die Spaltennamen
            df.columns = [col.strip().replace('\n', ' ') for col in df.columns]

            # Identifizieren Sie die relevanten Spalten
            bezirk_col = None
            crimes_col = None
            for col in df.columns:
                if 'Bezeichnung' in col:
                    bezirk_col = col
                elif 'Straftaten' in col and 'insgesamt' in col.lower():
                    crimes_col = col

            if not bezirk_col or not crimes_col:
                print(f"Relevante Spalten in Sheet {sheet} nicht gefunden.")
                continue

            # Extrahieren Sie die relevanten Daten
            df_relevant = df[[bezirk_col, crimes_col]].dropna()

            # Bereinigen Sie die Straftaten-Zahlen (Entfernen von Kommas und Umwandeln in Integer)
            df_relevant[crimes_col] = df_relevant[crimes_col].astype(str).str.replace('"', '').str.replace(',', '').astype(float).astype(int)

            # Summieren Sie die Straftaten pro Bezirk
            for _, row in df_relevant.iterrows():
                district = row[bezirk_col].strip()
                crimes = row[crimes_col]
                if district in total_crimes:
                    total_crimes[district] += crimes
                else:
                    total_crimes[district] = crimes

    # Ermitteln Sie den Bezirk mit den meisten Straftaten
    if total_crimes:
        max_district = max(total_crimes, key=total_crimes.get)
        max_crimes = total_crimes[max_district]
        return max_district, max_crimes
    else:
        print("Keine Daten gefunden.")
        return None, None

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_path = 'Fallzahlen&HZ2014-2023.xlsx'
    
    district, crimes = find_district_with_most_crimes(excel_path)
    
    if district and crimes:
        print(f"Der Bezirk mit den meisten Straftaten von allen Jahren kombiniert ist {district} mit {crimes} Straftaten.")
    else:
        print("Es konnte kein Bezirk mit den meisten Straftaten ermittelt werden.")