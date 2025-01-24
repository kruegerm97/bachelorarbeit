import pandas as pd

def clean_number(x):
    """
    Entfernt Punkte und Kommata aus Zahlen und konvertiert sie in Integer.
    Beispiel: "83,611" -> 83611
    """
    if pd.isna(x):
        return 0
    return int(str(x).replace(',', '').replace('.', ''))

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'
    
    # Lesen der CSV-Datei
    # Annahme: Die ersten 4 Zeilen sind Meta-Informationen und werden übersprungen
    df = pd.read_csv(csv_file, 
                     skiprows=4, 
                     sep=',',
                     quotechar='"',
                     encoding='utf-8')
    
    # Umbenennen der Spalten, um Zeilenumbrüche zu entfernen und die Lesbarkeit zu verbessern
    df.columns = [
        'LOR_Schluessel', 'Bezeichnung_Bezirksregion', 'Straftaten_insgesamt', 'Raub',
        'Strassenraub_Handtaschenraub', 'Koerper_verletzungen_insgesamt', 
        'Gefaehrliche_schwere_Koerperverletzung', 'Freiheitsberaubung_Noetigung_Bedrohung_Nachstellung',
        'Diebstahl_insgesamt', 'Diebstahl_Kraftwagen', 'Diebstahl_Kfz', 'Fahrraddiebstahl',
        'Wohnraumeinbruch', 'Branddelikte_insgesamt', 'Brandstiftung', 
        'Sachbeschadigung_insgesamt', 'Sachbeschadigung_Graffiti', 'Rauschgiftdelikte', 'Kieztaten'
    ]
    
    # Entfernen von möglichen Leerzeichen in den Spaltennamen
    df.columns = df.columns.str.strip()
    
    # Konvertieren der relevanten Spalten von String zu Integer
    numeric_columns = [
        'Straftaten_insgesamt', 'Raub', 'Strassenraub_Handtaschenraub',
        'Koerper_verletzungen_insgesamt', 'Gefaehrliche_schwere_Koerperverletzung',
        'Freiheitsberaubung_Noetigung_Bedrohung_Nachstellung', 'Diebstahl_insgesamt',
        'Diebstahl_Kraftwagen', 'Diebstahl_Kfz', 'Fahrraddiebstahl',
        'Wohnraumeinbruch', 'Branddelikte_insgesamt', 'Brandstiftung',
        'Sachbeschadigung_insgesamt', 'Sachbeschadigung_Graffiti',
        'Rauschgiftdelikte', 'Kieztaten'
    ]

    for col in numeric_columns:
        df[col] = df[col].apply(clean_number)
    
    # Entfernen von aggregierten Zeilen, die nicht zugeordnet werden können
    df_filtered = df[~df['Bezeichnung_Bezirksregion'].str.contains('nicht zuzuordnen', case=False, na=False)]
    
    # Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    df_sorted = df_filtered.sort_values(by='Straftaten_insgesamt', ascending=False)
    
    # Zur besseren Lesbarkeit die Zahlen mit Tausenderpunkten formatieren
    df_sorted['Straftaten_insgesamt'] = df_sorted['Straftaten_insgesamt'].apply(lambda x: f"{x:,}".replace(',', '.'))
    
    # Ausgabe der sortierten Liste
    print("Bezirke sortiert nach der Gesamtzahl der Straftaten (2023):\n")
    print(df_sorted[['LOR_Schluessel', 'Bezeichnung_Bezirksregion', 'Straftaten_insgesamt']].to_string(index=False))

    # Optional: Speichern der sortierten Daten in eine neue CSV-Datei
    df_sorted.to_csv('FZ_2023_sortiert.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()