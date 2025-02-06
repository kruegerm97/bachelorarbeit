import pandas as pd

def extract_berlin_total(df):
    """
    Extrahiert die Gesamtzahl der Straftaten für Berlin aus dem DataFrame.

    Es wird entweder nach dem `LOR-Schlüssel` 999999 oder nach dem Bezirksnamen
    'Berlin (PKS gesamt)' gesucht.

    Args:
        df (pd.DataFrame): Der DataFrame des aktuellen Sheets.

    Returns:
        int oder float: Die Gesamtzahl der Straftaten in Berlin.
    """
    # Versuch 1: Nach LOR-Schlüssel 999999 filtern
    berlin_row = df[df['LOR-Schlüssel'] == 999999]
    
    if not berlin_row.empty:
        return berlin_row['Straftaten_insgesamt'].values[0]
    
    # Versuch 2: Nach Bezirksnamen 'Berlin (PKS gesamt)' filtern
    berlin_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if not berlin_row.empty:
        return berlin_row['Straftaten_insgesamt'].values[0]
    
    # Wenn nichts gefunden wurde, gebe NaN zurück
    return float('nan')

def main():
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    try:
        # Lade alle Sheets der Excel-Datei
        xls = pd.ExcelFile(excel_file)
    except FileNotFoundError:
        print(f"Die Datei {excel_file} wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Laden der Excel-Datei: {e}")
        return
    
    # Liste zur Speicherung der Daten
    data = []
    
    for sheet_name in xls.sheet_names:
        try:
            # Lese das aktuelle Sheet
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Extrahiere die Gesamtzahl der Straftaten für Berlin
            total_crimes = extract_berlin_total(df)
            
            # Versuche, das Jahr aus dem Sheet-Namen zu extrahieren
            try:
                year = int(sheet_name)
            except ValueError:
                # Wenn der Sheet-Name kein Jahr ist, überspringe dieses Sheet
                print(f"Sheet '{sheet_name}' entspricht nicht dem erwarteten Jahresformat und wird übersprungen.")
                continue
            
            # Füge die Daten zur Liste hinzu
            data.append({'Jahr': year, 'Straftaten_insgesamt': total_crimes})
        
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Sheets '{sheet_name}': {e}")
            continue
    
    # Erstelle einen DataFrame aus den gesammelten Daten
    df_totals = pd.DataFrame(data)
    
    if df_totals.empty:
        print("Keine gültigen Daten gefunden.")
        return
    
    # Sortiere den DataFrame nach Jahr
    df_totals.sort_values('Jahr', inplace=True)
    
    # Setze das Jahr als Index
    df_totals.set_index('Jahr', inplace=True)
    
    # Berechne die prozentuale Veränderung zum Vorjahr
    df_totals['Prozentuale_Veraenderung'] = df_totals['Straftaten_insgesamt'].pct_change() * 100
    
    # Optional: Runde die Prozentwerte auf zwei Dezimalstellen
    df_totals['Prozentuale_Veraenderung'] = df_totals['Prozentuale_Veraenderung'].round(2)
    
    # Anzeige des resultierenden DataFrames
    print(df_totals)
    
    # Optional: Speichere das Ergebnis in eine neue Excel-Datei
    output_file = 'Straftaten_Zeitreihe.xlsx'
    try:
        df_totals.to_excel(output_file)
        print(f"Das Ergebnis wurde erfolgreich in '{output_file}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Ergebnisdatei: {e}")

if __name__ == "__main__":
    main()