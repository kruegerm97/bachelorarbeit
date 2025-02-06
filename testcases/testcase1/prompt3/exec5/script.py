import pandas as pd

def sort_fallzahlen_excel(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Liest die Daten aus dem angegebenen Excel-Sheet, sortiert sie nach 'Straftaten_insgesamt' absteigend,
    wobei die Zeilen mit den LOR-Schlüsseln 999900 und 999999 am Ende des DataFrames stehen.

    Parameters:
    - file_path: Pfad zur Excel-Datei.
    - sheet_name: Name des Sheets, das eingelesen werden soll.

    Returns:
    - Ein sortierter Pandas DataFrame.
    """
    try:
        # Schritt 1: Einlesen der Excel-Datei
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Erfolgreich das Sheet '{sheet_name}' aus '{file_path}' eingelesen.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei '{file_path}' wurde nicht gefunden.")
    except ValueError:
        raise ValueError(f"Das Sheet '{sheet_name}' existiert nicht in '{file_path}'.")
    except Exception as e:
        raise Exception(f"Ein unerwarteter Fehler ist beim Einlesen der Excel-Datei aufgetreten: {e}")

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    required_columns = ['LOR-Schlüssel', 'Straftaten_insgesamt']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Die folgenden erforderlichen Spalten fehlen im DataFrame: {missing_columns}")
    else:
        print("Alle erforderlichen Spalten sind vorhanden.")

    # Schritt 2: Separiere die Bezirke und die nicht zuzuordnenden Einträge
    # Definiere die LOR-Schlüssel, die nicht sortiert werden sollen
    exclude_lor_keys = [999900, 999999]

    # Konvertiere 'LOR-Schlüssel' zu integer, falls nötig
    if df['LOR-Schlüssel'].dtype != 'int64' and df['LOR-Schlüssel'].dtype != 'int32':
        try:
            df['LOR-Schlüssel'] = df['LOR-Schlüssel'].astype(int)
            print("'LOR-Schlüssel' erfolgreich in Integer konvertiert.")
        except ValueError:
            raise ValueError("'LOR-Schlüssel' enthält nicht-numerische Werte, die nicht in Integer konvertiert werden können.")

    # Teile den DataFrame in Bezirke und Nicht-Bezirke
    bezirke_df = df[~df['LOR-Schlüssel'].isin(exclude_lor_keys)]
    nicht_bezirke_df = df[df['LOR-Schlüssel'].isin(exclude_lor_keys)]

    print(f"Anzahl der Bezirke: {bezirke_df.shape[0]}")
    print(f"Anzahl der nicht zuzuordnenden Einträge: {nicht_bezirke_df.shape[0]}")

    # Schritt 3: Sortiere die Bezirke nach 'Straftaten_insgesamt' absteigend
    try:
        bezirke_sorted = bezirke_df.sort_values(by='Straftaten_insgesamt', ascending=False)
        print("Bezirke erfolgreich nach 'Straftaten_insgesamt' absteigend sortiert.")
    except KeyError:
        raise KeyError("Die Spalte 'Straftaten_insgesamt' wurde nicht gefunden und kann nicht zum Sortieren verwendet werden.")
    except Exception as e:
        raise Exception(f"Ein unerwarteter Fehler ist beim Sortieren der Bezirke aufgetreten: {e}")

    # Schritt 4: Konkateniere die sortierten Bezirke mit den nicht zuzuordnenden Einträgen
    final_df = pd.concat([bezirke_sorted, nicht_bezirke_df], ignore_index=True)
    print("Bezirke und nicht zuzuordnende Einträge erfolgreich kombiniert.")

    return final_df

if __name__ == "__main__":
    # Definiere den Pfad zur Excel-Datei und den Sheet-Namen
    excel_file = 'Fallzahlen.xlsx'
    sheet = 'Fallzahlen_2023'

    try:
        # Führe die Sortierung durch und hole das sortierte DataFrame
        sortiertes_df = sort_fallzahlen_excel(excel_file, sheet)
        print("Daten erfolgreich sortiert.")

        # Optional: Anzeige der ersten paar Zeilen des sortierten DataFrames
        print(sortiertes_df.head())

        # Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
        # sortiertes_df.to_excel('Fallzahlen_sortiert.xlsx', index=False)
        # print("Sortiertes DataFrame wurde in 'Fallzahlen_sortiert.xlsx' gespeichert.")

    except Exception as e:
        print(f"Fehler: {e}")