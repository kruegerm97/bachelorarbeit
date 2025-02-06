import pandas as pd

def main():
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'

    # Lade alle Sheet-Namen aus der Excel-Datei
    xls = pd.ExcelFile(excel_file)
    sheet_names = xls.sheet_names

    # Dictionary zum Speichern der DataFrames
    dataframes = {}
    
    # Dictionary zum Speichern der 'Straftaten_insgesamt' Werte
    strafaten_dict = {}

    for sheet in sheet_names:
        # Lese jedes Sheet in einen DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet)
        dataframes[sheet] = df

        # Extrahiere das Jahr aus dem Sheet-Namen (angenommen, Format 'Fallzahlen_YYYY')
        try:
            year = int(sheet.split('_')[-1])
        except ValueError:
            print(f"Sheet-Name {sheet} entspricht nicht dem erwarteten Format 'Fallzahlen_YYYY'.")
            continue

        # Finde die Zeile für 'Berlin (PKS gesamt)'
        berlin_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

        if not berlin_row.empty:
            # Extrahiere den Wert von 'Straftaten_insgesamt'
            strafaten_value = berlin_row['Straftaten_insgesamt'].values[0]
            strafaten_dict[year] = strafaten_value
        else:
            print(f"'Berlin (PKS gesamt)' nicht im Sheet {sheet} gefunden.")
            strafaten_dict[year] = None

    # Erstelle einen DataFrame aus den gesammelten Daten
    strafaten_df = pd.DataFrame(list(strafaten_dict.items()), columns=['Jahr', 'Straftaten_insgesamt'])
    strafaten_df.sort_values('Jahr', inplace=True)
    strafaten_df.reset_index(drop=True, inplace=True)

    # Berechne die prozentuale Veränderung zum Vorjahr
    strafaten_df['Prozentuale_Veraenderung'] = strafaten_df['Straftaten_insgesamt'].pct_change() * 100

    # Optional: Runde die Veränderung auf 2 Dezimalstellen
    strafaten_df['Prozentuale_Veraenderung'] = strafaten_df['Prozentuale_Veraenderung'].round(2)

    # Anzeige der Ergebnisse
    print(strafaten_df)

    # Optional: Speichern der Ergebnisse in eine neue Excel-Datei
    output_file = 'Straftaten_Veraenderung.xlsx'
    strafaten_df.to_excel(output_file, index=False)
    print(f"Ergebnisse wurden in '{output_file}' gespeichert.")

if __name__ == "__main__":
    main()