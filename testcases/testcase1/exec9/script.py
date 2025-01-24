import pandas as pd

def main():
    # Pfad zur CSV-Datei
    csv_datei = 'FZ_2023.csv'
    
    try:
        # Schritt 1: CSV-Datei einlesen und die ersten 4 Zeilen überspringen
        # Diese Zeilen enthalten Metadaten und leere Zeilen
        df = pd.read_csv(
            csv_datei,
            skiprows=4,                # Überspringt die ersten 4 Zeilen
            sep=',',                   # Komma als Trennzeichen
            encoding='utf-8',          # UTF-8 Encoding
            thousands=',',             # Komma als Tausendertrennzeichen
            engine='python'            # Verwenden des Python-Engines für flexiblere Parser-Optionen
        )
        
        # Schritt 2: Spaltennamen bereinigen (Entfernen von Zeilenumbrüchen und Leerzeichen)
        df.columns = df.columns.str.replace('\n', ' ', regex=True).str.strip()
        
        # Optional: Überprüfen der Spaltennamen
        # print(df.columns)
        
        # Schritt 3: Identifizieren der relevanten Spalten
        # Angenommen, die Spalte für 'Straftaten insgesamt' enthält 'Straftaten' und 'insgesamt' im Namen
        straffaten_col = [col for col in df.columns if 'Straftaten' in col and 'insgesamt' in col.lower()]
        if not straffaten_col:
            raise ValueError("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")
        straffaten_col = straffaten_col[0]
        
        # Identifizieren der Spalte für die Bezirksbezeichnung
        bezirk_col = 'Bezeichnung (Bezirksregion)'
        
        # Schritt 4: Daten bereinigen und sicherstellen, dass die relevanten Spalten numerisch sind
        df[straffaten_col] = pd.to_numeric(df[straffaten_col], errors='coerce')
        
        # Entfernen von Zeilen mit fehlenden Werten in den relevanten Spalten
        df = df.dropna(subset=[bezirk_col, straffaten_col])
        
        # Schritt 5: Sortieren der Bezirke nach der Gesamtanzahl der Straftaten (absteigend)
        df_sorted = df.sort_values(by=straffaten_col, ascending=False)
        
        # Schritt 6: Auswahl der relevanten Spalten für die Ausgabe
        ergebnis_df = df_sorted[[bezirk_col, straffaten_col]].reset_index(drop=True)
        
        # Optional: Anzeigen der sortierten Tabelle
        print(ergebnis_df)
        
        # Schritt 7: Speichern des Ergebnisses in einer neuen CSV-Datei
        ergebnis_df.to_csv('sortierte_straftaten_2023.csv', index=False, encoding='utf-8')
        print("\nDie sortierte Liste wurde in 'sortierte_straftaten_2023.csv' gespeichert.")
    
    except FileNotFoundError:
        print(f"Die Datei '{csv_datei}' wurde nicht gefunden. Bitte überprüfe den Dateipfad.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()