import pandas as pd

def calculate_bezirk_straftaten_percentage(excel_file: str, sheet_name: str = 'Fallzahlen_2023') -> pd.DataFrame:
    """
    Liest eine Excel-Datei ein und berechnet den prozentualen Anteil der
    Straftaten_insgesamt für jeden Bezirk im Vergleich zu ganz Berlin.

    Parameters:
    - excel_file: Pfad zur Excel-Datei.
    - sheet_name: Name des Sheets in der Excel-Datei (standardmäßig 'Fallzahlen_2023').

    Returns:
    - Ein Pandas DataFrame mit den Bezirken und ihrem prozentualen Anteil.
    """

    try:
        # 1. Excel-Datei einlesen
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print("Excel-Datei erfolgreich eingelesen.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei '{excel_file}' wurde nicht gefunden.")
    except Exception as e:
        raise Exception(f"Fehler beim Einlesen der Excel-Datei: {e}")

    # 2. DataFrame gespeichert (bereits in df)

    # 3. Überprüfen, ob die notwendigen Spalten vorhanden sind
    required_columns = ['Bezirke', 'Straftaten_insgesamt']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Die folgenden erforderlichen Spalten fehlen: {', '.join(missing_columns)}")
    print("Alle erforderlichen Spalten sind vorhanden.")

    # 4. Gesamtzahl der Straftaten für ganz Berlin finden
    total_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if total_row.empty:
        raise ValueError("Die Zeile mit 'Berlin (PKS gesamt)' wurde nicht gefunden.")
    total_straftaten = total_row['Straftaten_insgesamt'].values[0]
    print(f"Gesamtzahl der Straftaten für ganz Berlin: {total_straftaten}")

    # 5. Prozentualen Anteil der einzelnen Bezirke berechnen
    # Ausschließen der Gesamtzeile aus den Bezirken
    bezirk_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

    # Berechnung des prozentualen Anteils
    bezirk_df['Prozentualer_Anteil'] = (bezirk_df['Straftaten_insgesamt'] / total_straftaten) * 100

    # Optional: Runden auf zwei Dezimalstellen
    bezirk_df['Prozentualer_Anteil'] = bezirk_df['Prozentualer_Anteil'].round(2)

    # 6. Ergebnis als DataFrame zurückgeben
    result_df = bezirk_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']]

    print("Prozentualer Anteil der Straftaten pro Bezirk berechnet.")
    return result_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'

    # Berechnung durchführen
    try:
        prozent_df = calculate_bezirk_straftaten_percentage(excel_file)
        print("\nErgebnis:")
        print(prozent_df)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")