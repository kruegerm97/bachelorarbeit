import pandas as pd

def extract_year(sheet_name):
    """
    Extrahiert das Jahr aus dem Sheetnamen.
    Annahme: Der Sheetname enthält das Jahr als vierstellige Zahl, z.B. "2020", "2021".
    """
    import re
    match = re.search(r'(\d{4})', sheet_name)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Kein Jahr im Sheetnamen '{sheet_name}' gefunden.")

def get_total_crimes(df):
    """
    Extrahiert die Gesamtzahl der Straftaten für Berlin aus dem DataFrame.
    Annahme: Die Zeile mit 'Bezirke' == 'Berlin (PKS gesamt)' enthält die Gesamtzahl.
    """
    total_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if total_row.empty:
        raise ValueError("Keine Zeile mit 'Berlin (PKS gesamt)' gefunden.")
    return total_row['Straftaten_insgesamt'].values[0]

def main():
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Lade die Excel-Datei
    try:
        xls = pd.ExcelFile(excel_file)
    except FileNotFoundError:
        print(f"Datei '{excel_file}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        return
    
    # Liste der Sheets
    sheet_names = xls.sheet_names
    
    # Liste zur Speicherung der Ergebnisse
    data = []
    
    for sheet in sheet_names:
        try:
            # Lade das Sheet als DataFrame
            df = pd.read_excel(xls, sheet_name=sheet)
            
            # Extrahiere das Jahr
            year = extract_year(sheet)
            
            # Extrahiere die Gesamtzahl der Straftaten
            total_crimes = get_total_crimes(df)
            
            # Speichere das Ergebnis
            data.append({'Jahr': year, 'Straftaten_insgesamt': total_crimes})
        
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Sheets '{sheet}': {e}")
            continue
    
    # Erstelle einen DataFrame aus den gesammelten Daten
    crimes_df = pd.DataFrame(data)
    
    # Sortiere den DataFrame nach Jahr
    crimes_df.sort_values('Jahr', inplace=True)
    crimes_df.reset_index(drop=True, inplace=True)
    
    # Berechne die prozentuale Veränderung zum Vorjahr
    crimes_df['Prozentuale_Veraenderung'] = crimes_df['Straftaten_insgesamt'].pct_change() * 100
    
    # Optional: Runde die Prozentwerte auf zwei Dezimalstellen
    crimes_df['Prozentuale_Veraenderung'] = crimes_df['Prozentuale_Veraenderung'].round(2)
    
    # Setze das Jahr als Index (optional)
    crimes_df.set_index('Jahr', inplace=True)
    
    # Anzeige des resultierenden DataFrames
    print(crimes_df)
    
    # Optional: Speichern des DataFrames als CSV
    # crimes_df.to_csv('Prozentuale_Veraenderung_Straftaten_Berlin.csv')

if __name__ == "__main__":
    main()