import pandas as pd

def load_and_process_data(csv_file):
    """
    Lädt die CSV-Datei, bereinigt die Daten und sortiert die Bezirke nach
    der Gesamtzahl der Straftaten im Jahr 2023.
    
    :param csv_file: Pfad zur CSV-Datei
    :return: Ein DataFrame mit sortierten Bezirken
    """
    # Zuerst die Datei einlesen. Da die ersten paar Zeilen keine Daten enthalten,
    # verwenden wir den Parameter 'skiprows', um diese zu überspringen.
    # Basierend auf den bereitgestellten Daten scheint die tatsächliche Kopfzeile
    # bei der Zeile mit 'LOR-Schlüssel (Bezirksregion)' zu beginnen.
    
    # Finden der Zeile, die als Kopfzeile dient
    with open(csv_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if line.startswith('LOR-Schlüssel'):
                header_line = i
                break
    
    # Daten in pandas DataFrame laden, Kopfzeile definieren
    df = pd.read_csv(
        csv_file,
        sep=",",
        skiprows=header_line,
        encoding='utf-8',
        dtype=str
    )
    
    # Benennen der Spalten zur besseren Handhabung (falls notwendig)
    df.columns = [
        'LOR-Schlüssel',
        'Bezeichnung',
        'Straftaten insgesamt',
        'Raub',
        'Strassenraub_Handtaschen_raub',
        'Koerper_verletzungen_insgesamt',
        'Gefaehrl_schwere_Koerper_verletzung',
        'Freiheitsberaubung_noetigung_bedrohung_nachstellung',
        'Diebstahl_insgesamt',
        'Diebstahl_Kraftwagen',
        'Diebstahl_an_aus_Kfz',
        'Fahrraddiebstahl',
        'Wohnraumeinbruch',
        'Branddelikte_insgesamt',
        'Brand_stiftung',
        'Sachbeschadigung_insgesamt',
        'Sachbeschadigung_Graffiti',
        'Rauschgift_delikte',
        'Kieztaten'
    ]
    
    # Entfernen von Anführungszeichen und Tausendertrennzeichen, Konvertieren zu Integer
    numeric_columns = [
        'Straftaten insgesamt', 'Raub', 'Strassenraub_Handtaschen_raub',
        'Koerper_verletzungen_insgesamt', 'Gefaehrl_schwere_Koerper_verletzung',
        'Freiheitsberaubung_noetigung_bedrohung_nachstellung', 'Diebstahl_insgesamt',
        'Diebstahl_Kraftwagen', 'Diebstahl_an_aus_Kfz', 'Fahrraddiebstahl',
        'Wohnraumeinbruch', 'Branddelikte_insgesamt', 'Brand_stiftung',
        'Sachbeschadigung_insgesamt', 'Sachbeschadigung_Graffiti',
        'Rauschgift_delikte', 'Kieztaten'
    ]
    
    for col in numeric_columns:
        df[col] = df[col].str.replace('"', '')  # Entfernen von Anführungszeichen
        df[col] = df[col].str.replace(',', '').astype(int)  # Entfernen von ',' und Konvertieren zu int
    
    # Sortieren der Bezirke nach 'Straftaten insgesamt' absteigend
    df_sorted = df.sort_values(by='Straftaten insgesamt', ascending=False)
    
    return df_sorted

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'
    
    # Daten laden und verarbeiten
    sorted_data = load_and_process_data(csv_file)
    
    # Ergebnis anzeigen
    print("Bezirke sortiert nach der Gesamtzahl der Straftaten (2023):\n")
    for index, row in sorted_data.iterrows():
        print(f"{row['Bezeichnung']}: {row['Straftaten insgesamt']}")
    
    # Optional: Sortierte Daten in eine neue CSV-Datei exportieren
    sorted_data.to_csv('FZ_2023_sorted.csv', index=False, encoding='utf-8')
    print("\nDie sortierten Daten wurden in 'FZ_2023_sorted.csv' gespeichert.")

if __name__ == "__main__":
    main()