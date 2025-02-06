import pandas as pd

def analyze_fallzahlen(file_path, target_district="Berlin (PKS gesamt)", 
                       column_name="Straftaten_insgesamt"):
    """
    Analysiert die Excel-Datei 'Fallzahlen.xlsx' und erstellt eine Zeitreihe mit 
    der prozentualen Veränderung der Straftaten zum jeweiligen Vorjahr.
    
    Parameters:
    - file_path: Pfad zur Excel-Datei
    - target_district: Name des Bezirks, der analysiert werden soll
    - column_name: Name der Spalte, deren Veränderung berechnet werden soll
    
    Returns:
    - pandas DataFrame mit den Jahreszahlen und der prozentualen Veränderung
    """
    
    # Lade die Excel-Datei
    try:
        xls = pd.ExcelFile(file_path)
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten beim Laden der Datei: {e}")
        return
    
    # Initialisiere ein Dictionary zur Speicherung der Ergebnisse
    data = {}
    
    # Iteriere über alle Sheets in der Excel-Datei
    for sheet in xls.sheet_names:
        # Extrahiere das Jahr aus dem Sheet-Namen
        try:
            year = int(sheet.split('_')[-1])
        except ValueError:
            print(f"Das Sheet '{sheet}' folgt nicht dem erwarteten Namensformat. Überspringe dieses Sheet.")
            continue
        
        # Lese das aktuelle Sheet in einen DataFrame
        try:
            df = pd.read_excel(xls, sheet_name=sheet)
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten beim Lesen des Sheets '{sheet}': {e}")
            continue
        
        # Finde die Zeile für den Zielbezirk
        row = df[df['Bezirke'] == target_district]
        
        if row.empty:
            print(f"Der Bezirk '{target_district}' wurde im Sheet '{sheet}' nicht gefunden. Überspringe dieses Sheet.")
            continue
        
        # Extrahiere den Wert der gewünschten Spalte
        try:
            value = row[column_name].values[0]
            # Stelle sicher, dass der Wert numerisch ist
            value = float(value)
        except (IndexError, ValueError) as e:
            print(f"Fehler beim Extrahieren des Wertes in Sheet '{sheet}': {e}")
            continue
        
        # Speichere das Jahr und den Wert im Dictionary
        data[year] = value
    
    # Erstelle einen DataFrame aus dem Dictionary
    df_data = pd.DataFrame(list(data.items()), columns=['Year', column_name])
    
    # Sortiere den DataFrame nach dem Jahr aufsteigend
    df_data.sort_values('Year', inplace=True)
    df_data.reset_index(drop=True, inplace=True)
    
    # Berechne die prozentuale Veränderung zum Vorjahr
    df_data['Percent Change'] = df_data[column_name].pct_change() * 100
    
    # Optional: Runde die Prozentänderungen auf zwei Dezimalstellen
    df_data['Percent Change'] = df_data['Percent Change'].round(2)
    
    # Setze das Jahr als Index (optional)
    # df_data.set_index('Year', inplace=True)
    
    return df_data

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Führe die Analyse durch
    result_df = analyze_fallzahlen(excel_file)
    
    if result_df is not None:
        # Zeige das Ergebnis an
        print(result_df)
        
        # Optional: Speichere das Ergebnis in einer neuen Excel- oder CSV-Datei
        # result_df.to_excel('Straftaten_Prozentuale_Veraenderung.xlsx', index=False)
        # oder
        # result_df.to_csv('Straftaten_Prozentuale_Veraenderung.csv', index=False)