import pandas as pd

def load_and_process_excel(file_path):
    """
    Lädt alle Sheets aus der angegebenen Excel-Datei, fügt sie zusammen,
    filtert unerwünschte Zeilen, sortiert die Daten und gibt einen DataFrame zurück.
    
    Parameters:
        file_path (str): Der Pfad zur Excel-Datei.
    
    Returns:
        pd.DataFrame: Der verarbeitete DataFrame.
    """
    try:
        # Lade alle Sheets in ein Dictionary von DataFrames
        all_sheets = pd.read_excel(file_path, sheet_name=None, dtype={'LOR-Schlüssel': str})
        
        # Liste zum Speichern der DataFrames
        df_list = []
        
        for sheet_name, df in all_sheets.items():
            print(f"Lade Sheet: {sheet_name} mit {len(df)} Zeilen.")
            df_list.append(df)
        
        # Kombiniere alle DataFrames in einen einzigen DataFrame
        combined_df = pd.concat(df_list, ignore_index=True)
        print(f"Gesamtanzahl der Zeilen nach dem Zusammenführen: {len(combined_df)}")
        
        # Entferne Zeilen mit LOR-Schlüssel 999900 und 999999
        filtered_df = combined_df[~combined_df['LOR-Schlüssel'].isin([999900, 999999])]
        print(f"Anzahl der Zeilen nach dem Filtern: {len(filtered_df)}")
        
        # Sortiere nach 'Straftaten_insgesamt' absteigend
        sorted_df = filtered_df.sort_values(by='Straftaten_insgesamt', ascending=False)
        print("Daten wurden nach 'Straftaten_insgesamt' sortiert.")
        
        # Optional: Setze den Index zurück
        sorted_df.reset_index(drop=True, inplace=True)
        
        return sorted_df
    
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Verarbeite die Excel-Datei
    final_df = load_and_process_excel(excel_file)
    
    if final_df is not None:
        # Zeige die ersten paar Zeilen des finalen DataFrames
        print("\nErgebnis:")
        print(final_df.head())
        
        # Optional: Speichere den DataFrame in eine neue Excel- oder CSV-Datei
        # final_df.to_excel('Zusammengefuegte_Fallzahlen.xlsx', index=False)
        # final_df.to_csv('Zusammengefuegte_Fallzahlen.csv', index=False)