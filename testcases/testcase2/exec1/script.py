import pandas as pd

def find_district_with_most_crimes(file_path):
    """
    Liest die Kriminalitätsdaten aus der gegebenen Excel-Datei,
    führt die Daten über alle Jahre zusammen und gibt den Bezirk mit den meisten Straftaten zurück.
    
    :param file_path: Pfad zur Excel-Datei "Fallzahlen&HZ2014-2023.xlsx"
    :return: None (gibt das Ergebnis aus)
    """
    
    # Definiere die Jahre, die in den Sheets enthalten sind
    years = list(range(2014, 2024))  # 2014 bis 2023 inclusive
    sheet_names = [f'Fallzahlen_{year}' for year in years]
    
    # Initialisiere ein Dictionary, um die Gesamtzahlen pro Bezirk zu speichern
    total_crimes = {}
    
    for sheet in sheet_names:
        try:
            # Lese das aktuelle Sheet
            df = pd.read_excel(file_path, sheet_name=sheet)
            
            # Bereinige die Spaltennamen: Entferne Zeilenumbrüche und führende/trailende Leerzeichen
            df.columns = df.columns.str.replace('\n', ' ').str.strip()
            
            # Identifiziere die Spalte für 'Straftaten insgesamt'
            crimes_col = [col for col in df.columns if 'Straftaten' in col and 'insgesamt' in col.lower()]
            if not crimes_col:
                raise ValueError(f"Straftaten insgesamt Spalte nicht gefunden im Sheet: {sheet}")
            crimes_col = crimes_col[0]
            
            # Selektiere die relevanten Spalten
            relevant_df = df[['Bezeichnung (Bezirksregion)', crimes_col]]
            relevant_df = relevant_df.rename(columns={
                'Bezeichnung (Bezirksregion)': 'Bezirksregion',
                crimes_col: 'Straftaten_insgesamt'
            })
            
            # Bereinige die 'Straftaten_insgesamt' Zahlen: Entferne Kommas, Anführungszeichen und ersetze fehlende Werte
            relevant_df['Straftaten_insgesamt'] = relevant_df['Straftaten_insgesamt'].astype(str)\
                .str.replace('"', '')\
                .str.replace(',', '.')\
                .str.replace('–', '0')\
                .str.strip()
            
            # Konvertiere die Spalte in numerische Werte, setze Fehler auf NaN und fülle diese mit 0
            relevant_df['Straftaten_insgesamt'] = pd.to_numeric(relevant_df['Straftaten_insgesamt'], errors='coerce').fillna(0)
            
            # Gruppiere nach Bezirk und summiere die Straftaten
            grouped = relevant_df.groupby('Bezirksregion')['Straftaten_insgesamt'].sum()
            
            # Füge die Summen zum Gesamt-Dictionary hinzu
            for bezirk, sum_crimes in grouped.items():
                if bezirk in total_crimes:
                    total_crimes[bezirk] += sum_crimes
                else:
                    total_crimes[bezirk] = sum_crimes
        
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Sheets {sheet}: {e}")
    
    # Konvertiere das Dictionary zu einem DataFrame für einfachere Handhabung
    total_df = pd.DataFrame(list(total_crimes.items()), columns=['Bezirksregion', 'Total_Straftaten'])
    
    # Finde den Bezirk mit den meisten Straftaten
    max_row = total_df.loc[total_df['Total_Straftaten'].idxmax()]
    
    print(f"Bezirk mit den meisten Straftaten: {max_row['Bezirksregion']} mit {max_row['Total_Straftaten']:.0f} Straftaten.")

# Beispielaufruf
if __name__ == "__main__":
    # Ersetze den Pfad durch den tatsächlichen Pfad zu deiner Excel-Datei
    excel_file_path = 'Fallzahlen&HZ2014-2023.xlsx'
    find_district_with_most_crimes(excel_file_path)