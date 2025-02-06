import pandas as pd

def zusammenfuegen_und_sortieren(excel_datei):
    """
    Liest alle Sheets einer Excel-Datei, fügt sie zusammen,
    entfernt bestimmte LOR-Schlüssel, sortiert nach 'Straftaten_insgesamt'
    und gibt den resultierenden DataFrame zurück.
    
    Parameters:
    - excel_datei: str, Pfad zur Excel-Datei.
    
    Returns:
    - pd.DataFrame: Gefilterter und sortierter DataFrame.
    """
    
    # Laden Sie die Excel-Datei und holen Sie alle Sheet-Namen
    xls = pd.ExcelFile(excel_datei)
    sheet_namen = xls.sheet_names
    
    # Liste zur Speicherung der DataFrames aus jedem Sheet
    df_list = []
    
    # Durchlaufen Sie jede Sheet und lesen Sie die Daten
    for sheet in sheet_namen:
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        df_list.append(df)
        print(f"Gesheet '{sheet}' erfolgreich geladen.")
    
    # Verbinden Sie alle DataFrames zu einem einzigen DataFrame
    kombiniert_df = pd.concat(df_list, ignore_index=True)
    print("Alle Sheets wurden erfolgreich zusammengeführt.")
    
    # Entfernen Sie die Zeilen mit den LOR-Schlüsseln 999900 und 999999
    filtered_df = kombiniert_df[~kombiniert_df['LOR-Schlüssel'].isin([999900, 999999])]
    print("Unerwünschte LOR-Schlüssel wurden entfernt.")
    
    # Sortieren Sie den DataFrame nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    sorted_df = filtered_df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)
    print("DataFrame wurde nach 'Straftaten_insgesamt' sortiert.")
    
    return sorted_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_pfad = 'Fallzahlen.xlsx'
    
    # Rufen Sie die Funktion auf und speichern Sie das Ergebnis in 'final_df'
    final_df = zusammenfuegen_und_sortieren(excel_pfad)
    
    # Optional: Zeigen Sie die ersten paar Zeilen des finalen DataFrames an
    print(final_df.head())
    
    # Optional: Speichern Sie den finalen DataFrame als neue Excel-Datei
    # final_df.to_excel('Zusammengefuegte_Fallzahlen.xlsx', index=False)