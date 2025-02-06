import pandas as pd

def verarbeite_fallzahlen(dateipfad: str, sheet_name: str = 'Fallzahlen_2023') -> pd.DataFrame:
    """
    Liest eine Excel-Datei ein, überprüft notwendige Spalten, berechnet
    den prozentualen Anteil der Straftaten pro Bezirk und gibt das Ergebnis als DataFrame zurück.

    :param dateipfad: Pfad zur Excel-Datei 'Fallzahlen.xlsx'.
    :param sheet_name: Name des Sheets in der Excel-Datei. Standard ist 'Fallzahlen_2023'.
    :return: DataFrame mit Bezirken, Straftaten insgesamt und prozentualem Anteil.
    """
    try:
        # 1. Excel-Datei einlesen
        df = pd.read_excel(dateipfad, sheet_name=sheet_name)
        print("Excel-Datei erfolgreich eingelesen.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei '{dateipfad}' wurde nicht gefunden.")
    except Exception as e:
        raise Exception(f"Fehler beim Einlesen der Excel-Datei: {e}")

    # 2. Die Tabelle als Pandas DataFrame gespeichert (bereits in `df`)

    # 3. Überprüfen, ob die notwendigen Spalten vorhanden sind
    erforderliche_spalten = ['Bezirke', 'Straftaten_insgesamt']
    fehlende_spalten = [spalte for spalte in erforderliche_spalten if spalte not in df.columns]
    if fehlende_spalten:
        raise ValueError(f"Die folgenden erforderlichen Spalten fehlen in der Tabelle: {fehlende_spalten}")
    else:
        print("Alle erforderlichen Spalten sind vorhanden.")

    # 4. Gesamtzahl der Straftaten für ganz Berlin finden
    gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if gesamt_row.empty:
        raise ValueError("Die Zeile mit 'Berlin (PKS gesamt)' wurde nicht gefunden.")
    
    gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].iloc[0]
    print(f"Gesamtzahl der Straftaten in Berlin: {gesamt_straftaten}")

    if gesamt_straftaten == 0:
        raise ValueError("Die Gesamtzahl der Straftaten ist 0, kann keine Prozente berechnen.")

    # 5. Prozentualen Anteil der einzelnen Bezirke berechnen
    # Ausschließen der Gesamtzeile von den einzelnen Bezirken
    einzel_bezirke = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

    # Berechnung des prozentualen Anteils
    einzel_bezirke['Prozentualer_Anteil'] = (einzel_bezirke['Straftaten_insgesamt'] / gesamt_straftaten) * 100

    # Optional: Auf zwei Dezimalstellen runden
    einzel_bezirke['Prozentualer_Anteil'] = einzel_bezirke['Prozentualer_Anteil'].round(2)

    # 6. Ergebnis als DataFrame zurückgeben
    ergebnis = einzel_bezirke[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']]

    return ergebnis

if __name__ == "__main__":
    dateipfad = 'Fallzahlen.xlsx'  # Pfad zur Excel-Datei anpassen, falls erforderlich
    try:
        ergebnis_df = verarbeite_fallzahlen(dateipfad)
        print("\nProzentualer Anteil der Straftaten pro Bezirk in Berlin:")
        print(ergebnis_df.to_string(index=False))
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")