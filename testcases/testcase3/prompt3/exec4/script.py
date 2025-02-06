import pandas as pd

def main():
    # 1. Die Excel-Datei einlesen
    try:
        df = pd.read_excel('Fallzahlen.xlsx', sheet_name='Fallzahlen_2023')
    except FileNotFoundError:
        print("Die Datei 'Fallzahlen.xlsx' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Einlesen der Excel-Datei aufgetreten: {e}")
        return

    # 2. Die Tabelle als Pandas DataFrame gespeichert (bereits in 'df')

    # 3. Überprüfen, ob die notwendigen Spalten vorhanden sind
    notwendige_spalten = ['Bezirke', 'Straftaten_insgesamt']
    fehlende_spalten = [spalte for spalte in notwendige_spalten wenn spalte nicht in df.columns]
    wenn fehlende_spalten:
        print(f"Die folgenden notwendigen Spalten fehlen: {', '.join(fehlende_spalten)}")
        return

    # 4. Finde die Gesamtzahl der Straftaten für ganz Berlin
    gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    wenn gesamt_row.empty:
        print("Die Zeile mit Bezirk 'Berlin (PKS gesamt)' wurde nicht gefunden.")
        return
    gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].values[0]

    # 5. Berechne den prozentualen Anteil der einzelnen Bezirke von ganz Berlin
    # Exkludiere die Gesamtzeile aus der Berechnung
    bezirke_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()
    bezirke_df['Prozentualer_Anteil'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

    # Optional: Runden auf zwei Dezimalstellen
    bezirke_df['Prozentualer_Anteil'] = bezirke_df['Prozentualer_Anteil'].round(2)

    # 6. Das Ergebnis als DataFrame zurückgeben
    ergebnis_df = bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']]

    # Ergebnis anzeigen
    print(ergebnis_df)

if __name__ == "__main__":
    main()