import pandas as pd

def get_top_10_unterbezirke(excel_file):
    # Liste der Jahre von 2014 bis 2023
    jahre = list(range(2014, 2024))
    
    # Initialisiere ein leeres DataFrame für die aggregierten Daten
    aggregierte_daten = pd.DataFrame()
    
    # Iteriere über jede Jahres-Sheet
    for jahr in jahre:
        sheet_name = f'Fallzahlen_{jahr}'
        try:
            # Lese das aktuelle Sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Überprüfe, ob die notwendigen Spalten vorhanden sind
            if 'Bezeichnung (Bezirksregion)' not in df.columns or 'Straftaten insgesamt' not in df.columns:
                print(f"Wichtige Spalten fehlen im Sheet {sheet_name}. Überspringe dieses Sheet.")
                continue
            
            # Auswahl der relevanten Spalten
            # Annahme: 'Straftaten insgesamt' ist die Spalte mit den gesamten Straftaten
            # Passen Sie die Spaltennamen an, falls sie sich unterscheiden
            df_relevant = df[['Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']]
            
            # Gruppiere nach Unterbezirk und summiere die Straftaten
            df_grouped = df_relevant.groupby('Bezeichnung (Bezirksregion)', as_index=False).sum()
            
            # Füge die Daten dem aggregierten DataFrame hinzu
            if aggregierte_daten.empty:
                aggregierte_daten = df_grouped
            else:
                aggregierte_daten = aggregierte_daten.merge(df_grouped, on='Bezeichnung (Bezirksregion)', how='outer')
                aggregierte_daten['Straftaten insgesamt'] = aggregierte_daten['Straftaten insgesamt_x'].fillna(0) + aggregierte_daten['Straftaten insgesamt_y'].fillna(0)
                aggregierte_daten.drop(['Straftaten insgesamt_x', 'Straftaten insgesamt_y'], axis=1, inplace=True)
        
        except ValueError:
            print(f"Sheet {sheet_name} nicht gefunden in der Datei. Überspringe dieses Sheet.")
            continue
    
    # Nach allen Sheets aggregiert, sortiere die Unterbezirke nach Straftaten insgesamt
    aggregierte_daten_sorted = aggregierte_daten.sort_values(by='Straftaten insgesamt', ascending=False)
    
    # Wähle die Top 10 Unterbezirke aus
    top_10 = aggregierte_daten_sorted.head(10)
    
    return top_10

if __name__ == "__main__":
    excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'
    top_10_unterbezirke = get_top_10_unterbezirke(excel_datei)
    print("Die Top 10 Unterbezirke mit den meisten Straftaten insgesamt (2014-2023):\n")
    print(top_10_unterbezirke.to_string(index=False))