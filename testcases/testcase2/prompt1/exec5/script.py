import pandas as pd

def lese_und_sortiere_fallzahlen(excel_datei):
    """
    Liest alle Sheets aus der gegebenen Excel-Datei, kombiniert die Daten,
    sortiert sie nach der Gesamtanzahl der Straftaten pro Bezirk und
    gibt das sortierte DataFrame zurück.

    :param excel_datei: Pfad zur Excel-Datei 'Fallzahlen.xlsx'
    :return: Sortiertes pandas DataFrame
    """
    try:
        # Alle Sheets lesen; sheet_name=None gibt ein Dictionary zurück
        alle_sheets = pd.read_excel(excel_datei, sheet_name=None)
        print(f"Anzahl der gelesenen Sheets: {len(alle_sheets)}")
    except FileNotFoundError:
        print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

    # Kombinieren aller DataFrames in einen
    try:
        kombiniertes_df = pd.concat(alle_sheets.values(), ignore_index=True)
        print(f"Anzahl der Zeilen nach dem Kombinieren: {len(kombiniertes_df)}")
    except ValueError as ve:
        print(f"Fehler beim Kombinieren der Daten: {ve}")
        return None

    # Sicherstellen, dass die Spalte 'Straftaten_insgesamt' numerisch ist
    if not pd.api.types.is_numeric_dtype(kombiniertes_df['Straftaten_insgesamt']):
        kombiniertes_df['Straftaten_insgesamt'] = pd.to_numeric(
            kombiniertes_df['Straftaten_insgesamt'], errors='coerce'
        )
        kombiniertes_df = kombiniertes_df.dropna(subset=['Straftaten_insgesamt'])

    # Sortieren nach 'Straftaten_insgesamt' absteigend
    sortiertes_df = kombiniertes_df.sort_values(
        by='Straftaten_insgesamt', ascending=False
    ).reset_index(drop=True)

    print("Die Daten wurden erfolgreich sortiert.")
    return sortiertes_df

def main():
    excel_datei = 'Fallzahlen.xlsx'
    df = lese_und_sortiere_fallzahlen(excel_datei)
    if df is not None:
        # Optional: Das sortierte DataFrame anzeigen
        print(df)

        # Optional: Das sortierte DataFrame speichern
        # df.to_csv('Sortierte_Fallzahlen.csv', index=False, encoding='utf-8-sig')
        # print("Das sortierte DataFrame wurde als 'Sortierte_Fallzahlen.csv' gespeichert.")

if __name__ == "__main__":
    main()