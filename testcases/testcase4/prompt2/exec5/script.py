import pandas as pd
import re

def extract_year(sheet_name):
    """
    Extrahiert das Jahr aus dem Sheet-Namen.
    Erwartet Format: 'Fallzahlen_YYYY'
    """
    match = re.search(r'Fallzahlen_(\d{4})', sheet_name)
    if match:
        return int(match.group(1))
    else:
        return None

def get_straftaten_insgesamt(excel_file, sheet_name, target_district):
    """
    Liest ein Sheet und extrahiert den Wert von 'Straftaten_insgesamt' für den angegebenen Bezirk.
    """
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Annahme: Die Bezeichnung des Bezirks ist in der Spalte 'Bezirke'
    row = df[df['Bezirke'] == target_district]
    
    if not row.empty:
        return row.iloc[0]['Straftaten_insgesamt']
    else:
        print(f"Warnung: Bezirk '{target_district}' nicht in Sheet '{sheet_name}' gefunden.")
        return None

def main():
    excel_file = 'Fallzahlen.xlsx'
    target_district = 'Berlin (PKS gesamt)'
    
    # Lade alle Sheet-Namen
    xls = pd.ExcelFile(excel_file)
    sheet_names = xls.sheet_names
    
    # Filtere die relevanten Sheets und extrahiere die Jahre
    pattern = re.compile(r'^Fallzahlen_(\d{4})$')
    sheets_with_year = []
    for sheet in sheet_names:
        match = pattern.match(sheet)
        if match:
            year = int(match.group(1))
            sheets_with_year.append((year, sheet))
    
    if not sheets_with_year:
        print("Keine Sheets im erwarteten Format 'Fallzahlen_YYYY' gefunden.")
        return
    
    # Sortiere die Sheets nach Jahr
    sheets_with_year.sort(key=lambda x: x[0])
    
    # Extrahiere die 'Straftaten_insgesamt' Werte
    data = {}
    for year, sheet in sheets_with_year:
        value = get_straftaten_insgesamt(excel_file, sheet, target_district)
        if value is not None:
            data[year] = value
    
    # Erstelle ein DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Jahr', 'Straftaten_insgesamt'])
    df.sort_values('Jahr', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Berechne die prozentuale Veränderung zum Vorjahr
    df['Prozentuale_Veraenderung'] = df['Straftaten_insgesamt'].pct_change() * 100
    
    # Optional: Runde die Prozentwerte auf zwei Dezimalstellen
    df['Prozentuale_Veraenderung'] = df['Prozentuale_Veraenderung'].round(2)
    
    print(df)

if __name__ == "__main__":
    main()