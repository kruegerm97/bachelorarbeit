import pandas as pd

def berechne_straftaten_anteil(excel_datei, sheet_name, ausgabe_datei):
    # Excel-Datei einlesen
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)
    
    # Anzeigen der Daten zur Überprüfung (optional)
    # print(df.head())

    # Identifizieren der Gesamtzeile für Berlin
    # Annahme: Die Gesamtzeile hat 'Bezirke' als "Berlin (PKS gesamt)"
    gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if gesamt_row.empty:
        # Falls keine explizite Gesamtzeile vorhanden ist, summiere alle relevanten Bezirke
        # Annahme: Die Gesamtzeile hat einen LOR-Schlüssel von 999999
        gesamt_row = df[df['LOR-Schlüssel'] == 999999]
    
    if gesamt_row.empty:
        raise ValueError("Gesamtdaten für Berlin nicht gefunden.")
    
    # Gesamtzahl der Straftaten in Berlin
    gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].values[0]
    
    # Filtere nur die Bezirke, die zu Berlin gehören und nicht die Gesamtzeile oder nicht zuzuordnend
    # Annahme: 'Stadtgebiet Berlin, nicht zuzuordnen' und 'Berlin (PKS gesamt)' sollen ausgeschlossen werden
    relevante_bezirke = df[~df['Bezirke'].isin(['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen'])]
    
    # Berechne den prozentualen Anteil
    relevante_bezirke = relevante_bezirke.copy()  # Um eine Kopie zu erstellen
    relevante_bezirke['Prozentualer Anteil (%)'] = (relevante_bezirke['Straftaten_insgesamt'] / gesamt_straftaten) * 100
    
    # Optional: Runden auf zwei Dezimalstellen
    relevante_bezirke['Prozentualer Anteil (%)'] = relevante_bezirke['Prozentualer Anteil (%)'].round(2)
    
    # Sortiere die Bezirke nach dem prozentualen Anteil absteigend
    relevante_bezirke = relevante_bezirke.sort_values(by='Prozentualer Anteil (%)', ascending=False)
    
    # Auswahl der relevanten Spalten für die Ausgabe
    ausgabe_df = relevante_bezirke[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer Anteil (%)']]
    
    # Ausgabe in eine neue Excel-Datei
    ausgabe_df.to_excel(ausgabe_datei, index=False)
    
    print(f"Die prozentualen Anteile wurden erfolgreich berechnet und in '{ausgabe_datei}' gespeichert.")

if __name__ == "__main__":
    # Pfad zur Eingabe-Excel-Datei
    input_excel = 'Fallzahlen.xlsx'
    
    # Name des Sheets
    sheet = 'Fallzahlen_2023'
    
    # Name der Ausgabedatei
    output_excel = 'Straftaten_Anteil_Bezirke.xlsx'
    
    # Funktion aufrufen
    berechne_straftaten_anteil(input_excel, sheet, output_excel)