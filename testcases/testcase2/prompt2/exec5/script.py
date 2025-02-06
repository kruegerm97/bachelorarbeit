import pandas as pd

def process_fallzahlen_excel(file_path):
    """
    Liest die Excel-Datei 'Fallzahlen.xlsx', verarbeitet die Daten aus allen Sheets,
    entfernt bestimmte LOR-Schlüssel, fasst die Daten zusammen, sortiert sie nach
    'Straftaten_insgesamt' und gibt den finalen DataFrame zurück.
    
    :param file_path: Pfad zur Excel-Datei
    :return: Gefilterter und sortierter Pandas DataFrame
    """
    # Lese die Excel-Datei
    try:
        xls = pd.ExcelFile(file_path)
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

    # Liste zur Speicherung der einzelnen DataFrames
    df_list = []

    # Iteriere über alle Sheets
    for sheet_name in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Überprüfe, ob die notwendigen Spalten vorhanden sind
            required_columns = ['LOR-Schlüssel', 'Bezirke', 'Straftaten_insgesamt']
            if not all(col in df.columns for col in required_columns):
                print(f"Ein oder mehrere erforderliche Spalten fehlen im Sheet '{sheet_name}'.")
                continue

            # Entferne die Zeilen mit unerwünschten LOR-Schlüsseln
            df_filtered = df[~df['LOR-Schlüssel'].isin([999900, 999999])]

            # Wähle nur die benötigten Spalten
            df_selected = df_filtered[required_columns]

            # Füge eine neue Spalte für das Sheet hinzu (optional, falls benötigt)
            df_selected['Sheet'] = sheet_name

            # Füge den DataFrame der Liste hinzu
            df_list.append(df_selected)
        
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Sheets '{sheet_name}': {e}")
            continue

    if not df_list:
        print("Keine Daten zum Verarbeiten gefunden.")
        return None

    # Füge alle DataFrames zusammen
    combined_df = pd.concat(df_list, ignore_index=True)

    # Gruppiere nach 'LOR-Schlüssel' und 'Bezirke' und summiere 'Straftaten_insgesamt'
    grouped_df = combined_df.groupby(['LOR-Schlüssel', 'Bezirke'], as_index=False)['Straftaten_insgesamt'].sum()

    # Sortiere nach 'Straftaten_insgesamt' absteigend
    sorted_df = grouped_df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)

    return sorted_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file_path = 'Fallzahlen.xlsx'
    
    # Verarbeite die Excel-Datei und erhalte den finalen DataFrame
    final_df = process_fallzahlen_excel(excel_file_path)
    
    if final_df is not None:
        # Zeige die ersten paar Zeilen des finalen DataFrames an
        print(final_df)
        
        # Optional: Speichere den finalen DataFrame in einer neuen Excel- oder CSV-Datei
        # final_df.to_excel('Zusammengefasste_Fallzahlen.xlsx', index=False)
        # final_df.to_csv('Zusammengefasste_Fallzahlen.csv', index=False)