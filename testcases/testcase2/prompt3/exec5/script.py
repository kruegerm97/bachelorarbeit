import pandas as pd

def process_fallzahlen_excel(file_path='Fallzahlen.xlsx'):
    """
    Liest die Excel-Datei ein, verbindet die Sheets, sortiert das Ergebnis nach
    'Straftaten_insgesamt' und platziert die nicht zuordenbaren Einträge am Ende.
    
    Parameters:
    - file_path: Pfad zur Excel-Datei (Standard: 'Fallzahlen.xlsx')
    
    Returns:
    - final_df: Sortiertes Pandas DataFrame
    """
    # Schritt 1: Alle Sheets der Excel-Datei einlesen
    try:
        excel_sheets = pd.read_excel(file_path, sheet_name=None)
    except FileNotFoundError:
        print(f"Datei '{file_path}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Einlesen der Datei: {e}")
        return
    
    # Liste zur Speicherung der DataFrames
    df_list = []
    
    for sheet_name, df in excel_sheets.items():
        # Sicherstellen, dass 'LOR-Schlüssel' und 'Bezirke' als Schlüssel vorhanden sind
        if 'LOR-Schlüssel' not in df.columns or 'Bezirke' not in df.columns:
            print(f"Sheet '{sheet_name}' enthält nicht die notwendigen Spalten.")
            continue
        df_list.append(df)
    
    if not df_list:
        print("Keine gültigen Sheets gefunden.")
        return
    
    # Schritt 2: DataFrames zusammenführen (joinen) auf 'LOR-Schlüssel' und 'Bezirke'
    merged_df = df_list[0]
    for df in df_list[1:]:
        merged_df = pd.merge(merged_df, df, on=['LOR-Schlüssel', 'Bezirke'], how='outer', suffixes=('', '_dup'))
        
        # Entfernen von doppelten Spalten, falls vorhanden
        dup_columns = [col for col in merged_df.columns if col.endswith('_dup')]
        if dup_columns:
            merged_df.drop(columns=dup_columns, inplace=True)
    
    # Schritt 3: Sortieren nach 'Straftaten_insgesamt', wobei 999900 und 999999 am Ende stehen
    # Zuerst sicherstellen, dass 'Straftaten_insgesamt' numerisch ist
    merged_df['Straftaten_insgesamt'] = pd.to_numeric(merged_df['Straftaten_insgesamt'], errors='coerce')
    
    # Trennen der DataFrames
    districts_df = merged_df[~merged_df['LOR-Schlüssel'].isin([999900, 999999])]
    non_districts_df = merged_df[merged_df['LOR-Schlüssel'].isin([999900, 999999])]
    
    # Sortieren der Bezirke
    sorted_districts_df = districts_df.sort_values(by='Straftaten_insgesamt', ascending=False)
    
    # Kombinieren der sortierten Bezirke mit den nicht zuordenbaren Einträgen
    final_df = pd.concat([sorted_districts_df, non_districts_df], ignore_index=True)
    
    return final_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Verarbeitung der Excel-Datei
    sorted_df = process_fallzahlen_excel(excel_file)
    
    if sorted_df is not None:
        # Ausgabe des sortierten DataFrames
        print(sorted_df)
        
        # Optional: Speichern des Ergebnisses in einer neuen Excel-Datei
        # sorted_df.to_excel('Sorted_Fallzahlen.xlsx', index=False)