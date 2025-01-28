import pandas as pd

def find_top_crime_district(excel_file):
    # Liste der Jahre von 2014 bis 2023
    years = list(range(2014, 2024))
    
    # Generiere die erwarteten Sheet-Namen nach dem Muster 'Fallzahlen_YYYY'
    expected_sheets = [f'Fallzahlen_{year}' for year in years]
    
    # Lese alle Sheet-Namen aus der Excel-Datei
    all_sheets = pd.ExcelFile(excel_file).sheet_names
    
    # Filter nur die relevanten Sheets basierend auf der Namenskonvention
    relevant_sheets = [sheet for sheet in all_sheets if sheet in expected_sheets]
    
    if not relevant_sheets:
        print("Keine relevanten Sheets gefunden. Überprüfe die Sheet-Namen.")
        return
    
    # Liste zur Speicherung der DataFrames pro Jahr
    data_frames = []
    
    for sheet in relevant_sheets:
        try:
            # Lese das Sheet und überspringe die ersten 5 Zeilen, falls die Struktur konstant ist
            df = pd.read_excel(excel_file, sheet_name=sheet, skiprows=5)
            
            # Überprüfe, ob die benötigten Spalten vorhanden sind
            if 'Bezeichnung (Bezirksregion)' not in df.columns or 'Straftaten -insgesamt-' not in df.columns:
                print(f"Sheet {sheet} hat nicht die erwarteten Spalten. Wird übersprungen.")
                continue
            
            # Wähle nur die relevanten Spalten
            df = df[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']]
            
            # Bereinige die Zahlen: entferne Kommas und wandle in Integer um
            df['Straftaten -insgesamt-'] = df['Straftaten -insgesamt-'].astype(str).str.replace(',', '').astype(int)
            
            # Füge eine Spalte für das Jahr hinzu
            year = sheet.split('_')[-1]
            df['Jahr'] = int(year)
            
            data_frames.append(df)
        
        except Exception as e:
            print(f"Fehler beim Lesen von Sheet {sheet}: {e}")
    
    if not data_frames:
        print("Keine Daten zum Verarbeiten gefunden.")
        return
    
    # Kombiniere alle DataFrames in einen einzigen
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    # Aggregiere die Straftaten pro Bezirk über alle Jahre
    aggregated_df = combined_df.groupby('Bezeichnung (Bezirksregion)').agg({'Straftaten -insgesamt-': 'sum'}).reset_index()
    
    # Finde den Bezirk mit den meisten Straftaten
    top_district = aggregated_df.loc[aggregated_df['Straftaten -insgesamt-'].idxmax()]
    
    print(f"Der Bezirk mit den meisten Straftaten über alle Jahre hinweg ist:\n"
          f"Bezirk: {top_district['Bezeichnung (Bezirksregion)']}\n"
          f"Gesamtstraftaten: {top_district['Straftaten -insgesamt-']}")
    
    return top_district

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen&HZ2014-2023.xlsx'
    
    # Finde und gib den Bezirk mit den meisten Straftaten aus
    find_top_crime_district(excel_file)