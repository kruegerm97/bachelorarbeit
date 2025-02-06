import pandas as pd

def main():
    # 1. Excel-Datei einlesen und alle Sheets als DataFrames speichern
    excel_datei = 'Fallzahlen.xlsx'
    sheets_dict = pd.read_excel(excel_datei, sheet_name=None)
    
    # 2. DataFrames der einzelnen Sheets zusammenführen (joinen)
    # Alle DataFrames vertikal concatenieren
    concatenated_df = pd.concat(sheets_dict.values(), ignore_index=True)
    
    # Gruppieren nach 'LOR-Schlüssel' und 'Bezirke' und die numerischen Spalten akkumulieren
    gruppiert_df = concatenated_df.groupby(['LOR-Schlüssel', 'Bezirke'], as_index=False).sum()
    
    # 3. DataFrame sortieren nach 'Straftaten_insgesamt', dabei LOR-Schlüssel 999900 und 999999 am Ende lassen
    # Definieren der auszuschließenden LOR-Schlüssel
    ausschluss_keys = [999900, 999999]
    
    # DataFrame ohne die auszuschließenden LOR-Schlüssel
    zu_sortieren_df = gruppiert_df[~gruppiert_df['LOR-Schlüssel'].isin(ausschluss_keys)]
    
    # DataFrame mit den auszuschließenden LOR-Schlüsseln
    ausgeschlossen_df = gruppiert_df[gruppiert_df['LOR-Schlüssel'].isin(ausschluss_keys)]
    
    # Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    sortiert_df = zu_sortieren_df.sort_values(by='Straftaten_insgesamt', ascending=False)
    
    # Ausschließenere Zeilen am Ende des sortierten DataFrames anhängen
    final_df = pd.concat([sortiert_df, ausgeschlossen_df], ignore_index=True)
    
    # 4. Sortiertes DataFrame zurückgeben (hier wird es angezeigt)
    print(final_df)

if __name__ == '__main__':
    main()