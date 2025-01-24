import pandas as pd
import os

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'
    
    # Überprüfen, ob die Datei existiert
    if not os.path.exists(csv_file):
        print(f"Die Datei {csv_file} wurde nicht gefunden.")
        return
    
    try:
        # Lesen der CSV-Datei, Überspringen der ersten 4 Zeilen
        df = pd.read_csv(
            csv_file,
            skiprows=4,
            sep=',',
            quotechar='"',
            thousands=',',
            encoding='utf-8'
        )
        
        # Bereinigen der Spaltennamen: Entfernen von Zeilenumbrüchen und Leerzeichen
        df.columns = [col.replace('\n', ' ').strip() for col in df.columns]
        
        # Suchen der Spalte für "Straftaten insgesamt"
        str_column = None
        for col in df.columns:
            if 'Straftaten' in col and 'insgesamt' in col.lower():
                str_column = col
                break
        
        if not str_column:
            print("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")
            return
        
        # Umwandeln der "Straftaten insgesamt" in numerische Werte
        df[str_column] = pd.to_numeric(df[str_column], errors='coerce')
        
        # Sortieren des DataFrames nach "Straftaten insgesamt" in absteigender Reihenfolge
        df_sorted = df.sort_values(by=str_column, ascending=False)
        
        # Auswählen der relevanten Spalten für die Anzeige
        output_df = df_sorted[['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', str_column]]
        
        # Umbenennen der Spalten für bessere Lesbarkeit
        output_df = output_df.rename(columns={
            'LOR-Schlüssel (Bezirksregion)': 'LOR-Schlüssel',
            'Bezeichnung (Bezirksregion)': 'Bezirksbezeichnung',
            str_column: 'Straftaten Insgesamt'
        })
        
        # Anzeigen der sortierten Tabelle
        print(output_df.to_string(index=False))
        
        # Optional: Speichern der sortierten Daten in einer neuen CSV-Datei
        output_file = 'FZ_2023_sorted.csv'
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nDie sortierten Daten wurden in '{output_file}' gespeichert.")
        
    except Exception as e:
        print(f"Es gab einen Fehler beim Verarbeiten der Datei: {e}")

if __name__ == "__main__":
    main()