import pandas as pd

def process_fallzahlen_excel(file_path='Fallzahlen.xlsx'):
    """
    Liest die Excel-Datei ein, führt die Sheets zusammen, akkumuliert die Straftaten,
    sortiert das DataFrame nach 'Straftaten_insgesamt' und platziert spezielle
    LOR-Schlüssel am Ende.

    Parameters:
    - file_path: str, der Pfad zur Excel-Datei.

    Returns:
    - pd.DataFrame: Das sortierte DataFrame.
    """
    # Schritt 1: Excel-Datei einlesen und alle Sheets als DataFrames speichern
    try:
        sheets = pd.read_excel(file_path, sheet_name=None)
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Einlesen der Datei: {e}")
        return None

    # Schritt 2: DataFrames zusammenführen und Straftaten akkumulieren
    # Dabei werden alle Sheets kompiliert und numerische Werte summiert
    try:
        # Alle DataFrames zu einem einzigen DataFrame zusammenführen
        df_all = pd.concat(sheets.values(), ignore_index=True)
        
        # Gruppieren nach 'LOR-Schlüssel' und 'Bezirke' und numerische Spalten summieren
        group_columns = ['LOR-Schlüssel', 'Bezirke']
        df_grouped = df_all.groupby(group_columns, as_index=False).sum()
    except KeyError as e:
        print(f"Erforderliche Spalte fehlt: {e}")
        return None
    except Exception as e:
        print(f"Fehler beim Zusammenführen der DataFrames: {e}")
        return None

    # Schritt 3: Sortieren nach 'Straftaten_insgesamt', spezielle LOR-Schlüssel am Ende
    try:
        # Definieren der speziellen LOR-Schlüssel
        special_keys = [999900, 999999]
        
        # Separieren der speziellen und normalen Zeilen
        df_special = df_grouped[df_grouped['LOR-Schlüssel'].isin(special_keys)]
        df_normal = df_grouped[~df_grouped['LOR-Schlüssel'].isin(special_keys)]
        
        # Sortieren der normalen Zeilen nach 'Straftaten_insgesamt' absteigend
        df_normal_sorted = df_normal.sort_values(by='Straftaten_insgesamt', ascending=False)
        
        # Zusammenführen der sortierten normalen Zeilen mit den speziellen Zeilen
        df_final = pd.concat([df_normal_sorted, df_special], ignore_index=True)
    except KeyError:
        print("Die Spalte 'Straftaten_insgesamt' ist im DataFrame nicht vorhanden.")
        return None
    except Exception as e:
        print(f"Fehler beim Sortieren des DataFrames: {e}")
        return None

    # Schritt 4: Rückgabe des sortierten DataFrames
    return df_final

if __name__ == "__main__":
    # Verarbeiten der Excel-Datei und Erhalten des sortierten DataFrames
    sorted_df = process_fallzahlen_excel('Fallzahlen.xlsx')
    
    if sorted_df is not None:
        # Anzeige der ersten paar Zeilen des sortierten DataFrames
        print(sorted_df.head())
        
        # Optional: Speichern des sortierten DataFrames in einer neuen Excel-Datei
        # sorted_df.to_excel('Fallzahlen_sortiert.xlsx', index=False)