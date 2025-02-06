import pandas as pd
import sys

def main():
    excel_file = 'Fallzahlen.xlsx'
    sheet_name = 'Fallzahlen_2023'
    lor_keys_to_exclude = [999900, 999999]
    
    try:
        # Schritt 1: Einlesen der Excel-Datei
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print("Excel-Datei erfolgreich eingelesen.")
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{excel_file}' wurde nicht gefunden.")
        sys.exit(1)
    except ValueError as e:
        print(f"Fehler beim Einlesen des Sheets '{sheet_name}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        sys.exit(1)
    
    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    required_columns = ['LOR-Schlüssel', 'Straftaten_insgesamt']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Fehler: Fehlende Spalten in den Daten: {missing_columns}")
        sys.exit(1)
    
    # Sicherstellen, dass 'LOR-Schlüssel' numerisch ist
    try:
        df['LOR-Schlüssel'] = pd.to_numeric(df['LOR-Schlüssel'])
    except ValueError:
        print("Fehler: Die Spalte 'LOR-Schlüssel' enthält nicht-numerische Werte.")
        sys.exit(1)
    
    # Schritt 2: Trennen der Bezirke und der auszuschließenden Schlüssel
    df_bezirke = df[~df['LOR-Schlüssel'].isin(lor_keys_to_exclude)]
    df_excluded = df[df['LOR-Schlüssel'].isin(lor_keys_to_exclude)]
    
    # Schritt 3: Sortieren der Bezirke nach 'Straftaten_insgesamt' absteigend
    if 'Straftaten_insgesamt' not in df_bezirke.columns:
        print("Fehler: Die Spalte 'Straftaten_insgesamt' ist nicht in den Daten vorhanden.")
        sys.exit(1)
    
    try:
        df_bezirke_sorted = df_bezirke.sort_values(by='Straftaten_insgesamt', ascending=False)
    except Exception as e:
        print(f"Fehler beim Sortieren der Daten: {e}")
        sys.exit(1)
    
    # Schritt 4: Zusammenführen der sortierten Bezirke mit den ausgeschlossenen Zeilen
    df_final = pd.concat([df_bezirke_sorted, df_excluded], ignore_index=True)
    
    # Optional: Ausgabe oder Speicherung des finalen DataFrames
    # Beispiel: Anzeigen der ersten 5 Zeilen
    print("Sortiertes DataFrame:")
    print(df_final.head())
    
    # Beispiel: Speichern in eine neue Excel-Datei
    output_file = 'Fallzahlen_sortiert.xlsx'
    try:
        df_final.to_excel(output_file, index=False)
        print(f"Das sortierte DataFrame wurde erfolgreich in '{output_file}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei '{output_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()