import pandas as pd

def get_top_unterbezirke(excel_file, sheets_prefix='Fallzahlen_', start_year=2014, end_year=2023, top_n=10):
    # Liste zur Speicherung der DataFrames aus allen Jahren
    df_list = []
    
    for year in range(start_year, end_year + 1):
        sheet_name = f"{sheets_prefix}{year}"
        try:
            # Lade das jeweilige Sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Überprüfe, ob die notwendigen Spalten vorhanden sind
            if 'LOR-Schlüssel (Bezirksregion)' in df.columns and 'Straftaten insgesamt' in df.columns:
                # Wähle relevante Spalten
                df_subset = df[['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']].copy()
                
                # Falls es weitere Bereinigungen benötigt, kann dies hier eingefügt werden
                
                df_list.append(df_subset)
            else:
                print(f"Wichtige Spalten fehlen im Sheet {sheet_name}.")
        except Exception as e:
            print(f"Fehler beim Laden des Sheets {sheet_name}: {e}")
    
    if not df_list:
        print("Keine Daten zum Verarbeiten gefunden.")
        return
    
    # Kombiniere alle DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Gruppiere nach Unterbezirk und summiere die Straftaten insgesamt
    aggregated_df = combined_df.groupby(['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)'])['Straftaten insgesamt'].sum().reset_index()
    
    # Sortiere nach den meisten Straftaten und wähle die Top N
    top_unterbezirke = aggregated_df.sort_values(by='Straftaten insgesamt', ascending=False).head(top_n)
    
    return top_unterbezirke

if __name__ == "__main__":
    excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'  # Pfad zu deiner Excel-Datei
    top_n = 10  # Anzahl der Top-Unterbezirke
    
    top_unterbezirke = get_top_unterbezirke(excel_file, top_n=top_n)
    
    if top_unterbezirke is not None:
        print(f"Top {top_n} Unterbezirke mit den meisten Straftaten insgesamt (2014-2023):")
        print(top_unterbezirke.to_string(index=False))