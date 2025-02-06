import pandas as pd

def merge_and_sort_fallzahlen(excel_file):
    """
    Liest alle Sheets der angegebenen Excel-Datei, filtert unerwünschte LOR-Schlüssel,
    fasst die Daten der Bezirke zusammen, sortiert sie nach Straftaten_insgesamt
    und gibt das resultierende DataFrame zurück.
    
    Parameters:
    - excel_file (str): Pfad zur Excel-Datei (z.B. 'Fallzahlen.xlsx')
    
    Returns:
    - pd.DataFrame: Gefiltertes und sortiertes DataFrame
    """
    
    # Definiere die unerwünschten LOR-Schlüssel
    exclude_lor_keys = [999900, 999999]
    
    try:
        # Lade alle Sheets in ein Dictionary von DataFrames
        sheets_dict = pd.read_excel(excel_file, sheet_name=None)
        print(f"Es wurden {len(sheets_dict)} Sheets gefunden und geladen.")
    except FileNotFoundError:
        print(f"Die Datei '{excel_file}' wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist beim Lesen der Excel-Datei aufgetreten: {e}")
        return None
    
    # Liste zur Speicherung gefilterter DataFrames
    filtered_dfs = []
    
    # Iteriere über jedes Sheet und filtere die unerwünschten Zeilen
    for sheet_name, df in sheets_dict.items():
        print(f"Verarbeite Sheet: {sheet_name}")
        
        # Überprüfe, ob die erforderlichen Spalten vorhanden sind
        required_columns = ['LOR-Schlüssel', 'Bezirke', 'Straftaten_insgesamt']
        if not all(col in df.columns for col in required_columns):
            print(f"Sheet '{sheet_name}' fehlt eine oder mehrere erforderliche Spalten. Überspringe dieses Sheet.")
            continue
        
        # Filtere die unerwünschten LOR-Schlüssel
        df_filtered = df[~df['LOR-Schlüssel'].isin(exclude_lor_keys)].copy()
        print(f"Anzahl der Bezirke nach Filtern in Sheet '{sheet_name}': {len(df_filtered)}")
        
        # Optional: Falls du weitere Daten aggregieren möchtest, kannst du hier weitere Schritte hinzufügen
        
        filtered_dfs.append(df_filtered)
    
    if not filtered_dfs:
        print("Keine gültigen Daten zum Zusammenfügen gefunden.")
        return None
    
    # Füge alle gefilterten DataFrames zusammen
    combined_df = pd.concat(filtered_dfs, ignore_index=True)
    print(f"Gesamtanzahl der Zeilen nach dem Zusammenfügen: {len(combined_df)}")
    
    # Gruppiere die Daten nach 'LOR-Schlüssel' und 'Bezirke' und summiere 'Straftaten_insgesamt'
    aggregated_df = combined_df.groupby(['LOR-Schlüssel', 'Bezirke'], as_index=False)['Straftaten_insgesamt'].sum()
    print("Daten wurden nach 'LOR-Schlüssel' und 'Bezirke' aggregiert.")
    
    # Sortiere das DataFrame nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    sorted_df = aggregated_df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)
    print("Daten wurden nach 'Straftaten_insgesamt' sortiert.")
    
    return sorted_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Rufe die Funktion auf und erhalte das sortierte DataFrame
    result_df = merge_and_sort_fallzahlen(excel_file)
    
    if result_df is not None:
        # Zeige die ersten paar Zeilen des Ergebnisses an
        print("\nSortiertes Ergebnis:")
        print(result_df.head())
        
        # Optional: Speichere das Ergebnis in einer neuen Excel-Datei oder CSV
        # result_df.to_excel('Aggregierte_Fallzahlen.xlsx', index=False)
        # result_df.to_csv('Aggregierte_Fallzahlen.csv', index=False)