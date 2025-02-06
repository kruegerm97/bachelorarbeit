import pandas as pd

def lese_und_sortiere_fallzahlen(excel_datei):
    """
    Liest alle Sheets aus der angegebenen Excel-Datei, kombiniert die Daten,
    sortiert sie nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    und gibt den sortierten DataFrame zurück.
    
    :param excel_datei: Pfad zur Excel-Datei (z.B. 'Fallzahlen.xlsx')
    :return: Sortierter Pandas DataFrame
    """
    try:
        # Alle Sheets der Excel-Datei lesen. sheet_name=None liest alle Sheets als Dict.
        alle_sheets = pd.read_excel(excel_datei, sheet_name=None)
        
        # Liste zur Speicherung aller DataFrames
        dataframe_liste = []
        
        # Durch alle Sheets iterieren und die DataFrames zur Liste hinzufügen
        for sheet_name, df in alle_sheets.items():
            # Optional: Hinzufügen einer Spalte mit dem Sheet-Namen, falls nötig
            # df['Sheet_Name'] = sheet_name
            dataframe_liste.append(df)
        
        # Alle DataFrames zu einem einzigen DataFrame kombinieren
        kombiniertes_df = pd.concat(dataframe_liste, ignore_index=True)
        
        # Prüfen, ob die Spalte 'Straftaten_insgesamt' existiert
        if 'Straftaten_insgesamt' not in kombiniertes_df.columns:
            raise ValueError("Die Spalte 'Straftaten_insgesamt' wurde in den Daten nicht gefunden.")
        
        # Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
        sortiertes_df = kombiniertes_df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)
        
        return sortiertes_df
    
    except FileNotFoundError:
        print(f"Die Datei {excel_datei} wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    dateipfad = 'Fallzahlen.xlsx'
    
    # Funktion aufrufen und sortierten DataFrame erhalten
    df_sortiert = lese_und_sortiere_fallzahlen(dateipfad)
    
    if df_sortiert is not None:
        # Sortierten DataFrame anzeigen
        print(df_sortiert)
        
        # Optional: Sortierten DataFrame in eine neue Excel-Datei speichern
        df_sortiert.to_excel('Fallzahlen_sortiert.xlsx', index=False)