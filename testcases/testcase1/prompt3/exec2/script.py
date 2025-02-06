import pandas as pd

def sort_fallzahlen_excel(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Liest die Excel-Datei, sortiert die Daten nach 'Straftaten_insgesamt' absteigend,
    wobei die Zeilen mit den LOR-Schlüsseln 999900 und 999999 am Ende bleiben.

    Parameters:
    - file_path: Pfad zur Excel-Datei.
    - sheet_name: Name des Sheets in der Excel-Datei.

    Returns:
    - Sortierter Pandas DataFrame.
    """
    try:
        # Schritt 1: Einlesen der Excel-Datei
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Excel-Datei '{file_path}' erfolgreich eingelesen.")

        # Überprüfen, ob die notwendigen Spalten vorhanden sind
        benötigte_spalten = ['LOR-Schlüssel', 'Straftaten_insgesamt']
        fehlende_spalten = [spalte for spalte in benötigte_spalten if spalte not in df.columns]
        if fehlende_spalten:
            raise ValueError(f"Fehlende Spalten in der Excel-Datei: {fehlende_spalten}")

        # Schritt 2: Trennen der Bezirke und Nicht-Bezirke
        nicht_bezirke_keys = [999900, 999999]
        
        # Sicherstellen, dass 'LOR-Schlüssel' als numerisch betrachtet wird
        df['LOR-Schlüssel'] = pd.to_numeric(df['LOR-Schlüssel'], errors='coerce')

        bezirke_df = df[~df['LOR-Schlüssel'].isin(nicht_bezirke_keys)].copy()
        nicht_bezirke_df = df[df['LOR-Schlüssel'].isin(nicht_bezirke_keys)].copy()

        # Schritt 3: Sortieren der Bezirke nach 'Straftaten_insgesamt' absteigend
        bezirke_df.sort_values(by='Straftaten_insgesamt', ascending=False, inplace=True)

        # Schritt 4: Zusammenfügen der sortierten Bezirke mit den Nicht-Bezirken
        sortiertes_df = pd.concat([bezirke_df, nicht_bezirke_df], ignore_index=True)

        print("Daten erfolgreich sortiert.")
        return sortiertes_df

    except FileNotFoundError:
        print(f"Datei '{file_path}' wurde nicht gefunden.")
    except ValueError as ve:
        print(f"Wertfehler: {ve}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

# Anwendung des Skripts
if __name__ == "__main__":
    datei_pfad = 'Fallzahlen.xlsx'
    sheet = 'Fallzahlen_2023'

    sortiertes_dataframe = sort_fallzahlen_excel(datei_pfad, sheet)

    if sortiertes_dataframe is not None:
        # Schritt 5: Optional - Speichern des sortierten DataFrames in einer neuen Excel-Datei
        ausgabe_pfad = 'Sortierte_Fallzahlen.xlsx'
        try:
            sortiertes_dataframe.to_excel(ausgabe_pfad, index=False)
            print(f"Sortiertes DataFrame wurde erfolgreich in '{ausgabe_pfad}' gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")