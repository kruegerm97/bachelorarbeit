import pandas as pd

def load_and_clean_data(csv_file):
    """
    Lädt die CSV-Datei, bereinigt die Daten und gibt einen bereinigten DataFrame zurück.
    """
    try:
        # Überspringe die ersten 4 Zeilen, die keine relevanten Daten enthalten
        df = pd.read_csv(csv_file, skiprows=4, sep=',', encoding='utf-8')
        
        # Identifiziere die relevanten Spalten
        # Da die Spaltennamen Zeilenumbrüche enthalten können, benennen wir sie um
        # Basierend auf den bereitgestellten Daten:
        # Index 0: LOR-Schlüssel
        # Index 1: Bezeichnung
        # Index 2: Straftaten insgesamt
        df = df.rename(columns={
            df.columns[0]: 'LOR_Schluessel',
            df.columns[1]: 'Bezirksname',
            df.columns[2]: 'Straftaten_insgesamt'
        })
        
        # Entferne alle Zeilen, die keine LOR_Schluessel enthalten (z.B. leere Zeilen)
        df = df.dropna(subset=['LOR_Schluessel'])
        
        # Entferne Anführungszeichen und Leerzeichen
        df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].astype(str).str.replace('"', '').str.replace(' ', '')
        
        # Entferne Tausendertrennzeichen und konvertiere in Ganzzahlen
        df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].str.replace(',', '').astype(int)
        
        return df
    except Exception as e:
        print(f"Fehler beim Laden oder Bereinigen der Daten: {e}")
        return None

def sort_districts_by_crime(df):
    """
    Sortiert die Bezirke nach der Gesamtanzahl der Straftaten in absteigender Reihenfolge.
    """
    try:
        sorted_df = df.sort_values(by='Straftaten_insgesamt', ascending=False)
        return sorted_df
    except Exception as e:
        print(f"Fehler beim Sortieren der Daten: {e}")
        return None

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'
    
    # Lade und bereinige die Daten
    df = load_and_clean_data(csv_file)
    
    if df is not None:
        # Sortiere die Bezirke nach Straftaten insgesamt
        sorted_df = sort_districts_by_crime(df)
        
        if sorted_df is not None:
            # Zeige die sortierten Ergebnisse
            print("Bezirke sortiert nach Gesamtzahl der Straftaten (2023):\n")
            print(sorted_df[['Bezirksname', 'Straftaten_insgesamt']].to_string(index=False))
            
            # Optional: Speichere die sortierten Daten in einer neuen CSV-Datei
            sorted_df.to_csv('Sortierte_FZ_2023.csv', columns=['Bezirksname', 'Straftaten_insgesamt'], index=False)
            print("\nDie sortierten Daten wurden in 'Sortierte_FZ_2023.csv' gespeichert.")
    else:
        print("Daten konnten nicht geladen werden.")

if __name__ == "__main__":
    main()