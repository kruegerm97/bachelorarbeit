import pandas as pd
import sys

def read_excel_file(file_path, sheet_name):
    """
    Liest eine Excel-Datei und gibt das entsprechende Sheet als DataFrame zurück.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Erfolgreich das Blatt '{sheet_name}' aus '{file_path}' gelesen.")
        return df
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
        sys.exit(1)
    except ValueError:
        print(f"Fehler: Das Blatt '{sheet_name}' existiert nicht in '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        sys.exit(1)

def validate_columns(df, required_columns):
    """
    Überprüft, ob die erforderlichen Spalten im DataFrame vorhanden sind.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Fehler: Die folgenden erforderlichen Spalten fehlen im DataFrame: {missing_columns}")
        sys.exit(1)
    else:
        print("Alle erforderlichen Spalten sind vorhanden.")

def sort_dataframe(df, sort_column, exclude_keys, key_column):
    """
    Sortiert den DataFrame nach 'sort_column' absteigend, wobei die Zeilen mit 'exclude_keys'
    am Ende verbleiben.
    """
    # Trennen der Zeilen, die ausgeschlossen werden sollen
    df_excluded = df[df[key_column].isin(exclude_keys)]
    df_to_sort = df[~df[key_column].isin(exclude_keys)]
    
    # Sortieren der relevanten Zeilen
    df_sorted = df_to_sort.sort_values(by=sort_column, ascending=False)
    
    # Zusammenführen der sortierten und ausgeschlossenen Zeilen
    df_final = pd.concat([df_sorted, df_excluded], ignore_index=True)
    
    print("DataFrame erfolgreich sortiert.")
    return df_final

def main():
    # Parameter
    file_path = 'Fallzahlen.xlsx'
    sheet_name = 'Fallzahlen_2023'
    sort_column = 'Straftaten_insgesamt'
    key_column = 'LOR-Schlüssel'
    exclude_keys = [999900, 999999]
    output_file = 'Fallzahlen_sortiert.xlsx'
    
    # Schritt 1: Daten einlesen
    df = read_excel_file(file_path, sheet_name)
    
    # Schritt 2: Validierung der erforderlichen Spalten
    required_columns = [sort_column, key_column]
    validate_columns(df, required_columns)
    
    # Schritt 3: Sortierung durchführen
    df_sorted = sort_dataframe(df, sort_column, exclude_keys, key_column)
    
    # Optional: Weitere Überprüfung, ob alle Zeilen enthalten sind
    if len(df_sorted) != len(df):
        print("Warnung: Die Anzahl der Zeilen nach der Sortierung stimmt nicht mit der ursprünglichen Anzahl überein.")
    
    # Schritt 4: Ergebnis speichern
    try:
        df_sorted.to_excel(output_file, index=False)
        print(f"Das sortierte DataFrame wurde erfolgreich in '{output_file}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()