import pandas as pd

def compute_percentage_change(excel_file, target_row, target_column, sheet_prefix):
    """
    Liest eine Excel-Datei mit mehreren Sheets, extrahiert die Straftaten_insgesamt für
    einen bestimmten Eintrag und berechnet die prozentuale Veränderung zum Vorjahr.

    Parameters:
    - excel_file: str, Pfad zur Excel-Datei.
    - target_row: str, Der Eintrag in der 'Bezirke' Spalte, z.B. "Berlin (PKS gesamt)".
    - target_column: str, Name der Spalte, deren prozentuale Veränderung berechnet werden soll, z.B. "Straftaten_insgesamt".
    - sheet_prefix: str, Präfix der Sheet-Namen, z.B. "Fallzahlen_" für Sheets wie "Fallzahlen_2014".

    Returns:
    - pandas.DataFrame mit den Jahren und der prozentualen Veränderung.
    """
    try:
        # Alle Sheets einlesen
        sheets_dict = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
    except FileNotFoundError:
        print(f"Die Datei {excel_file} wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten beim Einlesen der Datei: {e}")
        return None

    data = []

    for sheet_name, df in sheets_dict.items():
        # Überprüfen, ob der Sheet-Name dem erwarteten Muster entspricht
        if not sheet_name.startswith(sheet_prefix):
            print(f"Überspringe Sheet '{sheet_name}', da es nicht mit '{sheet_prefix}' beginnt.")
            continue

        # Extrahiere das Jahr aus dem Sheet-Namen
        try:
            year_str = sheet_name.replace(sheet_prefix, "")
            year = int(year_str)
        except ValueError:
            print(f"Konnte das Jahr aus dem Sheet-Namen '{sheet_name}' nicht extrahieren.")
            continue

        # Suche die Zeile mit dem gewünschten Eintrag
        row = df[df['Bezirke'] == target_row]

        if row.empty:
            print(f"Der Eintrag '{target_row}' wurde in Sheet '{sheet_name}' nicht gefunden.")
            continue

        # Extrahiere den Wert der Zielspalte
        try:
            value = row.iloc[0][target_column]
            data.append({'Year': year, target_column: value})
        except KeyError:
            print(f"Die Spalte '{target_column}' wurde in Sheet '{sheet_name}' nicht gefunden.")
            continue

    if not data:
        print("Keine Daten gefunden, um die prozentuale Veränderung zu berechnen.")
        return None

    # Erstelle einen DataFrame aus den gesammelten Daten
    df_data = pd.DataFrame(data)

    # Sortiere die Daten nach Jahr
    df_data = df_data.sort_values('Year').reset_index(drop=True)

    # Berechne die prozentuale Veränderung zum Vorjahr
    df_data['Percentage_Change'] = df_data[target_column].pct_change() * 100

    return df_data[['Year', 'Percentage_Change']]

if __name__ == "__main__":
    # Parameter festlegen
    excel_file = 'Fallzahlen.xlsx'
    target_row = 'Berlin (PKS gesamt)'
    target_column = 'Straftaten_insgesamt'
    sheet_prefix = 'Fallzahlen_'

    # Funktion aufrufen
    percentage_change_df = compute_percentage_change(excel_file, target_row, target_column, sheet_prefix)

    if percentage_change_df is not None:
        print("Prozentuale Veränderung der Straftaten_insgesamt zum Vorjahr:")
        print(percentage_change_df)

        # Optional: DataFrame speichern
        # percentage_change_df.to_csv('prozentuale_veraenderung.csv', index=False)